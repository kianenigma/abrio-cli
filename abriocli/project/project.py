import click, json, requests, os

from ..conf.conf import errors,config
from ..util.file import *
from ..util.checker import *

@click.command()
@click.option('--pkey', prompt="Enter Project private key (create one in website if you don't have one)",)
@click.option('--email', prompt="Enter your Abrio Account Email")
@click.option('--password', prompt="Enter your Abrio Account Password" , hide_input=True)

def init(pkey, email, password) :
    '''
    Create new Abrio Project
    '''
    config = {
        'email' : email,
        'password' : password,
        'private_key' : pkey,
        'components' : [],
        'created_at' : ''
    }

    write_project_config(config)

    click.secho('\ndirectory marked as abrio project root. happy coding.\n',bold=True, fg='green')


@click.command()
def deploy() :
    '''
    Deploy Abrio project
    '''
    if not ensure_abrio_root():
        click.secho('\nAbrio Root Directory Not Detected.\n', fg="red", bold=True)
        return
    pkey = load_project_config()['private_key']
    response = requests.post(
        config['server']['host'] + 'project/start',
        json={'private_key' : pkey }
    )

    if response.status_code == 200:
        click.secho("\nProject Successfully Lunched.\n", bold=True, fg='green')

    elif response.status_code == 409 :
        click.secho("\nProject already lunched.\n" , bold=True, fg="yellow")

    else:
        click.secho(errors["UNKNOWN_NETWORK"], bold=True, fg="red")


@click.command()
def stop() :
    '''
    Stop Abrio Project
    '''
    if not ensure_abrio_root():
        click.secho('\nAbrio Root Directory Not Detected.\n', fg="red", bold=True)
        return
    pkey = load_project_config()['private_key']
    response = requests.post(
        config['server']['host'] + 'project/stop',
        json={'private_key': pkey}
    )

    if response.status_code == 200:
        click.secho("\nProject Successfully Stopped.\n", bold=True, fg='green')

    else:
        click.secho(errors["UNKNOWN_NETWORK"], bold=True, fg="red")


@click.command()
def status() :
    '''
    View Abrio project status
    '''
    pass
