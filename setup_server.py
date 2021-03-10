from setuptools import setup, find_packages
setup(
    name='online-text-flow-server',
    version='1.6.0',
    url='http://github.com/ELITR/online-text-flow',
    license='GPL',
    author='Otakar Smrz',
    author_email='otakar-smrz users.sf.net',
    namespace_packages=['elitr'],
    packages=['elitr', 'elitr.onlinetextflow_server'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        'asyncio',
        'click',
        'quart',
#        'requests',
#        'websocket-client',
    ],
    entry_points={
        'console_scripts': [
            'online-text-flow-server=elitr.onlinetextflow_server:main',
        ],
    },
)
