import os
from google.cloud import bigquery, bigquery_datatransfer

bq_client = bigquery.Client()
dts_client = bigquery_datatransfer.DataTransferServiceClient()

PROJECT_ID = os.getenv("BQ_PROJECT_ID")
PROJECT_LOCATION = os.getenv("BQ_PROJECT_LOCATION")
QUERIES_DIR = os.getenv("QUERIES_DIR")

def create_scheduled_query(schedule:str):
    parent = dts_client.common_location_path(project=PROJECT_ID, location=PROJECT_LOCATION)
    query_files = os.listdir(QUERIES_DIR)

    for file in query_files:
        if file.endswith(".sql"):
            with open("{DIR}/{FILE}".format(DIR=QUERIES_DIR, FILE=file), "r") as f:
                query = f.read()

            dts_config = bigquery_datatransfer.TransferConfig(
                display_name=os.path.splitext(file)[0],
                data_source_id="scheduled_query",
                params={"query": query},
                schedule=schedule
            )
            
            dts_scheduler = dts_client.create_transfer_config(
                bigquery_datatransfer.CreateTransferConfigRequest(
                    parent=parent,
                    transfer_config=dts_config
                )
            )