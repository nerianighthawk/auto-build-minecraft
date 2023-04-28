#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Yataka Neria

import subprocess
import os
import sys
import logging
import yaml
import json
from random import randrange
from dataclasses import dataclass, asdict
from functools import reduce


@dataclass
class ExtraVars:
    # create, start, stop, delete, download
    exec_type: str
    temp_dir: str
    gcp_project: str
    gcp_cred_file: str
    region: str
    resources_path: str
    dockerfile_path: str
    project_name: str
    hostname: str
    user_name: str
    zone: str


@dataclass
class MSABContext:
    # msab execute directory
    exec_dir: str
    # msab install directory
    install_dir: str
    # logger
    logger: logging.Logger


class MSABExecption(Exception):
    pass


def initialize_context() -> MSABContext:
    # path of msab execute directory
    exec_dir = os.getcwd()
    # path of msab install directory
    install_dir = os.path.join(os.path.dirname(__file__))

    # make temp directory
    os.makedirs('.msab', exist_ok=True)

    # setting of logging
    logger = logging.getLogger('msab')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s - %(message)s')
    # Set the file handler to output logs to test.log
    file_handler = logging.FileHandler('.msab/msab.log')
    # Individually set the log level output to test.log to ERROR
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)

    # Set StreamHandler for output to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # add respective handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return MSABContext(exec_dir, install_dir, logger)


def initialize_extra_vars(context: MSABContext, args: list) -> ExtraVars:
    exec_type = args[1]
    temp_dir = f'{context.exec_dir}/.msab'
    with open(f'{context.exec_dir}/msab.yml', 'r') as yml:
        config = yaml.safe_load(yml)
    region = config['zone'][:-2]
    gcp_cred_file = f'{context.exec_dir}/gcp_credential.json'
    with open(gcp_cred_file, 'r') as j:
        gcp = json.load(j)
    gcp_project = gcp['project_id']
    resources_path = f'{context.exec_dir}/resources'
    dockerfile_path = f'{context.install_dir}/Docker/Dockerfile'
    return ExtraVars(exec_type, temp_dir, gcp_project, gcp_cred_file, region, resources_path, dockerfile_path, **config)


def file_check(context: MSABContext):
    # Create mods and world directories if they don't exist
    os.makedirs('resources/mods', exist_ok=True)
    os.makedirs('resources/world', exist_ok=True)
    file_list: list[str] = [
        'resources/eula.txt',
        'resources/ops.json',
        'resources/server.properties',
        'resources/whitelist.json',
        'gcp_credential.json',
        'msab.yml'
    ]
    exists_files = reduce(lambda a, b: a and b, map(os.path.exists, file_list), True)
    if exists_files:
        context.logger.info('File existence confirmation: OK.')
    else:
        context.logger.error('The following files are required under the execution directory. Requierd files:resource/eula.txt, resource/ops.json, resource/whitelist.json, resource/server.properties, gcp_credential.json, msab.yml')
        raise MSABExecption


def args_check(context: MSABContext, args: list):
    exec_types = ['create', 'start', 'stop', 'delete', 'download']
    error_msg = 'The msab command expects one of create, start, stop, delete, download as command line arguments'
    if len(args) == 0:
        context.logger.error(error_msg)
        raise MSABExecption
    elif args[0] in exec_types:
        context.logger.error(error_msg)
        raise MSABExecption
    else:
        context.logger.info('Args confirmation: OK')


def create_config(context: MSABContext, extra_vars: ExtraVars):
    with open(f'{context.exec_dir}/ansible.cfg', 'w') as cfg:
        cfg.write(f'[defaults]\nhost_key_checking = False\n\n[ssh_connection]\nssh_args = -o UserKnownHostsFile={extra_vars.temp_dir}/known_hosts')


def run_ansible(context: MSABContext, extra_vars: ExtraVars):
    command = ['ansible-playbook', f'{context.install_dir}/playbook.yml', '-e', str(asdict(extra_vars))]
    subprocess.run(command)


def main():
    try:
        context: MSABContext = initialize_context()
        file_check(context)
        args: list(str) = sys.argv
        args_check(context, args)
        extra_vars: ExtraVars = initialize_extra_vars(context, args)
        context.logger.info(str(asdict(extra_vars)))
        create_config(context, extra_vars)
        run_ansible(context, extra_vars)
    except MSABExecption as e:
        context.logger.error(f'msab has error.')
        sys.exit(1)
    except Exception as e:
        context.logger.error(f'Exception in msab command: {str(e)}')
        sys.exit(1)
    finally:
        context.logger.info('finished msab.')


if __name__ == '__main__':
  main()
