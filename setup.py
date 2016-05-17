from setuptools import setup

setup(
    # Main Descriptions
    name="AbrIO",
    version="0.0.3",
    description = 'Abrio Engine cli for developers',
    author = 'AbrIO',
    author_email = 'abrioengine@gmail.com',
    url = 'https://github.com/Abrioengine/abrio-cli',
    download_url = 'https://github.com/Abrioengine/abrio-cli/archive/0.0.3.tar.gz',

    # Included packages
    packages=['abriocli'],

    # Included Dependencies
    install_requires=[
        'Click',
        'clint',
        'requests_toolbelt',
        'terminaltables'
    ],

    # Application Entry Point . Probably Just this one
    entry_points={
        'console_scripts' : ['abrio=abriocli.abrio:cli']
    } ,

    # Metadata Configurations 
    include_package_data=True,
      zip_safe=False
)
