from azure.communication.email import EmailClient

def main():
    try:
        connection_string = "endpoint=https://<resource-name>.communication.azure.com/;accesskey=<access-key>"
        client = EmailClient.from_connection_string(connection_string)

        authentication_details = (
            f"Authentication=Connection String: {connection_string}"
        )

        message = {
            "senderAddress": "<sender-address>",
            "recipients": {
                "to": [{"address": "<recipient-email>"}]
            },
            "content": {
                "subject": "Test Email on API",
                "plainText": "Test ACS Email with API through Connection String authentication.",
                "html": f"""
				<html>
					<body>
						<h1>
							Test ACS Email with API through Connection String authentication.
						</h1>
                        <p>{authentication_details}</p>
					</body>
				</html>"""
            },
            
        }

        poller = client.begin_send(message)
        result = poller.result()
        print("Message sent: ", result)

    except Exception as ex:
        print(ex)

main()
