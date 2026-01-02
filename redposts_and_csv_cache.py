import boto3
import json
from datetime import datetime
from typing import Dict

class PokemonCache:
    def __init__(self, s3_bucket: str, s3_key: str, dynamodb_table: str):
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.dynamodb_table = dynamodb_table
        self.s3_client = boto3.client('s3')
        self.dynamodb_client = boto3.client('dynamodb')

    def load_csv_data(self) -> Dict[str, Dict[str, list]]:
        response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=self.s3_key)
        data = response['Body'].read().decode('utf-8')
        return json.loads(data)



