from setuptools import setup, find_packages

setup(
    name='online-text-flow',
    version='1.0',
    url='http://github.com/ELITR/online-text-flow',
    license='GPL',
    author='Otakar Smrz',
    author_email='otakar-smrz users.sf.net',
    namespace_packages=['elitr'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click',
        'flask',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'online-text-flow=elitr.onlinetextflow:main',
            'online-text-flow-events=elitr.onlinetextflow.events:main',
            'online-text-flow-client=elitr.onlinetextflow.client:main',
            'online-text-flow-server=elitr.onlinetextflow.server:main',
        ],
    },
)
