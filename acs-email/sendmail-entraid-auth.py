import os

from azure.communication.email import EmailClient
from azure.identity import ClientSecretCredential, ManagedIdentityCredential


ACS_ENDPOINT = "https://<resource-name>.communication.azure.com/"
UAMI_CLIENT_ID = "<managed-identity-client-id>"
AZURE_TENANT_ID = "<tenant-id>"
AZURE_CLIENT_ID = "<service-principal-client-id>"
AZURE_CLIENT_SECRET = "<client-secret>"


def create_credential():
    auth_mode = os.environ.get("ACS_AUTH_MODE", "service-principal")

    if auth_mode == "managed-identity":
        if not UAMI_CLIENT_ID:
            raise RuntimeError(
                "UAMI_CLIENT_ID must identify the UAMI attached to this Azure "
                "compute resource."
            )
        return (
            ManagedIdentityCredential(client_id=UAMI_CLIENT_ID),
            UAMI_CLIENT_ID,
            auth_mode,
        )

    if auth_mode == "service-principal":
        client_id = AZURE_CLIENT_ID
        return (
            ClientSecretCredential(
                tenant_id=AZURE_TENANT_ID,
                client_id=client_id,
                client_secret=AZURE_CLIENT_SECRET,
            ),
            client_id,
            auth_mode,
        )

    raise RuntimeError(
        "ACS_AUTH_MODE must be 'managed-identity' or 'service-principal'."
    )


def main():
    credential, identity_client_id, auth_mode = create_credential()
    client = EmailClient(endpoint=ACS_ENDPOINT, credential=credential)

    try:
        authentication_details = (
            f"Authentication={auth_mode}, Client ID={identity_client_id}"
        )
        message = {
            "senderAddress": "<sender-address>",
            "recipients": {
                "to": [
                    {"address": "<recipient-email-1>"},
                    {"address": "<recipient-email-2>"},
                ]
            },
            "content": {
                "subject": "Test Email on API",
                "plainText": f"Test ACS Email with API through EntraID authentication. {authentication_details}",
                "html": f"""
                <html>
                    <body>
                        <h1>
                            Test ACS Email with API through EntraID authentication.
                        </h1>
                        <p>{authentication_details}</p>
                    </body>
                </html>"""
            },
        }

        poller = client.begin_send(message)
        result = poller.result()
        print("Message sent: ", result)
    finally:
        client.close()
        credential.close()


if __name__ == "__main__":
    main()
