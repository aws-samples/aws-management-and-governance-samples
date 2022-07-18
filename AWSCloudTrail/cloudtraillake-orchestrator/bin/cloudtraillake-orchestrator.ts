#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { CloudtraillakeOrchestratorStack } from '../lib/cloudtraillake-orchestrator-stack';

const app = new cdk.App();
new CloudtraillakeOrchestratorStack(app, 'CloudtraillakeOrchestratorStack');
