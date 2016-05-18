import os
from ..conf.conf import config
from .file import load_project_config

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
