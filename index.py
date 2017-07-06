import json
import shlex
import subprocess
import requests

def lambda_handler(event, context):
    nullReturn = json.loads("{}")
    if ('RequestType' not in event or
        'ResourceProperties' not in event):
        sendResponseCfn(event, context, "FAILED", nullReturn, "Cannot identify RequestType or ResourceProperties." )
        return

    properties = event['ResourceProperties'];

    if ("CreateAsDefault" in properties and
        properties['CreateAsDefault'] == "False"):
        commandRequestType = "CliCommand" + event['RequestType'];
    else:
        commandRequestType = "CliCommandCreate"

    if (commandRequestType in properties and
        properties[commandRequestType] != ""):
        try:
            output = run_cmd("wrapper " + properties[commandRequestType])
            r = nullReturn if output is None else json.loads(output)
            sendResponseCfn(event, context, "SUCCESS", r, "Command Executed.")
        except Exception as e:
            sendResponseCfn(event, context, "FAILED", nullReturn, "Failed to execute the command.")
    else:
        sendResponseCfn(event, context, "SUCCESS", nullReturn, commandRequestType + " has no action.")

    return True

def run_cmd(command):
    command = shlex.split("/bin/bash -c '" + command + "'")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, stderr = process.communicate()
    return output

def sendResponseCfn(event, context, responseStatus, responseData, reason):
    responseBody = {'Status': responseStatus,
                    'Reason': 'Log stream name: ' + context.log_stream_name,
                    'PhysicalResourceId': context.log_stream_name,
                    'StackId': event['StackId'],
                    'RequestId': event['RequestId'],
                    'LogicalResourceId': event['LogicalResourceId'],
                    'Data': responseData}
    print("Log Reason: " + reason)
    try:
        req = requests.put(event['ResponseURL'], data=json.dumps(responseBody))
    except Exception as e:
        print(e)
        raise
