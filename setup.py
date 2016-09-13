from setuptools import setup, find_packages

setup(
    name='mpy-tools',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mpy-upload=mpy_utils.upload:main',
        ],
    },
)
