#!/bin/bash

# To reduce output of cdk synth, delete below from synth results.
# - delete Parameters.BootstrapVersion
# - delete Rules.CheckBootstrapVersion
# - no-version-reporting
# - path-metadata false
# - asset-metadata false
#
# Usage:
#   (Run at cdk root directory)
#   bash cdk_synth_simple.sh
# Output:
#   tmp.yaml is created and shown.
#
# Note: Used only for one stack cdk.

# Check if in the cdk root
if [ ! -f cdk.json ]; then
	  printf "\n--app is required either in command-line, in cdk.json or in ~/.cdk.json.\n"
	    exit
fi

FILE="tmp.yaml"

cdk synth --no-version-reporting --path-metadata false --asset-metadata false | \
	yq 'del( .Parameters.BootstrapVersion )' | \
	yq 'del( .Rules.CheckBootstrapVersion )' | \
	yq 'del(.. | select(tag == "!!map" and length == 0))' > $FILE

cat $FILE
