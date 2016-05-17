import click
from ..util.checker import *

@click.option('--version' , prompt="Enter component version", default="0.0.1")
@click.option('--public', is_flag=True, prompt='Do you want to mark this component as private?' )
@click.option('--name', prompt="Enter component name")
@click.command()

def init(name, public, version):
    '''
    Create new abrio component.
    '''
    print version , public , name
    if not ensure_abrio_root() :
        click.secho('\nAbrio Root Directory Not Detected.' , fg="red", bold=True)
        return


@click.command()
def upload() :
    '''
    Upload Abrio component to server.
    '''
    pass


@click.command()
def rm() :
    '''
    Delete Abrio Component.
    '''
    pass


@click.command()
def ls() :
    '''
    List Available Abrio components
    '''
    pass