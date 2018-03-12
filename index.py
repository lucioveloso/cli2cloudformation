import json
import shlex
import subprocess
from botocore.vendored import requests


def lambda_handler(event, context):

    if 'RequestType' not in event or 'ResourceProperties' not in event:
        send_cfn_response(event, context, "FAILED", {}, "Cannot identify RequestType or ResourceProperties.")
        return

    properties = event['ResourceProperties']

    if "CreateAsDefault" in properties and properties["CreateAsDefault"] == "True":
        command_request_type = "Create"  # Ignore cfn RequestType
    else:
        command_request_type = event['RequestType']

    if command_request_type in properties and properties[command_request_type] != "":
        try:
            output = run_cmd("/var/task/wrapper " + properties[command_request_type])

            if output is None or output == "":
                r = {}
            else:
                r = json.loads(output)

            send_cfn_response(event, context, "SUCCESS", r, "Command Executed.")

        except Exception as e:
            print(e)
            send_cfn_response(event, context, "FAILED", {}, "Failed to execute the command.")
    else:
        send_cfn_response(event, context, "SUCCESS", {}, command_request_type + " has no action.")


def run_cmd(command):
    command = shlex.split("/bin/bash -c '" + command + "'")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, stderr = process.communicate()
    return output


def send_cfn_response(event, context, response_status, response_data, reason):
    response_body = {'Status': response_status,
                    'Reason': 'Log stream name: ' + context.log_stream_name,
                    'PhysicalResourceId': context.log_stream_name,
                    'StackId': event['StackId'],
                    'RequestId': event['RequestId'],
                    'LogicalResourceId': event['LogicalResourceId'],
                    'Data': response_data}
    print("Log Reason: " + reason)
    try:
        requests.put(event['ResponseURL'], data=json.dumps(response_body))
    except Exception as e:
        print(e)
        raise

