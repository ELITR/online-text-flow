from setuptools import setup, find_namespace_packages
from sys import version_info

setup(
    name='online-text-flow',
    version='1.8.1',
    url='http://github.com/ELITR/online-text-flow',
    license='GPL',
    author='Otakar Smrz',
    author_email='otakar-smrz users.sf.net',
    packages=find_namespace_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'asyncio',
        'click',
        'mosestokenizer',
        'quart' if version_info >= (3, 7) else 'quart==0.6.15',
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
