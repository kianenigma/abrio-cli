import click
import json

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

    with open('./abrio.json' , 'w+') as config_file :
        config_file.write(json.dumps(config,indent=4, separators=(',', ': ')))

    click.secho('\ndirectory marked as abrio project root. happy coding.\n',bold=True, fg='green')


@click.command()
def deploy() :
    '''
    Deploy Abrio project
    '''
    pass


@click.command()
def stop() :
    '''
    Stop Abrio Project
    '''
    pass


@click.command()
def restart() :
    '''
    Restart Abrio project
    '''
    pass


@click.command()
def status() :
    '''
    View Abrio project status
    '''
    pass