import boto3
import os
import csv
from io import StringIO
from datetime import datetime
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData,text
from sqlalchemy.exc import SQLAlchemyError
from google.oauth2.service_account import Credentials
import gspread
from dotenv import load_dotenv

class GoogleScraper:
    def __init__(self) -> None:
        load_dotenv()
        self.user = os.getenv('db_username')
        self.host = os.getenv('db_host')
        self.password = os.getenv('db_password')
        self.database = os.getenv('db_database')
        self.bucket = os.getenv('bucket')
        self.folder = 'bowtiedlist'
        self.engine = create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}/{self.database}",
            echo=True
        )
        
        # Initialize MetaData
        self.metadata = MetaData()
        
        # Define a table structure here or elsewhere in the class
        self.data_table = Table('bowtiedlist', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('name', String),
                                Column('x_handle', String),
                                Column('categories', String),
                                Column('substack', String),
                                Column('product_service', String))
        
        # Create the table if it doesn't exist, binding metadata to the engine
        self.metadata.create_all(self.engine)


    def get_secret_from_s3(self,bucket_name, key):
        try:
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=bucket_name, Key=key)
            return response['Body'].read().decode('utf-8')
        except Exception as e:
            print(f"Error fetching secret from S3: {e}")
            return None

    def authenticate_google_sheets(self):
        scope = ["https://www.googleapis.com/auth/spreadsheets.readonly",
                 "https://www.googleapis.com/auth/drive.readonly"]
        credentials_json = self.get_secret_from_s3(self.bucket, f"{self.folder}/{os.getenv('cred_key')}")
        with open('/tmp/token.json', 'w') as creds_file:
            creds_file.write(credentials_json)
        creds = Credentials.from_service_account_file("/tmp/token.json", scopes=scope)
        client = gspread.authorize(creds)
        return client

    def get_sheet_data(self, sheet_id, range_name):
        client = self.authenticate_google_sheets()
        sheet = client.open_by_key(sheet_id).worksheet(range_name)
        data = sheet.get_all_records()  # Returns a list of dictionaries.
        enriched_data = []
        # Enrich the data with row numbers starting from 2 (assuming row 1 is the header)
        for index, row in enumerate(data, start=2):
            row['ID'] = index
            enriched_data.append(row)
        return enriched_data

    def update_database(self, data):
        with self.engine.connect() as connection:
            for row in data:
                # Build the upsert SQL statement using the ON CONFLICT clause
                upsert_stmt = text("""
                INSERT INTO bowtiedlist (id, name, x_handle,categories, substack,product_service) VALUES (:id, :name,:handle, :category, :substack , :product)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    x_handle = EXCLUDED.x_handle,
                    categories = EXCLUDED.categories,
                    substack = EXCLUDED.substack,
                    product_service = EXCLUDED.product_service;
                """)
                try:
                    connection.execute(upsert_stmt, {
                        'id': row.get('ID'),
                        'name': row.get('BowTied Member'),
                        'handle': row.get('X Handle'),
                        'category': row.get('Categories (Seperated By Commas)'),
                        'substack': row.get('Substack'),
                        'product': row.get('Products / Serivces')
                    })
                    connection.commit()
                except SQLAlchemyError as e:
                    print("Database error:", e)
                    connection.rollback()

    def dump_to_s3(self, data):
        try:
            # Convert data to CSV format
            csv_buffer = StringIO()
            csv_writer = csv.DictWriter(csv_buffer, fieldnames=data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(data)

            # Generate S3 key with timestamp
            current_time = datetime.utcnow().strftime('%Y-%m-%d_%H-%M')
            s3_key = f"{self.folder}/{current_time}.csv"

            # Upload to S3
            s3_client = boto3.client('s3')
            s3_client.put_object(
                Bucket=self.bucket,
                Key=s3_key,
                Body=csv_buffer.getvalue()
            )
            print(f"Data successfully dumped to s3://{self.bucket}/{s3_key}")
        except Exception as e:
            print(f"Error dumping data to S3: {e}")

    def main(self):
        SHEET_ID = '1cQ0rZ7nDSJlfIPNZ97le52M3mcvZdRsn3t4QAV13Eos'
        RANGE_NAME = 'BowTiedList'
        data = self.get_sheet_data(SHEET_ID, RANGE_NAME)
        self.update_database(data)
        self.dump_to_s3(data)

def lambda_handler(event,context):
    print(event)
    try:
        scraper = GoogleScraper()
        scraper.main() 
        return {
            'status': 200,
            'data': 'Done'
        }
    except Exception as e:
        return {
            'status': 500,
            'error': str(e)
        }

if __name__ == "__main__":
    scraper = GoogleScraper()
    scraper.main()
