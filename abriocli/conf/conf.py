config = {
    "server" : {
        # "host" : "http://127.0.0.1:5000/api/v1/",
        "host" : "http://abrio.ir/api/v1/",
    } ,
    "abrio_root_file" : "abrio.json",
    "sdk_file" : "AbrioSDK-V0.0.5.zip"
}

errors = {
    "UNKNOWN_NETWORK" : "Unknown Error occurred while connection to server. try again"
}

from os.path import *
MAIN_DIRECTORY = dirname(dirname(__file__))
def get_full_path(*path):
    return join(MAIN_DIRECTORY, *path)
