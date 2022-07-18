import json
import boto3
import time
import re
import datetime
client = boto3.client('cloudtrail')
RequiredParameters = ['EventDataStore', 'QueryStatement']
MaxQueryResults = 100

def lambda_handler(event, context):
    
    # check the input parameters from the function invocation
    for requiredParam in RequiredParameters:
        if requiredParam not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    "MissingParameter": requiredParam
                })
            }
    EventDataStore = event['EventDataStore']
    QueryStatement = event['QueryStatement']
    
    # insert the EventDataStore into the QueryStatement if  used {EventDataStore} in place of hard coding it into the QueryStatement
    # Note: need to do more error handling for this to work. Use QueryFormatParams in the mean time
    #QueryStatement = QueryStatement.format(EventDataStore = event['EventDataStore'])
    
    # further manipulate the QueryStatement if the caller passed in parameters to format into the query 
    # note the format is {m[VariableName]}
    # for example:
    # "QueryStatement": "SELECT eventID, eventName, eventSource, eventTime FROM {m[EventDataStore]} WHERE ...
    # "QueryFormatParams" : {
    #  "EventDataStore": "996f9246-56ad-49eb-bdd2-7276a6d17884",
    #  "invalidParams": "will not be inserted"
    #}
    if 'QueryFormatParams' in event:
        QueryStatement = QueryStatement.format(m=event['QueryFormatParams'])
    
    # start the query
    response = client.start_query(
        QueryStatement=QueryStatement
    )
    QueryId = response['QueryId']
    
    # begin getting query results
    QueryResultRows = []
    NextToken = None
    
    while 1:

        # get the batch of query results
        args = {}
        args['EventDataStore'] = EventDataStore
        args['QueryId'] = QueryId
        args['MaxQueryResults'] = MaxQueryResults
        if NextToken is not None:
            args['NextToken'] = NextToken
        response = client.get_query_results(**args)
        
        # handle if query is not yet finished
        if response['QueryStatus'] != 'FINISHED':
            time.sleep(1)
            continue
        
        # save the results and continue getting results if any
        if 'QueryResultRows' in response:
            QueryResultRows.extend(response['QueryResultRows'])
        if 'NextToken' in response:
            NextToken=response['NextToken']
        else:
            break

    print("CloudTrail Lake Query:", { "TotalResults": len(QueryResultRows), "QueryStatement": QueryStatement, "EventDataStore": EventDataStore } )

    return {
        'statusCode': 200,
        'body': QueryResultRows
    }

