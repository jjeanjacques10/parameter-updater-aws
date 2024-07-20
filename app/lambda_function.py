import logging
import json

from app.ssm_service import SSMService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
ssm_service = SSMService('/dev/onepiece-app/env')


def lambda_handler(event, context):
    print(f'Processing event: {event}')
    try:
        body = json.loads(event['body'])
        field = body['field']
        new_value = body['value']

        parameters = ssm_service.get_parameter_store_value()
        logging.info(parameters)

        new_parameters = []
        for param in parameters.split(';'):
            parameters = param.split('=')
            if parameters[0] == field:
                logging.info(f'Updating {field} to {new_value}')
                parameters[1] = new_value
            new_parameters.append('='.join(parameters))

        parameters = ';'.join(new_parameters)
        logging.info(parameters)

        ssm_service.update_parameter_store_value(parameters)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Parameters updated successfully',
                'parameters': parameters
            })
        }
    except Exception as e:
        logging.error(f"Error updating parameters: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error updating parameters',
                'error': str(e)
            })
        }
