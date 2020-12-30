import sys

if sys.version_info < (3,7):
    # this ensures that events and client work on Python 3.6, but server
    # may not work correctly!!!
    quart = "quart==0.6.15"
else:
    quart = "quart"

from setuptools import setup, find_packages
setup(
    name='online-text-flow',
    version='1.4.1',
    url='http://github.com/ELITR/online-text-flow',
    license='GPL',
    author='Otakar Smrz',
    author_email='otakar-smrz users.sf.net',
    namespace_packages=['elitr'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'asyncio',
        'click',
        'mosestokenizer',
        quart,
        'requests',
        'websocket-client',
    ],
    entry_points={
        'console_scripts': [
            'online-text-flow=elitr.onlinetextflow:main',
            'online-text-flow-events=elitr.onlinetextflow.events:main',
            'online-text-flow-client=elitr.onlinetextflow.client:main',
            'online-text-flow-server=elitr.onlinetextflow.server:main',
            'online-text-flow-to_brief=elitr.onlinetextflow.to_brief:main',
            'online-text-flow-from_brief=elitr.onlinetextflow.from_brief:main',
        ],
    },
)
