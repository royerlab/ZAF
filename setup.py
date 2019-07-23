from setuptools import setup

setup(
    name='fishfeed',
    version='0.1',
    py_modules=['fishfeed'],
    install_requires=[
        'Click', 'smbus'
    ],
    entry_points='''
        [console_scripts]
        fishfeed=fishfeed.cli:fishfeed
    ''',
)
