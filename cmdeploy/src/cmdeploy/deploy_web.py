import importlib.resources
import os

import pyinfra

from cmdeploy import deploy_website


def main():
    config_path = os.getenv(
        "CHATMAIL_INI",
        importlib.resources.files("cmdeploy").joinpath("../../../chatmail.ini"),
    )
    deploy_website(config_path)


if pyinfra.is_cli:
    main()
