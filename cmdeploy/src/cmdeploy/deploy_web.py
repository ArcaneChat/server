import importlib.resources
import os

import pyinfra

from cmdeploy import deploy_website

if pyinfra.is_cli:
    deploy_website()
