import os.path
import csv
from datetime import datetime
import json
import jsons

class fileManager():
    "Class which contains functions to save and load data from files"

    def __init__(self) -> None:
        pass


    def read_json(self, path) -> str:
        try:
            with open(path, 'r') as handle:
                return json.load(handle)
        except FileNotFoundError:
            print('Could not read JSON file. File not found.')
            return ""
        except json.JSONDecodeError:
            print('Could not read JSON file. Could not been parsed as JSON.')
            return ""


    def dump_data_to_json(self, data, path) -> None:
        with open(path, 'w') as outfile:
            json_string = jsons.dump(data)
            json.dump(json_string, outfile, indent=4, sort_keys=True)


    # add a 'n.a.' as measured data, if there are gaps in flowerpot slot-array
    def build_data_to_write(self, flowerpots):
        maximum_slot = max([pot.slot for pot in flowerpots])

        data_array = []
        pot_iterator = 0

        for slot in range(maximum_slot + 1):
            if slot == flowerpots[pot_iterator].slot:
                data_array.append(flowerpots[pot_iterator].actual_moisture)
                pot_iterator += 1
            else:
                data_array.append('n.a.')
        return data_array


    def write_data_to_file(self, filename: str,timestamp: datetime, flowerpots) -> None:
        if not flowerpots:
            return
            
        if not os.path.exists(filename):
            maximum_slot = max([pot.slot for pot in flowerpots])

            header1 = ['timestamp'] + list(range(0, maximum_slot + 1))
            with open(filename, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(header1)
            

        data_to_write = [timestamp.strftime("%Y-%m-%d %H:%M:%S")] + self.build_data_to_write(flowerpots)
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data_to_write)
        return



