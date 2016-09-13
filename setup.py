from setuptools import setup

setup(
    name='mpy-tools',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'mpy-upload=mpy_utils.upload:main',
        ],
    },
)
