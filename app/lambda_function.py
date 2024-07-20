import json

from ssm_service import SSMService

ssm_service = SSMService('/dev/onepiece-app/env')

def lambda_handler(event, context):
    print(f'Processing event: {event}')
    try:
        body = json.loads(event['body'])
        field = body['field']
        new_value = body['value']

        parameters = ssm_service.get_parameter_store_value()
        print(parameters)

        new_parameters = []
        for param in parameters.split(';'):
            parameters = param.split('=')
            print(f'Validating {parameters[0]}')
            if parameters[0] == field:
                print(f'Updating {field} to {new_value}')
                parameters[1] = new_value
            new_parameters.append('='.join(parameters))

        parameters = ';'.join(new_parameters)
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
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error updating parameters',
                'error': str(e)
            })
        }
