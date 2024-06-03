from setuptools import setup, find_packages

setup(
    name='commons',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'emoji == 1.7.0',
        'fastapi == 0.75.1',
        'jose == 1.0.0',
        'six == 1.16.0',
        'starlette == 0.17.1',
        'requests == 2.27.1',
        'neo4j == 4.4.3',
    ],
)
