config = {
    "server" : {
        "host" : "http://127.0.0.1:5000",
        "api_url" : "/api/v1/component"
    } ,
    "abrio_root_file" : "abrio.json",
    "sdk_file" : "AbrioSDK-V0.0.3.zip"
}

from os.path import *
MAIN_DIRECTORY = dirname(dirname(__file__))
def get_full_path(*path):
    return join(MAIN_DIRECTORY, *path)
