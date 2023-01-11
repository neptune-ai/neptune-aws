# Neptune + Amazon SageMaker integration

This is an integration that exposes the `init_run` function that reads the Neptune API token and project name from
AWS Secrets Manager instead of environment variables.

```python
from neptune.new.integrations.aws import init_run 

run = init_run(
    secret="neptune-secret",  # Use your secret name here
    region="us-west-1",       # Use appropriate region here
) 
```
