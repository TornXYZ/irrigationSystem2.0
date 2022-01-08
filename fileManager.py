import os.path
import csv
from datetime import datetime

class fileManager():
    "Class which contains functions to save and load data from files"

    def __init__(self) -> None:
        pass


    # add a 'n.a.' as measured data, if there are gaps in flowerpot slot-array
    def build_data_to_write(self, flowerpots):
        maximum_slot = max([pot.slot for pot in flowerpots])

        data_array = []
        pot_iterator = 0

        for slot in range(maximum_slot + 1):
            if slot == flowerpots[pot_iterator].slot:
                data_array.append(flowerpots[pot_iterator].actual_moisture.value)
                pot_iterator += 1
            else:
                data_array.append('n.a.')
        return data_array


    def write_data_to_file(self, filename: str,timestamp: datetime, flowerpots) -> None:
        if not os.path.exists(filename):
            maximum_slot = max([pot.slot for pot in flowerpots])

            header1 = ['timestamp'] + list(range(0, maximum_slot + 1))
            with open(filename, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(header1)
            

        data_to_write = [timestamp] + self.build_data_to_write(flowerpots)
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data_to_write)
        return



