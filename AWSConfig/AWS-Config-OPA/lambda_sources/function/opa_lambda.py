import os
import json
import boto3
import logging
from botocore.exceptions import ClientError
import subprocess
import tempfile


logging_level = os.environ['LOGGING_LEVEL']

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)
handler = logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s')
handler.setFormatter(formatter)
logger.propagate = False


class Opa(object):
    def __init__(self, input_file_name, policy_package_name, rule_to_eval) -> None:
        try:
            self.input_file_path = input_file_name
            self.query = '"data.{}.{}"'.format(policy_package_name,
                                               rule_to_eval)
        except Exception as e:
            logger.error(e)
            raise
        else:
            logger.info('OPA input query: {}'.format(self.query))

    def eval_compliance(self, policy_file_path) -> bool:
        try:
            command = 'opa eval -d {} -i {} {}'.format(policy_file_path,
                                                       self.input_file_path,
                                                       self.query)
            logger.debug('OPA eval command: {}'.format(command))
            output = run_process(command)
            for result in output['result']:
                for _ in result['expressions']:
                    logger.debug('OPA output query: {}'.format(_['text']))
                    if '"{}"'.format(_['text']) == self.query:
                        compliance = _['value']
                        logger.debug(
                            'OPA output compliance: {}'.format(compliance)
                        )
                        logger.info('OPA compliance evaluated successfully')
                        return compliance
        except Exception as e:
            logger.error(e)
            raise


class Config(object):
    def __init__(self, event) -> None:
        self.config_event = json.loads(event['invokingEvent'])
        self.config_item = self.config_event['configurationItem']
        logger.debug('Config Item: {}'.format(self.config_item))
        self.result_token = event['resultToken']
        logger.debug('Result token: {}'.format(self.result_token))
        self.input_parameters = json.loads(event['ruleParameters'])
        logger.debug('Config rule parameters: {}'.format(self.input_parameters))
        self.message_type = self.config_event['messageType']
        logger.debug('Config message type: {}'.format(self.message_type))
        self.resource_id = self.config_item['resourceId']
        logger.debug('AWS resource id: {}'.format(self.resource_id))
        self.resource_status = self.config_item['configurationItemStatus']
        logger.debug('AWS resource status: {}'.format(self.resource_status))
        self.client = boto3.client('config')

    def set_compliance(self, compliance) -> None:
        evaluation = {
            'Annotation': 'Setting compliance based on OPA policy evaluation.\n',
            'ComplianceResourceType': self.config_item['resourceType'],
            'ComplianceResourceId': self.config_item['resourceId'],
            'OrderingTimestamp': self.config_item['configurationItemCaptureTime']
        }
        if self.resource_status == 'ResourceDeleted':
            evaluation['ComplianceType'] = 'NOT_APPLICABLE'
            msg = 'Resource {} is deleted, setting Compliance Status to ' \
                  'NOT_APPLICABLE.'.format(self.resource_id)
            logger.info(msg)
            evaluation['Annotation'] += msg
        elif compliance:
            evaluation['ComplianceType'] = 'COMPLIANT'
            msg = 'Resource {} is compliant'.format(self.resource_id)
            logger.info(msg)
            evaluation['Annotation'] += msg
        else:
            evaluation['ComplianceType'] = 'NON_COMPLIANT'
            msg = 'Resource {} is NOT compliant'.format(self.resource_id)
            logger.info(msg)
            evaluation['Annotation'] += msg
        try:
            self.client.put_evaluations(Evaluations=[evaluation],
                                        ResultToken=self.result_token)
        except ClientError as e:
            logger.error(
                'Config service PUT Evaluation failed with error: {}'.format(
                    e.response['Error']['Message']
                )
            )


def download_s3_obj(bucket, prefix, object_key) -> str:
    try:
        s3 = boto3.resource('s3')
        object_path = ''.join([prefix, object_key])
        obj = s3.Object(bucket, object_path)
        obj_body = obj.get()['Body'].read().decode('utf-8')
    except ClientError as e:
        logger.error('S3 download file failed with: {}'.format(
            e.response['Error']['Message']))
    except Exception as e:
        logger.error(e)
    else:
        return obj_body


def run_process(command):
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            shell=True,
            encoding='utf-8'
        )
    except BrokenPipeError as e:
        logger.error('Process failed with {}'.format(e))
        raise
    except Exception as e:
        logger.error('Process failed with {}'.format(e))
        raise
    else:
        output = json.loads(process.stdout)
        logger.debug('Shell command stdout: {}'.format(output))
        return output


def get_tempfile(content):
    try:
        tf = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8')
        tf.write(content)
        tf.seek(0)
    except Exception as e:
        logger.error('Creating tempfile failed with {}'.format(e))
        raise
    else:
        return tf


def lambda_handler(event, context):
    try:
        logger.debug('Lambda event: {}'.format(event))
        config = Config(event)
        logger.info('Config input processed')

        input_file = get_tempfile(json.dumps(config.config_item))
        logger.info('OPA input file created')
        logger.debug('Name of the input file is: {}'.format(input_file.name))

        policy_file = get_tempfile(download_s3_obj(
            config.input_parameters['ASSETS_BUCKET'],
            config.input_parameters['REGO_POLICIES_PREFIX'],
            config.input_parameters['REGO_POLICY_KEY']
        ))
        logger.info('OPA policy file created')
        logger.debug('Name of the policy file is: {}'.format(policy_file.name))

        opa = Opa(
            input_file.name,
            config.input_parameters['OPA_POLICY_PACKAGE_NAME'],
            config.input_parameters['OPA_POLICY_RULE_TO_EVAL']
        )

        config.set_compliance(opa.eval_compliance(policy_file.name))
    finally:
        try:
            input_file.close()
            policy_file.close()
        except UnboundLocalError as e:
            logger.error(
                'Tempfiles not created. Nothing to close. Error: {}'.format(e)
            )
        else:
            logger.info("Temp files have been closed")
