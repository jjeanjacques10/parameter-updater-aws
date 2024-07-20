import json, re

from ssm_service import SSMService

ssm_service = SSMService()


def get_delimiter(parameters):
    pattern = r'[;,]'
    match = re.search(pattern, parameters)

    if not match:
        raise Exception('Delimiter not found')
    return match.group()


def lambda_handler(event, context):
    print(f'Processing event: {event}')
    try:
        body = json.loads(event['body'])
        field = body['field']
        new_value = body['value']
        ssm_service.parameter_store_name = body['parameter_store_name']

        parameters = ssm_service.get_parameter_store_value()
        print(parameters)

        delimiter = get_delimiter(parameters)

        new_parameters = []
        for param in parameters.split(delimiter):
            parameters = param.split('=')
            if parameters[0] == field:
                print(f'Updating {field} to {new_value}')
                parameters[1] = new_value
            new_parameters.append('='.join(parameters))

        parameters = delimiter.join(new_parameters)
        print(parameters)

        ssm_service.update_parameter_store_value(parameters)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Parameters updated successfully',
                'parameters': parameters
            })
        }
    except Exception as e:
        print(f"Error updating parameters: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error updating parameters',
                'error': str(e)
            })
        }
