#!/bin/bash

# Get query IDs and strings
query_info=$(aws logs describe-queries --query 'queries[*].{queryId: queryId, queryString: queryString}' --output json)

# Check if we got any queries
if [ -z "$query_info" ] || [ "$query_info" == "[]" ]; then
    echo "No queries found."
    exit 0
fi

# Iterate through each query
echo "$query_info" | jq -c '.[]' | while read -r query; do
    query_id=$(echo $query | jq -r '.queryId')
    query_string=$(echo $query | jq -r '.queryString')
    
    echo "Query ID: $query_id"
    echo "Query String: $query_string"
    echo "Statistics:"
    
    # Get statistics for this query
    aws logs get-query-results --query-id "$query_id" --query 'statistics' --output yaml
    
    echo "------------------------"
done
