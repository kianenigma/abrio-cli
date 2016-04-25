from setuptools import setup

setup(
    # Main Descriptions
    name="AbrIO",
    version="0.0.1",

    # Included packages
    packages=['abriocli'],

    # Included Dependencies
    install_requires=[
        'Click',
        'clint',
        'requests_toolbelt'
    ],

    # Application Entry Point . Probably Just this one
    entry_points={
        'console_scripts' : ['abrio=abriocli.abrio:cli']
    } ,

    # Metadata Configurations 
    include_package_data=True,
      zip_safe=False
)
