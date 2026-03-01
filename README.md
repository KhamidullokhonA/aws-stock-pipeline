# AWS Serverless Stock Market Data Pipeline

## Architecture
![Architecture Diagram](architecture/diagram.png)

## Overview
An end-to-end serverless data pipeline that fetches daily stock market 
data, transforms it, and visualizes it in a dashboard.

## Tech Stack
- **Ingestion:** AWS Lambda + EventBridge
- **Storage:** Amazon S3
- **Transform:** AWS Glue (PySpark)
- **Query:** Amazon Athena
- **Visualization:** Amazon QuickSight

## Pipeline Flow
```
Alpha Vantage API → Lambda → S3 (raw) → Glue → S3 (processed) → Athena → QuickSight
```

## Setup Instructions
1. Clone this repo
2. Get a free API key from [Alpha Vantage](https://www.alphavantage.co)
3. Create two S3 buckets: `stock-raw-yourname` and `stock-processed-yourname`
4. Deploy Lambda function with environment variables
5. Set up EventBridge schedule (cron: `0 21 * * ? *`)
6. Run Glue job to transform data
7. Run Glue Crawler to populate Athena catalog
8. Connect QuickSight to Athena for dashboard

## Dashboard Preview
![QuickSight Dashboard](architecture/dashboard.png)
