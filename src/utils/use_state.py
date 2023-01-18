'''
Save state across files and run times
'''
import json

from constants import STATE_PATH

# create a function that reads a json, if json doesn't exist, create it
def read_json():
    '''Reads a json, if json doesn't exist, create it'''
    try:
        # open json using with
        with open(STATE_PATH, 'r', encoding="utf-8") as f:
            # load json
            file = json.load(f)
            f.close()
            return file
    except FileNotFoundError:
        # if file doesn't exist, create it
        with open(STATE_PATH, 'w', encoding="utf-8") as f:
            json.dump({}, f)
            f.close()
        return {}

# create a function that writes to a json
def write_json(file):
    '''Writes to a json'''
    with open(STATE_PATH, 'w', encoding="utf-8") as f:
        json.dump(file, f)
        f.close()

# create class docstring for UseState
class UseState:
    '''Creates a state that can be used in the bot'''
    def __init__(self, name, default):
        # set the name of the state
        self.name = name

        # read json
        file = read_json()
        # if the name doesn't exist in the json, create it
        if name not in file:
            file[name] = default
            write_json(file)
        # set the value of the state
        self.value = file[name]

    # create a function that sets the value of the state
    def set(self, value):
        '''Set value of the state'''
        # read json
        file = read_json()
        # set the value of the state
        file[self.name] = value
        # write json
        write_json(file)

    # create a function that gets the value of the state
    def get(self):
        '''Get value of the state'''
        # read json
        file = read_json()
        # return the value of the state
        return file[self.name]
        