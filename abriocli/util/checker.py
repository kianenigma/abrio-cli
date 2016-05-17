import os
from ..conf.conf import config

def ensure_abrio_root() :
    path = os.getcwd()
    file = config['abrio_root_file']
    if os.path.exists(os.path.join(path, file)) :
        return True
    return False


