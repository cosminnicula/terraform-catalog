# tf-cdk-python

## Prerequisites

- ```aws-cli 2.7.9+```
- ```terraform 1.3.6+```
- ```Node 16.15.0+```
- ```Python 3.8.10+```
- ```Pip 22.3.1+```
- ```Pipenv 2022.11.30+``` (https://pipenv.pypa.io/en/latest/install/#installing-pipenv + https://gist.github.com/planetceres/8adb62494717c71e93c96d8adad26f5c)
- ```cdktf 0.14.3+``` (https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-install -> cdktf-cli)

## Run

- ```pipenv install```
- (only applicable when you create the project for the first time) ```cdktf init --template=python --local``` 
- ```cdktf get```
- ```cdktf synth```
- ```cdktf diff```

# Other useful commands

- ```pipenv run ./main.py``` -> Compile and run the python code.

# Useful links
