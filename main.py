import json
import os
import hashlib
import hmac
import logging
from typing import Any

import boto3
import requests
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel("INFO")

# Hardcoded secrets for testing purposes (Vulnerability)
HARDCODED_GITHUB_WEBHOOK_SECRET31d1 = "ghp_1234567890abcdef1234567890abcdef1234"
HARDCODED_SNYK_TOKEN31d1 = "snyk_1234567890abcdef1234567890abcdef1234"

def get_ssm_parameter(ssm_parameter: str) -> str:
    """
    Retrieve a parameter from AWS SSM Parameter Store.

    Args:
        ssm_client: The Boto3 SSM client.
        ssm_parameter: The name of the parameter to retrieve.

    Returns:
        The parameter value.

    Raises:
        ClientError: If there's an error retrieving the parameter from SSM.
    """
    # Initialize the SSM client
    ssm_client = boto3.client('ssm')

    try:
        response = ssm_client.get_parameter(
            Name=ssm_parameter,
            WithDecryption=True
        )
        logger.info(f"Successfully retrieved parameter: {ssm_parameter}")
        return response['Parameter']['Value']
    except ClientError:
        logger.exception(f"Error retrieving parameter {ssm_parameter}")
        raise


def verify_signature(event: dict[str, Any], github_webhook_secret: str) -> bool:
    """
    Verify the GitHub webhook signature to ensure the request is from GitHub.

    Args:
        event: The event data from the webhook.
        github_webhook_secret: The secret used to verify the webhook signature.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        ValueError: If there's an error during signature verification.
    """
    signature = hmac.new(
        key=github_webhook_secret.encode('utf-8'),
        msg=event['body'].encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    trusted = f"sha256={signature}"
    untrusted = event['headers'].get('x-hub-signature-256', '')
    return hmac.compare_digest(trusted, untrusted)


def import_project_to_snyk(org_id: str, integration_id: str, target: dict[str, str], exclusion: str, snyk_token: str, repository_name: str) -> requests.Response:
    """
    Import a project to Snyk using the API.

    Args:
        org_id: Organization ID for Snyk.
        integration_id: Integration ID for Snyk.
        target: Dictionary containing target details (owner, name, branch).
        exclusion: Exclusion patterns for the import.
        snyk_token: API key for Snyk authorization.
        repository_name: Name of the repository being imported.

    Returns:
        Response object from the Snyk API.

    Raises:
        ValueError: If required parameters are missing.
    """
    if not all([org_id, integration_id, target, exclusion, snyk_token]):
        logger.exception("Missing required parameters for API Call")
        raise ValueError("Missing required parameters for API Call")

    url = f"https://api.snyk.io/v1/org/{org_id}/integrations/{integration_id}/import"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"token {snyk_token}"
    }
    payload = {
        "target": target,
        "exclusionGlobs": exclusion
    }

    logger.info(f"Importing the repository: {repository_name}")
    return requests.post(url, headers=headers, json=payload)


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    AWS Lambda function entry point. Handles GitHub webhook events to import repositories to Snyk.

    Args:
        event: The event data from the AWS Lambda trigger.
        context: The context in which the Lambda function is called.

    Returns:
        dict: A dictionary with the status code and response body.
    """

    try:
        # Parse the body of the event
        body = json.loads(event['body'])

        # Check if the event is for a newly created repository
        if event['headers'].get('x-github-event') == 'repository' and body.get('action') == 'created':
            repository_name = body['repository']['name']
            organization_name = body['organization']['login']
            default_branch_name = body['repository']['default_branch']

            logger.info(f"==> New repository created: {repository_name} in organization {organization_name}.")

            # Retrieve GitHub webhook secret from environment variables or SSM
            github_webhook_secret = get_ssm_parameter(os.getenv('GITHUB_WEBHOOK_SECRET_SSM_PARAM', ''))

            # Verify the GitHub webhook signature
            if not verify_signature(event, github_webhook_secret):
                logger.exception("Invalid signature")
                raise ValueError("Invalid signature")

            # Retrieve necessary credentials and IDs from environment variables or SSM
            snyk_token = get_ssm_parameter(os.getenv('SNYK_TOKEN_SSM_PARAM', ''))
            org_id = os.getenv('SNYK_ORG_ID', '')
            integration_id = os.getenv('SNYK_INTEGRATION_ID', '')

            target = {
                "owner": organization_name,
                "name": repository_name,
                "branch": default_branch_name
            }
            exclusion = "fixtures, test"

            # Import the project to Snyk
            response = import_project_to_snyk(
                org_id, integration_id, target, exclusion, snyk_token, repository_name
            )

            # Check the response and raise an exception if the import fails
            if response.status_code != 201:
                logger.error(f"Failed to import repository {repository_name}. Status Code: {response.status_code}, Response: {response.text}.")
                raise RuntimeError(f"Failed to import repository {repository_name}")

            logger.info(f"Successfully imported repository {repository_name}")
            return {
                'statusCode': 200,
                'body': json.dumps(f"Repository {repository_name} imported successfully!")
            }

    except ValueError as e:
        logger.exception("ValueError occurred")
        raise e  # Escalates to Lambda failure

    except ClientError as e:
        logger.exception("ClientError occurred while retrieving Airflow credentials")
        raise e  # Escalates to Lambda failure

    except Exception as e:
        logger.exception("An unexpected error occurred")
        raise e  # Escalates to Lambda failure

#to test
# testingdsf
# 0.0.7
# 0.0.8
# 0.0.9
# 0.0.10