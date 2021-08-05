#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages
from pkg_resources import resource_filename

# depending on your execution context the version file
# may be located in a different place!
vsn_path = resource_filename(__name__, 'async_hvac/version')
if not os.path.exists(vsn_path):
    vsn_path = resource_filename(__name__, 'version')
    if not os.path.exists(vsn_path):
        print("%s is missing" % vsn_path)
        sys.exit(1)

setup(
    name='vtb-async-hvac',
    version=open(vsn_path, 'r').read(),
    description='HashiCorp Vault API client (VTB version)',
    long_description='HashiCorp Vault API python 3.6+ client using asyncio (VTB version).',
    author='Vyacheslav Kazakov',
    author_email='vyachka@gmail.com',
    url='https://github.com/VyacheslavKazakov/async-hvac',
    keywords=['hashicorp', 'vault', 'hvac'],
    classifiers=['License :: OSI Approved :: Apache Software License'],
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.7.3',
    ],
    include_package_data=True,
    package_data={'async_hvac': ['version']},
    extras_require={
        'parser': ['pyhcl==0.4.4']
    }
)
