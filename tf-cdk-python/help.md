- Compile:
  ```pipenv run ./main.py```  Compile and run the python code.

- Synthesize:
  ```cdktf synth [stack]```   Synthesize Terraform resources to cdktf.out/

- Diff:
  ```cdktf diff [stack]```    Perform a diff (terraform plan) for the given stack

- Deploy:
  ```cdktf deploy [stack]```  Deploy the given stack

- Destroy:
  ```cdktf destroy [stack]``` Destroy the given stack

See also https://cdk.tf/modules-and-providers