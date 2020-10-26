This documentation covers the deployment process and the creation of infrastructure.

## Deployment

## Azure infrastructure

The infrastructure is managed using [Terraform](https://www.terraform.io/).<br>
The state is stored remotely in encrypted Azure storage.<br>
[Terraform workspaces](https://www.terraform.io/docs/state/workspaces.html) are used to separate environments.

### Creating a new environment

When creating a new staging environment you may wish to build it in the same region as
the current live environment.

#### Configuring the storage backend

The Terraform state is stored remotely in Azure, this allows multiple team members to
make changes and means the state file is backed up. The state file contains
sensitive information so access to it should be restricted, and it should be stored
encrypted at rest.

##### Create a new storage backend

The [Azure tutorial](https://docs.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage) outlines the steps to create a storage account and container for the state file. You will need:

- resource_group_name: The name of the resource group used for the Azure Storage account.
- storage_account_name: The name of the Azure Storage account.
- container_name: The name of the blob container.
- key: The name of the state store file to be created.

##### Create a backend configuration file

Create a new file named `backend.vars` with the following content:

```
resource_group_name  = [the name of the Azure resource group]
storage_account_name = [the name of the Azure Storage account]
container_name       = [the name of the blob container]
key                  = "terraform.tstate"
```

##### Initialise Terraform

This step assumes you have installed Terraform to your local machine.
It will download the required Terraform modules and configure the remote state backend
to use the settings you specified in the previous step.

`$ terraform init -backend-config=backend.vars`

##### (Optional) Create a variables file

Terraform will automatically load a file ending with `.auto.tfvars`.<br>
You can create a file with the following content:

```
location = [Azure region, eg "uksouth"]
prefix = [a name for the project, eg "nhsei"]
ssl_email_address = [an email address used by Letsencrypt]
```

If you do not wish to create the file Terraform will ask you to provide the variables
when you run it.

##### Create the infrastructure

Now Terraform has been initialised you can create a workspace. The workspace name is
included in various resources such as the CDN, database, and load balancer.<br>
Do not use a <prefix>-<workspace> combination that already exists unless you know what
you are doing.

`$ terraform workspace new staging`

Switch to the new workspace<br>
`$ terraform workspace select staging`

Plan the changes<br>
`$ terraform plan`

Terraform will ask you to provide any variables not specified in an `*.auto.tfvars` file.
Now you can run:

`$ terraform apply`

If everything looks good, answer `yes` and wait for the new infrastructure to be created.

#### Connecting to the Kubernetes cluster

The Terraform state file contains the details needed to connect to the cluster.
The output is named `kube_config`.

```j
$ terraform output kube_config > ~/.nhsei-azurek8s
$ export KUBECONFIG=~/.nhsei-azurek8s
```

You should be able to run `kubectl` commands normally.
