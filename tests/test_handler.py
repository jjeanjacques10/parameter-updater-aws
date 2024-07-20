import json
import boto3
import pytest
from moto import mock_aws
from app.lambda_function import lambda_handler


@pytest.fixture(scope='function')
def ssm_client():
    with mock_aws():
        yield boto3.client('ssm', region_name='us-east-1')


def test_should_update_parameters_with_semicolon_delimiter(ssm_client):
    initial_parameters = 'PORT=8080;TIMEOUT_API_REQUEST=3000;TOGGLE_CARDS_OFFLINE=true'

    ssm_client.put_parameter(
        Name='/dev/onepiece-app/env',
        Description='Parameters for onepiece-app',
        Value=initial_parameters,
        Type='SecureString',
        Overwrite=True
    )

    # Define the lambda event
    event = {
        'body': json.dumps({
            'field': 'TIMEOUT_API_REQUEST',
            'value': '1000',
            'parameter_store_name': '/dev/onepiece-app/env'
        })
    }
    context = {}

    # Invoke the lambda function
    response = lambda_handler(event, context)

    # Verify the response
    assert response['statusCode'] == 200
    response_body = json.loads(response['body'])
    assert 'Parameters updated successfully' in response_body['message']

    # Verify the parameter was updated in SSM
    updated_parameters = ssm_client.get_parameter(Name='/dev/onepiece-app/env', WithDecryption=True)
    assert updated_parameters['Parameter']['Value'] == 'PORT=8080;TIMEOUT_API_REQUEST=1000;TOGGLE_CARDS_OFFLINE=true'


def test_should_update_parameters_with_commas_delimiter(ssm_client):
    initial_parameters = 'PORT=8080,TIMEOUT_API_REQUEST=3000,TOGGLE_CARDS_OFFLINE=true'

    ssm_client.put_parameter(
        Name='/dev/onepiece-app/env',
        Description='Parameters for onepiece-app',
        Value=initial_parameters,
        Type='SecureString',
        Overwrite=True
    )

    # Define the lambda event
    event = {
        'body': json.dumps({
            'field': 'TIMEOUT_API_REQUEST',
            'value': '1000',
            'parameter_store_name': '/dev/onepiece-app/env'
        })
    }
    context = {}

    # Invoke the lambda function
    response = lambda_handler(event, context)

    # Verify the response
    assert response['statusCode'] == 200
    response_body = json.loads(response['body'])
    assert 'Parameters updated successfully' in response_body['message']

    # Verify the parameter was updated in SSM
    updated_parameters = ssm_client.get_parameter(Name='/dev/onepiece-app/env', WithDecryption=True)
    assert updated_parameters['Parameter']['Value'] == 'PORT=8080,TIMEOUT_API_REQUEST=1000,TOGGLE_CARDS_OFFLINE=true'


def test_should_update_parameters_with_semicolon_and_commas(ssm_client):
    initial_parameters = 'PORT=8080;TIMEOUT_API_REQUEST=3000;TOGGLE_CARDS_OFFLINE=true;ISLANDS_LIST=orange,blue,green'

    ssm_client.put_parameter(
        Name='/dev/onepiece-app/env',
        Description='Parameters for onepiece-app',
        Value=initial_parameters,
        Type='SecureString',
        Overwrite=True
    )

    # Define the lambda event
    event = {
        'body': json.dumps({
            'field': 'ISLANDS_LIST',
            'value': 'blue,green',
            'parameter_store_name': '/dev/onepiece-app/env'
        })
    }
    context = {}

    # Invoke the lambda function
    response = lambda_handler(event, context)

    # Verify the response
    assert response['statusCode'] == 200
    response_body = json.loads(response['body'])
    assert 'Parameters updated successfully' in response_body['message']

    # Verify the parameter was updated in SSM
    updated_parameters = ssm_client.get_parameter(Name='/dev/onepiece-app/env', WithDecryption=True)
    assert updated_parameters['Parameter'][
               'Value'] == 'PORT=8080;TIMEOUT_API_REQUEST=3000;TOGGLE_CARDS_OFFLINE=true;ISLANDS_LIST=blue,green'


def test_should_update_parameters_with_commas_and_semicolon(ssm_client):
    initial_parameters = 'PORT=8080,TIMEOUT_API_REQUEST=3000,TOGGLE_CARDS_OFFLINE=true,ISLANDS_LIST=orange;blue;green'

    ssm_client.put_parameter(
        Name='/dev/onepiece-app/env',
        Description='Parameters for onepiece-app',
        Value=initial_parameters,
        Type='SecureString',
        Overwrite=True
    )

    # Define the lambda event
    event = {
        'body': json.dumps({
            'field': 'ISLANDS_LIST',
            'value': 'blue;green',
            'parameter_store_name': '/dev/onepiece-app/env'
        })
    }
    context = {}

    # Invoke the lambda function
    response = lambda_handler(event, context)

    # Verify the response
    assert response['statusCode'] == 200
    response_body = json.loads(response['body'])
    assert 'Parameters updated successfully' in response_body['message']

    # Verify the parameter was updated in SSM
    updated_parameters = ssm_client.get_parameter(Name='/dev/onepiece-app/env', WithDecryption=True)
    assert updated_parameters['Parameter'][
               'Value'] == 'PORT=8080,TIMEOUT_API_REQUEST=3000,TOGGLE_CARDS_OFFLINE=true,ISLANDS_LIST=blue;green'
