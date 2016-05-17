import click, os ,zipfile, json
from ..util.checker import *
from ..conf.conf import config, get_full_path
from ..project.project import add_component_project, remove_component_project

@click.option('--version', prompt="Enter component version", default="0.0.1" )
@click.option('--public', is_flag=True, prompt='Do you want to mark this component as public?' )
@click.option('--name', prompt="Enter component name", default="Test")
@click.command()

def init(name, public, version):
    '''
    Create new abrio component.
    '''
    if not ensure_abrio_root() :
        click.secho('\nAbrio Root Directory Not Detected.\n' , fg="red", bold=True)
        return

    if os.path.exists(name) :
        click.secho("\nDirecotry with name <{0}> already exists.\n".format(name), fg="red", bold=True)
        return


    os.mkdir(name)
    zfile = zipfile.ZipFile(os.path.join(get_full_path('data', config['sdk_file'])))
    zfile.extractall(name)

    # make a request to server and create this component
    component_config = {
        'pkey' : '',
        'public' : public,
        'version': version,
        'name' : name,
        'last_compiled' : ''
    }

    with open(os.path.join(name, (name+'.json')), 'w') as config_file :
        config_file.write(json.dumps(component_config, indent=4, separators=(',', ': ')))

    add_component_project(name)

    click.secho("\nComponent <{0}> created.\n".format(name), bold=True, fg='green')




@click.command()
def upload() :
    '''
    Upload Abrio component to server.
    '''
    pass


@click.option('--sure', prompt="Are you sure you want to delete this component", is_flag=True)
@click.argument('name')
@click.command()
def rm(name, sure) :
    '''
    Delete Abrio Component.
    '''
    if sure :
        os.system('rm -Rf {0}'.format(name))
        remove_component_project(name)
        click.secho("\nComponent <{0}> deleted.\n".format(name), bold=True, fg="yellow")

@click.command()
def ls() :
    '''
    List Available Abrio components
    '''
    pass