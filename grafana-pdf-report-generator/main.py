import os
import base64
from azure.communication.email import EmailClient
from azure.identity import DefaultAzureCredential

GRAFANA_API_KEY = os.environ.get("GRAFANA_API_KEY")
GRAFANA_HOSTNAME = os.environ.get("GRAFANA_HOSTNAME")
GRAFANA_DASHBOARD = os.environ.get("GRAFANA_DASHBOARD")
GRAFANA_CMD_TS = os.environ.get("GRAFANA_CMD_TS", "from=now-30d")
GRAFANA_CMD_VAR_CLUSTER = os.environ.get("GRAFANA_CMD_VAR_CLUSTER", "var-cluster=cluster01")
GRAFANA_CMD_O = os.environ.get("GRAFANA_CMD_O", "/app/out.pdf")
GRAFANA_SSL_CHECK = os.environ.get("GRAFANA_SSL_CHECK", "false")
GRAFANA_PROTO = os.environ.get("GRAFANA_PROTO", "https://")
AZURE_EMAIL_ENDPOINT = os.environ.get("AZURE_EMAIL_ENDPOINT")
def main():
    cmd = '/usr/local/bin/grafana-reporter -grid-layout=1 -cmd_enable=1'
    cmd += f' -cmd_apiKey {GRAFANA_API_KEY}'
    cmd += f' -ip {GRAFANA_HOSTNAME}'
    cmd += f' -cmd_dashboard {GRAFANA_DASHBOARD}'
    cmd += f' -cmd_ts "{GRAFANA_CMD_TS}&{GRAFANA_CMD_VAR_CLUSTER}"'
    cmd += f' -cmd_o {GRAFANA_CMD_O}'
    cmd += f' -ssl-check={GRAFANA_SSL_CHECK}'
    cmd += f' -proto={GRAFANA_PROTO}'

    # Debugging print
    print("Generated Command:")
    print(cmd)

    os.system(cmd)


    client = EmailClient(AZURE_EMAIL_ENDPOINT, DefaultAzureCredential())

    # Read the PDF file in binary mode and encode it in Base64
    with open(GRAFANA_CMD_O, 'rb') as file:
        file_bytes_b64 = base64.b64encode(file.read())

    message = {
        "senderAddress": "DoNotReply@537221b4-59af-46c0-aebd-793c3919dd98.azurecomm.net",
        "recipients":  {
            "to": [
                {"address": "receiver1@gmail.com"},
                {"address": "receiver2@itgix.com"},
                {"address": "receiver3@itgix.com"} 
            ],
        },
        "content": {
            "subject": "SLI Report for URL Uptime",
            "plainText": "SLI Report for the past 30 days. Please find the attached PDF.",
        },
        "attachments": [ 
            {
                "name": "SLI-report.pdf",
                "contentType": "application/pdf",
                "contentInBase64": file_bytes_b64.decode()
            }
        ]
    }

    poller = client.begin_send(message)
    result = poller.result()

    print(result)


if __name__ == "__main__":
    main()
