# cli2cloudformation
cli2cloudformation is an AWS lambda that provides the possibility to execute CLI Commands inside CloudFormation stacks.a

You can use cli2cloudformation to get all kind of information from your environment, for example:
* Get the AMI ID by Name (In this case it will work in all the regions).
* Get the default vpc, subnets or whatever your need.
* Sync bucket during a CloudFormation execution.
* Specify customized actions to executed in each CloudFormation operation: Create / Update / Delete.

## Get Started

```
git clone https://github.com/lucioveloso/cli2cloudformation.git
cd cli2cloudformation
npm install -g serverless
npm install serverless-python-requirements
sls deploy
```

After that, you're ready to enjoy the CLI in Cloudformation:

### Example getting the AMI ID in any region:

```
"imageIdNameBased": {
        "Type": "Custom::cli2cfnLambda",
        "Properties": {
          "ServiceToken": "arn:aws:lambda:eu-west-1:123456789012:function:cli2cloudformation-dev-cli",
          "Create": "ec2 describe-images --filters 'Name=name,Values=amzn-ami-hvm-2017.03.0.20170417-x86_64-gp2' --query 'Images[0]'"
	}
}
```

Than, in any part of your template you can get this result just including:

```
"Fn::GetAtt" : ["imageIdNameBased", "ImageId"]
```
