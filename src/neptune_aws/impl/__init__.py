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
from typing import Optional

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


def init_run(
    *,
    secret: str,
    region: str,
    project: Optional[str] = None,
    **kwargs,
) -> neptune.Run:
    """Starts a new tracked run and adds it to the top of the runs table.

    Takes the project name and API token from AWS Secrets. A secret with the following fields must be
    defined in AWS Secrets Manager:
    - `project` with the Neptune project name
    - `api_token` with the Neptune API token
    For how to find the above Neptune credentials, see the docs: https://docs.neptune.ai/setup/setting_credentials

    Args:
        secret: Name of the AWS secret holding the Neptune project name and API token.
        region: The AWS region where the AWS secret is defined.
        project: Name of the project where the run should go, in the form "workspace-name/project_name". If not given,
            the project is read from the AWS secret.
        **kwargs: Additional keyword arguments for the `init_run()` method of the Neptune client library.
            For details, see the API reference: https://docs.neptune.ai/api/neptune#init_run

    Returns:
        Run object that is used to manage the tracked run and log metadata to it.

    Example:
        Creating a new run:

        >>> from neptune.new.integrations.aws import init_run  # doctest: +SKIP
        >>> run = init_run(
        ...     secret="neptune-secret",  # Use your secret name here
        ...     region="us-west-1",       # Use the appropriate region here
        ... )  # doctest: +SKIP
    """

    # See:
    # https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_cache-python.html
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/secrets-manager.html

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region)
    get_secret_value_response = client.get_secret_value(SecretId=secret)
    secret = json.loads(get_secret_value_response["SecretString"])

    if project is None:
        project = secret["project"]

    run = neptune.init_run(
        project=project,
        api_token=secret["api_token"],
        **kwargs,
    )
    run[INTEGRATION_VERSION_KEY] = __version__

    return run
