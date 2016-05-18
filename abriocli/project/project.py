import click, json, requests, os

from ..conf.conf import errors,config

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

    if response.status_code == 409 :
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


def load_project_config() :
    '''
    read config dict from json file
    '''
    with open('./abrio.json', 'r') as config_file:
        return json.load(config_file)


def load_component_config(name) :
    '''
    shorthand for opening config file for one component only
    '''
    with open('./abrio.json', 'r') as config_file:
        project_config = json.load(config_file)
        for comp in project_config['components'] :
            if comp['name'] == name :
                return comp
    return False


def write_project_config(config) :
    '''
    write config dict to json file
    '''
    with open('./abrio.json', 'w' ) as config_file:
        config_file.write(json.dumps(config, indent=4, separators=(',', ': ')))

def write_component_config(name, component_config) :
    project_config = load_project_config()
    components = project_config['components']
    for idx,comp in enumerate(components) :
        if comp['name'] == name :
            components[idx] = component_config
            write_project_config(project_config)
            return

def add_component_project(component_config) :
    '''
    add a component to project components
    '''
    config = load_project_config()
    components = config['components']
    components.append(component_config)
    write_project_config(config)


def remove_component_project(name) :
    '''
    remove a component form project
    '''
    config = load_project_config()
    components = config['components']
    for comp in components :
        if comp['name'] == name :
            components.remove(comp)
            write_project_config(config)
            return

def ensure_component_exists(name) :
    config = load_project_config()
    components = [ component['name'] for component in config['components'] ]
    if name in components :
        return  True
    return False


def ensure_abrio_root() :
    path = os.getcwd()
    file = config['abrio_root_file']
    if os.path.exists(os.path.join(path, file)) :
        return True
    return False
