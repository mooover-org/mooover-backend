from setuptools import setup, find_packages

setup(
    name='corelib',
    description='Library that contains data structures and functionalities to be used anywhere in the Mooover project.',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'emoji == 2.12.1',
        "fastapi == 0.111.0",
        'python-jose == 3.3.0',
        'six == 1.16.0',
    ],
)
