import boto3
from datetime import datetime, timedelta

def get_total_metrics_count():
    try:
        # Create CloudWatch client
        cloudwatch = boto3.client('cloudwatch')
        
        # List all metrics with pagination
        paginator = cloudwatch.get_paginator('list_metrics')
        
        total_metrics = 0
        
        # Iterate through all pages
        for page in paginator.paginate():
            metrics = page['Metrics']
            total_metrics += len(metrics)
            
        return total_metrics
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def main():
    count = get_total_metrics_count()
    if count is not None:
        print(f"Total number of metrics: {count}")

if __name__ == "__main__":
    main()
