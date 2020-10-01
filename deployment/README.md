This documentation covers the deployment process and the creation of infrastructure.

## Deployment

## Azure setup - creating a new environment

### Get your subscription_id

You will need the subscription_id for the subscription you wish to create the infrastructure on.

You can get this by running:

`$ az account list --output table`

### Create a service principal

This will be used to authenticate the request.

`$ az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/<subscription_id>"`
