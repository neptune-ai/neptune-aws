# Neptune-AWS integration

Read your Neptune credentials directly from AWS Secrets.

## What will you get with this integration?

* Log, organize, visualize, and compare ML experiments in a single place
* Monitor model training live
* Version and query production-ready models and associated metadata (e.g. datasets)
* Collaborate with the team and across the organization

## What will be logged to Neptune?

* Training code and Git information
* System metrics and hardware consumption
* [Other metadata](https://docs.neptune.ai/logging/what_you_can_log)

## Resources

* [Documentation](https://docs.neptune.ai/integrations/aws/)

## Example

Install Neptune and the integration:

```sh
pip install -U "neptune[aws]"
```

Enable Neptune logging:

```python
from neptune.integrations.aws import init_run

run = init_run(
    secret="neptune-secret",  # Use your secret name here
    region="us-west-1",  # Use the appropriate region here
)
```

## Support

If you got stuck or simply want to talk to us, here are your options:

* Check our [FAQ page](https://docs.neptune.ai/getting_help).
* You can submit bug reports, feature requests, or contributions directly to the repository.
* Chat! In the Neptune app, click the blue message icon in the bottom-right corner and send a message. A real person will talk to you ASAP (typically very ASAP).
* You can just shoot us an email at [support@neptune.ai](mailto:support@neptune.ai).
