import click, zipfile, json
import requests
import datetime
from colorclass import Color
from terminaltables import AsciiTable

from requests.auth import HTTPBasicAuth
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from clint.textui.progress import Bar as ProgressBar

from ..util.file import *
from ..util.checker import *
from ..conf.conf import config, get_full_path
from ..conf.conf import config,errors


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

    click.secho("\nConnection to sever..." , bold=True, fg="yellow")
    project_config = load_project_config()
    email = project_config['email']
    pwd = project_config['password']
    name = name
    is_private = public
    response = requests.post(
        config['server']['host']+'component/create',
        auth=HTTPBasicAuth(email, pwd),
        json={'isPrivate': is_private, 'name': name}
    )

    if response.status_code == 201 :
        pkey = response.json()['token']
        os.mkdir(name)
        zip_file = zipfile.ZipFile(os.path.join(get_full_path('data', config['sdk_file'])))
        zip_file.extractall(name)

        component_config = {
            'pkey': pkey,
            'public': public,
            'version': version,
            'name': name,
            'last_uploaded': ''
        }

        # with open(os.path.join(name, (name+'.json')), 'w') as config_file :
        #     config_file.write(json.dumps(component_config, indent=4, separators=(',', ': ')))

        add_component_project(component_config)

        click.secho("\nComponent <{0}> created.\n".format(name), bold=True, fg='green')

    else :
        click.secho(errors["UNKNOWN_NETWORK"],bold=True, fg="red")


@click.command()
@click.argument('name')
def upload(name) :
    '''
    Upload Abrio component to server.
    '''

    if not ensure_abrio_root():
        click.secho('\nAbrio Root Directory Not Detected.\n', fg="red", bold=True)
        return

    if not ensure_component_exists(name):
        click.secho("\nComponent <{0}> does not exist.\n".format(name), bold=True, fg="red")

    build_dir = '/sample/build/libs/'

    os.system('cd {0} && gradle jar && cd ..'.format(name))
    jar_dir = name + build_dir + name + '.jar'
    os.rename(name + build_dir + 'sample.jar',jar_dir)

    encoder = create_upload(jar_dir)
    callback = create_callback(encoder)
    monitor = MultipartEncoderMonitor(encoder, callback)

    component_config = load_component_config(name)
    component_config['last_uploaded'] = str(datetime.datetime.now())
    write_component_config(name, component_config)

    headers = {
        'Content-Type': monitor.content_type,
        'private key': component_config['pkey'],
        'version' : component_config['version']
    }

    upload_response = requests.post(
        config['server']['host'] + "component/upload",
        data=monitor,
        # auth=HTTPBasicAuth(email, pwd),
        headers=headers)

    if upload_response.status_code == 200 :
        click.secho('\n\n\nComponent uploaded\n', bold=True, fg="green")

    else :
        click.secho(errors["UNKNOWN_NETWORK"], bold=True, fg="red")





@click.option('--sure', prompt="Are you sure you want to delete this component", is_flag=True)
@click.argument('name')
@click.command()
def rm(name, sure) :
    '''
    Delete Abrio Component.
    '''

    if not ensure_abrio_root():
        click.secho('\nAbrio Root Directory Not Detected.\n', fg="red", bold=True)
        return

    if sure :
        if ensure_component_exists(name) :
            os.system('rm -Rf {0}'.format(name))
            remove_component_project(name)
            # todo delete from server
            click.secho("\nComponent <{0}> deleted.\n".format(name), bold=True, fg="yellow")

        else :
            click.secho("\nComponent <{0}> does not exist.\n".format(name), bold=True, fg="red")

@click.command()
def ls() :
    '''
    List Available Abrio components
    '''

    if not ensure_abrio_root():
        click.secho('\nAbrio Root Directory Not Detected.\n', fg="red", bold=True)
        return



    project_config = load_project_config()

    response = requests.get(
        config['server']['host'] + "project/list_components",
        json={'private_key': project_config['private_key']}
    )

    if response.status_code == 200 :
        component_table = [
                        ['Component Name', 'Version', 'Public', "Last Upload" , "Type"]] + \
                        [
                            [
                                component['name'],
                                component['version'],
                                str(component['public']),
                                component['last_uploaded'],
                                Color('{autoyellow}Local{/autoyellow}')
                            ] for component in project_config['components']
                        ]

        component_table += [
            [
                comp['name'],
                comp['deploy_version'],
                 str(not comp['private']),
                 "---",
                 Color('{autocyan}Online{/autocyan}')
             ] for comp in json.loads(response.content)['result']]


        table = AsciiTable(component_table)
        click.echo(table.table)

    else :
        click.secho(errors["UNKNOWN_NETWORK"], bold=True, fg="red")




def create_callback(encoder):
    encoder_len = encoder.len

    bar = ProgressBar(expected_size=encoder_len, filled_char='=')

    def callback(monitor):
        bar.show(monitor.bytes_read)
    return callback

def create_upload(file_path):
    file_name = file_path.split("/")[-1]
    return MultipartEncoder({'files':(file_name,open(file_path, 'rb'))})