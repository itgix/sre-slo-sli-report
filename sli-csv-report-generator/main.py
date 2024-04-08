import os
import base64
import pandas as pd
import requests
from openpyxl.utils import get_column_letter
from azure.communication.email import EmailClient
from azure.identity import DefaultAzureCredential

# Environment variables
THANOS_URL = os.environ.get("THANOS_URL", "http://cluster03-thanos-query-frontend.thanos.svc.cluster.local:9090/api/v1/query")
CLUSTERS = os.environ.get("CLUSTERS", "cluster01, cluster02, cluster03, cluster04").split(',')
EXCEL_FILE_NAME = os.environ.get("EXCEL_FILE_NAME", "/app/cluster_sli_report.xlsx")
AZURE_EMAIL_ENDPOINT = os.environ.get("AZURE_EMAIL_ENDPOINT", "https://email-send-the-slo.europe.communication.azure.com/")

def query_thanos(url, query):
    response = requests.get(url, params={'query': query})
    results = response.json()['data']['result']
    return results

def create_dataframe(results, cluster_name):
    data = []
    for result in results:
        instance = result['metric']['instance']
        sli_namespace = result['metric'].get('sli_namespace', '')
        value = min(float(result['value'][1]), 100.0)
        data.append([instance, cluster_name, sli_namespace, value])
    return pd.DataFrame(data, columns=['instance', 'cluster', 'sli_namespace', 'value'])

def autofit_column_widths(worksheet):
    for col in worksheet.columns:
        max_length = 0
        column = get_column_letter(col[0].column)
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column].width = adjusted_width

def main():
    all_data_frames = []
    for cluster in CLUSTERS:
        query = f'avg_over_time(sum by (instance,sli_namespace,cluster) (probe_success{{cluster="{cluster}", sli_namespace!=""}})[30d:5m]) * 100'
        results = query_thanos(THANOS_URL, query)
        df = create_dataframe(results, cluster)
        all_data_frames.append(df)

    all_data = pd.concat(all_data_frames, ignore_index=True)

    with pd.ExcelWriter(EXCEL_FILE_NAME, engine='openpyxl') as writer:
        all_data.to_excel(writer, sheet_name='All Clusters', index=False)
        workbook = writer.book
        autofit_column_widths(workbook['All Clusters'])

    # Email sending logic
    client = EmailClient(AZURE_EMAIL_ENDPOINT, DefaultAzureCredential())
    with open(EXCEL_FILE_NAME, 'rb') as file:
        file_bytes_b64 = base64.b64encode(file.read())

    message = {
        "senderAddress": "DoNotReply@123456789-abcd-0099887766.azurecomm.net",
        "recipients": {
            "to": [
                {"address": "receiver2@itgix.com"},
                {"address": "receiver2@itgix.com"},
                {"address": "receiver3@gmail.com"}
            ],
        },
        "content": {
            "subject": "SLI Report for URL Uptime",
            "plainText": "SLI Report for the past 30 days. Please find the attached Excel file.",
        },
        "attachments": [
            {
                "name": os.path.basename(EXCEL_FILE_NAME),
                "contentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "contentInBase64": file_bytes_b64.decode()
            }
        ]
    }

    poller = client.begin_send(message)
    result = poller.result()
    print(result)

if __name__ == "__main__":
    main()
