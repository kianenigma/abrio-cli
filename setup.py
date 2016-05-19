from setuptools import setup

setup(
    # Main Descriptions
    name="AbrIO",
    version="0.0.42",
    description = 'Abrio Engine cli for developers',
    author = 'AbrIO',
    author_email = 'abrioengine@gmail.com',
    url = 'https://github.com/Abrioengine/abrio-cli',
    download_url = 'https://github.com/Abrioengine/abrio-cli/archive/0.0.42.tar.gz',

    # Included packages
    packages=['abriocli', 'abriocli.component', 'abriocli.project', 'abriocli.util', 'abriocli.conf'],

    # Included Dependencies
    install_requires=[
        'Click',
        'clint',
        'requests_toolbelt',
        'terminaltables',
        'colorclass'
    ],

    # Application Entry Point . Probably Just this one
    entry_points={
        'console_scripts' : ['abrio=abriocli.abrio:cli']
    } ,

    # Metadata Configurations 
    include_package_data=True,
      zip_safe=False
)
