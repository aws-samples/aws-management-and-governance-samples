#*
#* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#* SPDX-License-Identifier: MIT-0
#*
#* Permission is hereby granted, free of charge, to any person obtaining a copy of this
#* software and associated documentation files (the "Software"), to deal in the Software
#* without restriction, including without limitation the rights to use, copy, modify,
#* merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#* permit persons to whom the Software is furnished to do so.
#*
#* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#* INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#* PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#* HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#* OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#* SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#*

def lambda_handler(event, context):
    misconfigurations = get_keyvalue_misconfigurations(IDEAL_FILE_S3_KEY, CONFIG_SETTINGS_GROUP, CONFIG_MGMT_ATHENA_TABLE, CUSTOM_QUERIES)

    if misconfigurations:
        response = invoke_reporting_lambda(misconfigurations, context)

        print(response)
        return misconfigurations
    else:
        return []

def get_keyvalue_misconfigurations(IDEAL_FILE_S3_KEY, CONFIG_SETTINGS_GROUP, CONFIG_MGMT_ATHENA_TABLE, CUSTOM_QUERIES):

    aggregatedResults = []
    s3Client = boto3.resource('s3')
    athenaClient = boto3.client('athena')

    # Load ideal JSON from S3
    idealConfig = get_ideal_config_file_from_s3(os.environ["IDEAL_FILE_S3_BUCKET"], IDEAL_FILE_S3_KEY, s3Client)

    # Check inventory against ideal using query builder
    query = compare_with_ideal_config(idealConfig, CONFIG_MGMT_ATHENA_TABLE, CONFIG_SETTINGS_GROUP)
    aggregatedResults += query_Athena_and_parse_response(query, athenaClient)

    # Check manually written queries, if any
    for query in CUSTOM_QUERIES:
        aggregatedResults += query_Athena_and_parse_response(query, athenaClient)

    print(aggregatedResults)

    return aggregatedResults


def compare_with_ideal_config(idealConfig, CONFIG_MGMT_ATHENA_TABLE, CONFIG_SETTINGS_GROUP):

    query_list = []
    aggregated_query = ""

    # Gets top level key, usually "common" for our use case. Use different top-level keys to
    # auto-build queries using a different builder function.
    for category in idealConfig:
        # Next level of keys, if statements determine whether it's a string and a structure after, or
        # just a string : value
        for key, subkey_or_value in idealConfig[category].items():
            #subkey_or_value is either the subkey or value, depending on the case below
            if isinstance(subkey_or_value, str):
                #subkey_or_value is the value in this block
                # builds the query using the keys and values found when parsing
                # adds query to a list to be concatenated later
                query = build_query(key, None, subkey_or_value, CONFIG_MGMT_ATHENA_TABLE, CONFIG_SETTINGS_GROUP)
                query_list.append(query)

            elif isinstance(subkey_or_value, dict):
                #subkey_or_value is subkey in this block
                # json looks like string : {string, value} so this for loop parses that
                for subkey, value in idealConfig[category][key].items():
                    # same as above loop
                    query = build_query(key, subkey, value, CONFIG_MGMT_ATHENA_TABLE, CONFIG_SETTINGS_GROUP)
                    query_list.append(query)

    # need the length of the list because we can't loop through and add UNION to every query_list
    # because the last query in the list will not need UNION at the end
    list_length = len(query_list)
    counter = 0
    # concatenates queries and adds UNION in between
    while counter < list_length:
        aggregated_query += query_list[counter]
        if counter != list_length - 1:
            aggregated_query+= " UNION "
        counter += 1

    return aggregated_query

def build_query(key, subkey, value, CONFIG_MGMT_ATHENA_TABLE, CONFIG_SETTINGS_GROUP):
    if "{condition:" in value:
        #<set condition to specified value in ideal config file>
    elif isinstance(value, list):
        condition = " NOT IN "
    else:
        condition = "!=" #default conditional

    if "{*}" in value: #used as wildcard in ideal config file
        value = value.replace("{*}", "%")
        condition = " NOT LIKE "

    if subkey:
        if "{*}" in value:
            value = value.replace("{*}", "%")
            condition = " NOT LIKE "

        if "{*}" in subkey:
            subkey = subkey.replace("{*}", "%")
            subkeyCondition = " LIKE "
        else:
            subkeyCondition = "="
        if subkey == '{*}': #use indicates "for any subkey, value should be..."
            subkey = None

    #append the correct query statement based on values provided
    if subkey is None and not isinstance(value, list):
        # print("entered")
        query = "SELECT * FROM \"paas-config-mgmt\".\"{}\" WHERE settingsgroup='{}' AND key='{}' AND value{}'{}'".format(
         CONFIG_MGMT_ATHENA_TABLE, CONFIG_SETTINGS_GROUP, key, condition, value
         )
    elif subkey is None and isinstance(value, list):
        query = "SELECT * FROM \"paas-config-mgmt\".\"{}\" WHERE settingsgroup='{}' AND key='{}' AND value {} (".format(
         CONFIG_MGMT_ATHENA_TABLE, CONFIG_SETTINGS_GROUP, key, condition
         )
        query += ', '.join(map(lambda x: "'" + x + "'", value)) + ")"
    elif subkey is not None and isinstance(value, list):
        query = "SELECT * FROM \"paas-config-mgmt\".\"{}\" WHERE settingsgroup='{}' AND key='{}' AND subkey{}'{}' AND value{} (".format(
             CONFIG_MGMT_ATHENA_TABLE, CONFIG_SETTINGS_GROUP, key, subkeyCondition, subkey, condition
             )
        query += ', '.join(map(lambda x: "'" + x + "'", value)) + ")"
    else:
        query = "SELECT * FROM \"paas-config-mgmt\".\"{}\" WHERE settingsgroup='{}' AND key='{}' AND subkey{}'{}' AND value{}'{}'".format(
             CONFIG_MGMT_ATHENA_TABLE, CONFIG_SETTINGS_GROUP, key, subkeyCondition, subkey, condition, value
             )

    return query
