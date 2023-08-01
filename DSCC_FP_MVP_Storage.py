from io import StringIO
import boto3
import json
import pandas as pd
from smart_open import smart_open

def store_df_into_s3(dataframe, file_name):
    # Load credentials from configuration file
    with open("DSCC-FP-MVP-Configuration.json") as config_file:
        config = json.load(config_file)

    client = boto3.client('s3', aws_access_key_id=config["aws_access_key_id"],aws_secret_access_key=config["aws_secret_access_key"])
    
    # Convert DataFrame to CSV format
    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer, index=False)

    client.put_object(Body=csv_buffer.getvalue(), Bucket='dsccfpmvpstorage', Key='{}.csv'.format(file_name))

    print('{} CSV file saved successfully to S3 bucket'.format(file_name))

def retrieve_data_from_s3(file_name):
    
    # Load credentials from configuration file
    with open("DSCC-FP-MVP-Configuration.json") as config_file:
        config = json.load(config_file)

    client = boto3.client('s3', aws_access_key_id=config["aws_access_key_id"],aws_secret_access_key=config["aws_secret_access_key"])

    s3_object = client.get_object(Bucket='dsccfpmvpstorage', Key='{}.csv'.format(file_name))
    

    body = s3_object['Body']
    print('Successfully retrieved {} Data from Storage'.format(file_name))

    df = pd.read_csv(body)

    return df
