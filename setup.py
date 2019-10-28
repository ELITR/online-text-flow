from setuptools import setup

setup(
    name='online-text-flow',
    version='1.0',
    url='http://github.com/ELITR/online-text-flow',
    license='GPL',
    author='Otakar Smrz',
    author_email='otakar-smrz users.sf.net',
    py_modules=['events', 'client', 'server', 'group'],
    include_package_data=True,
    package_data=[
        '': ['*.html', '*.md']
        ],
    install_requires=[
        'click',
        'flask',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'online-text-flow=group:cli',
            'online-text-flow-events=events:main',
            'online-text-flow-client=client:main',
            'online-text-flow-server=server:main',
        ],
    },
)
