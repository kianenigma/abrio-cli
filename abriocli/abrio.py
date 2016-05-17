import click
import os , zipfile
import requests
import json
from clint.textui.progress import Bar as ProgressBar
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

import component.component as Component
import project.project as Project
import conf.conf as configuration

base_url = configuration.config['server']['host']
api_url  = configuration.config['server']['api_url']
sdk_file = configuration.config['sdk_file']

def get_file_path(file_path) :
    '''
    get a file relative path from packages install directory
    '''
    return os.path.join(
    os.path.dirname(__file__),'data',file_path )

def create_callback(encoder):
    encoder_len = encoder.len

    bar = ProgressBar(expected_size=encoder_len, filled_char='=')

    def callback(monitor):
        bar.show(monitor.bytes_read)
    return callback

def create_upload(file_path):
    file_name = file_path.split("/")[-1]
    return MultipartEncoder({'files':(file_name,open(file_path, 'rb'))})


@click.group()
def cli():
    '''
    Abrio Core Command Line Interface

        .________        _______       ______        ________      ______
        /_______/\     /_______/\     /_____/\      /_______/\    /_____/\
        \::: _  \ \    \::: _  \ \    \:::_ \ \     \__.::._\/    \:::_ \ \
        .\::(_)  \ \    \::(_)  \/_    \:(_) ) )_      \::\ \      \:\ \ \ \
        ..\:: __  \ \    \::  _  \ \    \: __ `\ \     _\::\ \__    \:\ \ \ \
        ...\:.\ \  \ \    \::(_)  \ \    \ \ `\ \ \   /__\::\__/\    \:\_\ \ \
        ....\__\/\__\/     \_______\/     \_\/ \_\/   \________\/     \_____\/  '''
    pass

# Croup Command for Project
@cli.group()
def project() :
    '''
    Create and manage a project
    '''
    pass


# Group Command for component
@cli.group()
def component() :
    '''
    Create and manage a component
    '''
    pass

project.add_command(Project.init)
project.add_command(Project.deploy)
project.add_command(Project.stop)
project.add_command(Project.restart)
project.add_command(Project.status)

component.add_command(Component.init)
component.add_command(Component.upload)
component.add_command(Component.rm)
# @cli.command()
# def deploy() :
#     '''
#         Deploy Abrio Project.
#         creates the project in website,
#         uses the returned token to upload
#         the jar file.
#     '''
#     if os.path.exists("abrio.json"):
#         config = json.loads(open("abrio.json").read().strip())
#         create_response = requests.post(base_url+api_url+"/create",json={"name":config["name"]})
#         token = ""
#         if create_response.status_code == 201:
#             token = create_response.json()["token"]
#             config["private key"] = token
#             config_file = open("abrio.json","w")
#             config_file.write(json.dumps(config))
#             click.echo("* created project on server")
#         else:
#             click.echo(click.style(create_response.text , bg='red'))
#             click.echo(click.style("problem in connecting to server" , bg='red'))
#
#         file_path = "sample/build/libs/%s.jar" % (config["name"])
#         old_file_path = "sample/build/libs/sample.jar "
#
#         if not os.path.exists(file_path):
#             click.echo("* building jar ...")
#             os.system('gradle jar')
#             os.system("mv "+ old_file_path + file_path)
#         else:
#             click.echo("* jar exists")
#
#         click.echo(click.style("* uploading project ..." ,blink=True,bold=True))
#         encoder = create_upload(file_path)
#         callback = create_callback(encoder)
#         monitor = MultipartEncoderMonitor(encoder, callback)
#         #upload_response = requests.post(,headers = config, files={"files":open("sample/build/libs/%s.jar"%(config["name"]),"rb")})
#         config['Content-Type'] = monitor.content_type
#
#
#         upload_response = requests.post(base_url+api_url+"/upload", data=monitor, headers=config)
#         print('\nUpload finished! (Returned status {0} {1})'.format(upload_response.status_code, upload_response.reason))
#         #upload_response = requests.post(base_url+api_url+"/upload",headers = config, files={"files":open("sample/build/libs/%s.jar"%(config["name"]),"rb")})
#
#         if upload_response.status_code == 200:
#             click.echo(click.style("Project Deployed" , bg='green' , fg="white"))
#         else:
#             click.echo(click.style("problem in uploading to server" , bg='red'))
#             click.echo(click.style(upload_response.text , bg='red',fg="white"))
#         #os.system('cp sample/build/libs/sample.jar ' + out)
#     else:
#         click.echo(click.style("config file not found, move to project folder" ,fg="white", bg='red'))
#
# @cli.command()
# def compile() :
#     click.echo("* building jar ...")
#     os.system('gradle jar')
#
#
#
# @cli.command()
# def debug() :
#     pass
