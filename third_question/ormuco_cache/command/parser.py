from ormuco_cache.command.retrieve import RetrieveCommand
from ormuco_cache.command.store import  StoreCommand

import json


class CommandParser:
    def __init__(self, settings):
        self.retrieveCommand = RetrieveCommand(settings)
        self.storeCommand = StoreCommand(settings)

    def parse(self, input):
        try:
            tokens = input.split(' ')
            command_token = tokens[0]
            key = tokens[1]

            if command_token == RetrieveCommand.COMMAND_PREFIX:
                return self.retrieveCommand.execute(key)
            elif command_token == StoreCommand.COMMAND_PREFIX:
                json_string = ''.join(tokens[2:])
                data = json.loads(json_string)
                return self.storeCommand.execute(key, data)
            #elif command_token == 'ACK':
            #    return True
            #elif command_token == "MISS":
            #    return None
            else:
                raise Exception('invalid command')
        except:
            if input == 'ACK':
                return True
            elif input == "MISS":
                return None
            else:
                raise Exception('invalid command')
