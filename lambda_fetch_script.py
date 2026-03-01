import sys
import json
import boto3
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import Row
from pyspark.sql.functions import col

# Setup
sc    = SparkContext()
glue  = GlueContext(sc)
spark = glue.spark_session

# Config — update these to your bucket names!
RAW_BUCKET       = "stock-raw-khamidullokhon"
PROCESSED_BUCKET = "stock-processed-khamidullokhon"
SYMBOL           = "AAPL"

# Read raw JSON from S3
s3     = boto3.client('s3')
prefix = f"raw/{SYMBOL}/"
objs   = s3.list_objects_v2(Bucket=RAW_BUCKET, Prefix=prefix)

rows = []
for obj in objs.get('Contents', []):
    body = s3.get_object(Bucket=RAW_BUCKET, Key=obj['Key'])['Body'].read()
    data = json.loads(body)
    ts   = data.get("Time Series (Daily)", {})
    for date, values in ts.items():
        rows.append(Row(
            date   = date,
            open   = float(values["1. open"]),
            high   = float(values["2. high"]),
            low    = float(values["3. low"]),
            close  = float(values["4. close"]),
            volume = int(values["5. volume"]),
            symbol = SYMBOL
        ))

# Create DataFrame and save as Parquet
df = spark.createDataFrame(rows)
df.write.mode("overwrite").partitionBy("symbol") \
  .parquet(f"s3://{PROCESSED_BUCKET}/processed/stocks/")

print(f"✅ Saved {df.count()} rows to processed bucket!")