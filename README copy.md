# GitHub to Snyk Import Lambda Function

This AWS Lambda function is designed to handle GitHub webhook events and import newly created repositories into Snyk. It verifies the webhook signature to ensure the request is from GitHub and uses the Snyk API to import the repository.

## Features

- **GitHub Webhook Handling**: Listens for repository creation events from GitHub.
- **Signature Verification**: Ensures the request is legitimate by verifying the GitHub webhook signature.
- **Snyk Integration**: Imports the new repository into Snyk using the Snyk API.

## Setup

### Environment Variables

The following environment variables need to be set for the Lambda function to operate correctly:

- `GITHUB_WEBHOOK_SECRET_SSM_PARAM`: The SSM parameter name where the GitHub webhook secret is stored.
- `SNYK_TOKEN_SSM_PARAM`: The SSM parameter name where the Snyk API token is stored.
- `SNYK_ORG_ID`: The Snyk organization ID.
- `SNYK_INTEGRATION_ID`: The Snyk integration ID.

### AWS SSM Parameters

Ensure that the GitHub webhook secret and Snyk API token are stored in AWS SSM Parameter Store, with decryption enabled.

## Usage

Once deployed and configured, the Lambda function will automatically handle repository creation events from GitHub and import them into Snyk.

## Error Handling

- **Invalid Signature**: If the signature verification fails, the function logs an error and raises a `ValueError`.
- **SSM Parameter Retrieval**: If there's an error retrieving parameters from SSM, a `ClientError` is logged and raised.
- **Snyk Import Failure**: If the import to Snyk fails, a `RuntimeError` is logged and raised.