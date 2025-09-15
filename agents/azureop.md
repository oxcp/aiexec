## Description
Azure AI Agent to assist people for Azure operations.

## Features
- Generate script/code for Azure resource management and workload deployment
- Use function calls to save and execute script/code

## Source
- [Source Code](./azureop.py)

## Usage
- [Usage video](https://oxcp.github.io/ainotes/azureopagent.html)

## Sample Prompts
```
[Users:]
With specified docker image which implements a web page, help to create Azure Container Apps to run the docker image and host the web page. You just create the minimum requested resource to finish the task. There is no need to use Log Analytics workspace.

[Assistant:]
To create the Azure Container App and host a web page using a specified Docker image, I'll need the following details from you:

1. **Docker Image Name** (e.g., `myrepo/myimage:latest`).
2. **Resource Group Name** (e.g., `my-resource-group`).
3. **Region** (e.g., `eastus`).
4. **Container App Name** (e.g., `my-container-app`).

Can you provide these details?

[Users:]
This is the info you may need to perform the task: \
azure region: eastus \
azure group name: acapoc \
azure container apps environment name: aca-env \
azure container apps name: aca01 \
subscription ID: <your_subscription_id> \
Client ID: <your_client_id> \
Client secret: <your_client_secret> \
tenant ID: <your_tenant_id> \
container image: <your_container_image> \
container registry username: <your_container_registry_username> \
container registry password: <your_container_registry_password> \
container expose port:<your_container_expose_port> \
After finish the task, return the URL of the deployed Azure Container Apps which points to the web page

[Assistant:]
Assistant: I will create Azure Container Apps as per the provided details using the Azure CLI. Here's the plan:

1. **Login to Azure** using the service principal credentials you provided.
2. **Create the Container Apps environment** named `aca-env`.
3. **Deploy the Container App** named `aca01` with the provided Docker image `gckacr.azurecr.io/hellok8s:v0`.
4. Set up to expose port `80` in the container app.

Finally, I will output the public URL of the deployed container app pointing to the hosted web page.

Here's the script:

```bash
#!/bin/bash

# Variables
SUBSCRIPTION_ID="<your_subscription_id>"
CLIENT_ID="ea5...
...
...
...
Azure Container App has been successfully deployed!
Access the web page at: http://aca01.happygrass-10f2e007.eastus.azurecontainerapps.io

Assistant: The Azure Container App has been successfully deployed. You can access the hosted web page at:

**[http://aca01.happygrass-10f2e007.eastus.azurecontainerapps.io](http://aca01.happygrass-10f2e007.eastus.azurecontainerapps.io)**

Let me know if there is anything else you need assistance with!

[Users:]
exit

```
