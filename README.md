# SLI CSV Report Generator

## Project Overview
The `sli-csv-report-generator` is a Python-based application designed to query metrics from Thanos, process these metrics into a structured format, and generate an Excel report (`cluster_sli_report.xlsx`). It is also configured to send the generated report via email using Azure Communication Services.

## Installation and Setup
To set up the `sli-csv-report-generator`, follow these steps:
1. Ensure that Python is installed on your system.
2. Clone the repository to your local machine.
3. Install the necessary Python dependencies by running:
   ```
   pip install -r requirements.txt
   ```

## Usage Instructions
Run the script using the following command:
```
python main.py
```
Before running the script, ensure that the relevant environment variables are set. These variables include details such as the Thanos URL, clusters, Excel file name, and Azure email endpoint.

## Docker Image Management
To build, tag, and push the Docker image, use the following commands:
1. Build the Docker image:
   ```
   docker build -t sli_send_report:v2.0.0 .
   ```
2. Tag the Docker image:
   ```
   docker tag sli_send_report:v2.0.0 registry.sli.de/report/sli_send_report:v2.0.0
   ```
3. Push the Docker image to the registry:
   ```
   docker push registry.sli.de/report/sli_send_report:v2.0.0

## Docker Usage
The Docker image for this project is stored in a Harbor registry. To pull the image, a secret has been created in the Kubernetes `monitoring` namespace. If you need to create or update the secret, use the following command::
```
kubectl create secret docker-registry harborimagepullkey \
  --docker-server=registry.sli.de \
  --docker-username=[USERNAME] \
  --docker-password=[PASSWORD] \
  -n monitoring
```
Replace `[USERNAME]` with the actual username.
Replace `[PASSWORD]` with the actual password.

## Helm Chart and Kubernetes Deployment
A separate repository will handle the deployment of the Helm chart, which sets up a Kubernetes cronjob for running this project.

## Additional Information
For more details on the functionality and configuration, please refer to the comments and documentation within the `main.py` script.



