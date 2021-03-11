from setuptools import setup, find_packages
setup(
    name='online-text-flow',
    version='1.7.0',
    url='http://github.com/ELITR/online-text-flow',
    license='GPL',
    author='Otakar Smrz',
    author_email='otakar-smrz users.sf.net',
    namespace_packages=['elitr'],
    packages=['elitr', 'elitr.onlinetextflow'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'click',
        'mosestokenizer',
        'requests',
        'websocket-client',
    ],
    entry_points={
        'console_scripts': [
            'online-text-flow=elitr.onlinetextflow:main',
            'online-text-flow-events=elitr.onlinetextflow.events:main',
            'online-text-flow-client=elitr.onlinetextflow.client:main',
            'online-text-flow-to_brief=elitr.onlinetextflow.to_brief:main',
            'online-text-flow-from_brief=elitr.onlinetextflow.from_brief:main',
        ],
    },
)
