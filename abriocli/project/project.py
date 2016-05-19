import click, requests, json
from terminaltables import AsciiTable
from ..conf.conf import errors
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
        'create_date' : ''
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
    if not ensure_abrio_root():
        click.secho('\nAbrio Root Directory Not Detected.\n', fg="red", bold=True)
        return

    click.secho("\nConnecting to server..\n", fg='yellow', bold=True)
    project_config = load_project_config()
    pkey = project_config['private_key']
    response = requests.get(
        config['server']['host'] + 'project/status',
        json={'private_key': pkey}
    )
    if response.status_code == 200 :
        content = json.loads(response.content)
        project_config['create_date'] = content['create_date']
        project_config['name'] = content['name']
        write_project_config(project_config)

        project_table = [
            ['Name', "Is Running", "Created At", "Owner"],
            [
                project_config['name'],
                str(content['is_running']),
                project_config['create_date'],
                project_config['email']
            ]
        ]
        click.echo(AsciiTable(project_table).table)

    else :
        click.secho(errors["UNKNOWN_NETWORK"], bold=True, fg="red")

