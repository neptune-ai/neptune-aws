#
# Copyright (c) 2023, Neptune Labs Sp. z o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json

import boto3

try:
    # neptune-client=0.9.0+ package structure
    import neptune.new as neptune
except ImportError:
    # neptune-client>=1.0.0 package structure
    import neptune

from neptune_aws.impl.version import __version__

__all__ = ["__version__", "init_run"]

INTEGRATION_VERSION_KEY = "source_code/integrations/aws"


def init_run(secret, region, **kwargs):
    """Starts a new tracked run taking project name and API token from AWS Secrets and adds it to the top of the runs
    table.

    The AWS Secret needs to have the two fields `project` with project name and `api_token` with Neptune API token.

    Args:
        secret: Name of the AWS Secret holding the Neptune project name and API token.
        region: The AWS region where the AWS Secret is defined.
        **kwargs: Additional parameters of the `init_run` method from Neptune client.

    Returns:
        Run object that is used to manage the tracked run and log metadata to it.

    Examples:

        Creating a new run:

        >>> from neptune.new.integrations.aws import init_run
        >>> run = init_run(
        ...     secret="neptune-secret",  # Use your secret name here
        ...     region="us-west-1",       # Use appropriate region here
        ... )

    For more, see the API reference:
    https://docs.neptune.ai/api/neptune#init_run
    """

    # See:
    # https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_cache-python.html
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/secrets-manager.html

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region)
    get_secret_value_response = client.get_secret_value(SecretId=secret)
    secret = json.loads(get_secret_value_response["SecretString"])

    run = neptune.init_run(
        project=secret["project"],
        api_token=secret["api_token"],
        **kwargs,
    )
    run[INTEGRATION_VERSION_KEY] = __version__

    return run
