import json
import shlex
import subprocess
import requests


def lambda_handler(event, context):
    null_return = json.loads("{}")
    if ('RequestType' not in event or
        'ResourceProperties' not in event):
        sendResponseCfn(event, context, "FAILED", null_return, "Cannot identify RequestType or ResourceProperties." )
        return

    properties = event['ResourceProperties']
    command_request_type = "CliCommand" + event['RequestType']

    # Use action create as default if not action update or delete is specified.
    if("CreateAsDefault" in properties and
        properties["CreateAsDefault"] == "True" and
            (command_request_type not in properties or
             properties[command_request_type] == "")):
        command_request_type = "CliCommandCreate"

    if (command_request_type in properties and
        properties[command_request_type] != ""):
        try:
            print(properties[command_request_type])
            output = run_cmd("/var/task/wrapper " + properties[command_request_type])
            if output is None or output == "":
                print("Null return")
                r = null_return
            else:
                print(output)
                r = json.loads(output)
            sendResponseCfn(event, context, "SUCCESS", r, "Command Executed.")
            print("Command executed.")
        except Exception as e:
            print(e)
            sendResponseCfn(event, context, "FAILED", null_return, "Failed to execute the command.")
    else:
        sendResponseCfn(event, context, "SUCCESS", null_return, command_request_type + " has no action.")

    return True


def run_cmd(command):
    command = shlex.split("/bin/bash -c '" + command + "'")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, stderr = process.communicate()
    return output


def sendResponseCfn(event, context, responseStatus, responseData, reason):
    response_body = {'Status': responseStatus,
                    'Reason': 'Log stream name: ' + context.log_stream_name,
                    'PhysicalResourceId': context.log_stream_name,
                    'StackId': event['StackId'],
                    'RequestId': event['RequestId'],
                    'LogicalResourceId': event['LogicalResourceId'],
                    'Data': responseData}
    print("Log Reason: " + reason)
    try:
        requests.put(event['ResponseURL'], data=json.dumps(response_body))
    except Exception as e:
        print(e)
        raise

