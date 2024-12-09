# CloudWatch Logs Query Analyzer

## Description

This Bash script retrieves and analyzes CloudWatch Logs queries using the AWS CLI. It fetches query IDs and strings, then provides detailed statistics for each query.

## Prerequisites

- AWS CLI installed and configured with appropriate permissions
- `jq` command-line JSON processor
- Bash shell

## Usage

1. Make the script executable:

`chmod +x get-log-insights-query-info.sh`


2. Run the script:

`./script_name.sh`


## What the Script Does

1. Retrieves query IDs and strings from CloudWatch Logs using `aws logs describe-queries`.
2. Checks if any queries were found.
3. For each query:
- Displays the Query ID and Query String.
- Fetches and displays statistics for the query using `aws logs get-query-results`.

## Output

The script outputs:
- Query ID
- Query String
- Query Statistics in YAML format

If no queries are found, it will display "No queries found."

## Error Handling

The script includes basic error handling:
- Checks if any queries were returned before processing.
- Uses `set -e` to exit on any command errors (optional, not currently in the script).

## Dependencies

- AWS CLI
- jq

## Notes

- Ensure your AWS CLI is configured with the correct permissions to access CloudWatch Logs.
- The script uses the default AWS CLI profile. Modify if you need to use a specific profile.


