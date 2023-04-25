#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Yataka Neria

import subprocess
import os
import sys
import logging
from dataclasses import dataclass, asdict
from functools import reduce


@dataclass
class ExtraVars:
    # create, start, stop, delete, download
    exec_type: str


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


def initialize_extra_vars(context: MSABContext, args: list(str)) -> ExtraVars:
    exec_type = args[0]
    return ExtraVars(exec_type)


def file_check(context: MSABContext):
    # Create mods and world directories if they don't exist
    os.makedirs('resource/mods', exist_ok=True)
    os.makedirs('resource/world', exist_ok=True)
    file_list: list[str] = [
        'resource/eula.txt',
        'resource/ops.json',
        'resource/server.properties',
        'resource/whitelist.json',
        'gcp_credential.json',
        'msab.yml'
    ]
    exists_files = reduce(lambda a, b: a and b, map(os.path.exists, file_list), True)
    if exists_files:
        context.logger.info('File existence confirmation: OK.')
    else:
        context.logger.error('The following files are required under the execution directory. Requierd files:resource/eula.txt, resource/ops.json, resource/whitelist.json, resource/server.properties, gcp_credential.json, msab.yml')
        raise MSABExecption


def args_check(context: MSABContext, args: list(str)):
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


def run_ansible(context: MSABContext, extra_vars: ExtraVars):
    command = ['ansible-playbook', f'{context.install_dir}/playbook.yml', '-e', asdict(extra_vars)]
    subprocess.run(command)


def main():
    try:
        context: MSABContext = initialize_context()
        file_check(context)
        args: list(str) = sys.argv
        args_check(context, args)
        extra_vars: ExtraVars = initialize_extra_vars(context, args)
        run_ansible(context, extra_vars)
        context.logger.info('python log finished.')
        context.logger.info('Below is the ansible run log')
    except MSABExecption as e:
        context.logger.error(f'msab has error.')
        sys.exit(1)
    except Exception as e:
        context.logger.error(f'Exception in msab command: {str(e)}')
        sys.exit(1)


if __name__ == '__main__':
  main()
