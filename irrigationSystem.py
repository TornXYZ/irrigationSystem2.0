import tkinter as tk
import flowerpotManager
import configurationManager
import exceptions

class GUI:
    "This class controls the GUI."

    def __init__(self, irr_system: flowerpotManager):
        self.irr_system = irr_system

        self.root = tk.Tk()
        tk.Label(self.root, text="IRRIGATION SYSTEM").grid(row=0)
        tk.Label(self.root, text="Add flowerpot: ").grid(row=1, column=0)
        tk.Label(self.root, text="Flowerpot list: ").grid(row=2, column=0)

        self.new_pot_slot_entry = tk.Entry(self.root)
        self.new_pot_slot_entry.grid(row=1, column=1)

        new_pot_name_entry = tk.Entry(self.root)
        new_pot_name_entry.insert(0, "pot0")
        new_pot_name_entry.grid(row=1, column=2)

        new_pot_button = tk.Button(self.root, text="Add pot.", command=lambda: self.add_flowerpot(int(self.new_pot_slot_entry.get()), str(new_pot_name_entry.get()))).grid(row=1, column=3)

        self.num_pots_str = tk.StringVar()
        self.num_pots_str.set("0")
        num_pots_label = tk.Label(self.root, textvariable=self.num_pots_str).grid(row=22, column=1)

        self.log_output = tk.StringVar()
        self.log_output.set("Booting complete!")
        log_label = tk.Label(self.root, textvariable=self.log_output).grid(row=23, column=1)

        self.name_label_collection = []
        self.slot_label_collection = []
        self.actual_moisture_label_collection = []
        self.expected_moisture_label_collection = []

        self.initialize_pot_labels()
        self.update_new_pot_slot_insert()
        return

    def run(self) -> None:
        self.root.mainloop()
        return

    def build_pot_labels(self, pot):
        new_slot_label = tk.Label(self.root, text=pot.slot)
        new_slot_label.grid(row=3 + int(pot.slot), column=0)
        self.slot_label_collection.append(new_slot_label)

        new_name_label = tk.Label(self.root, text=pot.name)
        new_name_label.grid(row=3 + int(pot.slot), column=1)
        self.name_label_collection.append(new_name_label)

        new_actual_moisture_label = tk.Label(self.root, text=pot.actual_moisture)
        new_actual_moisture_label.grid(row=3 + int(pot.slot), column=2)
        self.actual_moisture_label_collection.append(new_actual_moisture_label)

        new_expected_moisture_label = tk.Label(self.root, text=pot.expected_moisture)
        new_expected_moisture_label.grid(row=3 + int(pot.slot), column=3)
        self.expected_moisture_label_collection.append(new_expected_moisture_label)
        return


    def update_new_pot_slot_insert(self):
        new_insert = 0
        for pot in self.irr_system.pot_collection:
            if new_insert < pot.slot:
                break
            else: 
                new_insert += 1

        self.new_pot_slot_entry.delete(0, tk.END)
        self.new_pot_slot_entry.insert(0, str(new_insert))
        return
                

    def initialize_pot_labels(self):
        for pot in self.irr_system.pot_collection:
            self.build_pot_labels(pot)

        self.num_pots_str.set(str(len(self.name_label_collection)))
        return


    def add_flowerpot(self, slot: int, name: str) ->None:
        new_pot = flowerpotManager.flowerpot(slot, name)
        try:
            self.irr_system.add_pot(new_pot)
        except exceptions.PotDoubletteError:
            self.log_output.set(f"Slot {new_pot.slot} already occupied. Pot not added.")
            return

        self.build_pot_labels(new_pot)

        self.num_pots_str.set(str(len(self.name_label_collection)))
        self.update_new_pot_slot_insert()
        return


    def remove_pot(self):
        pass


def main():
    config = configurationManager.configuration('config.ini')
    irr_system = flowerpotManager.flowerpotManager(config)
    gui = GUI(irr_system)
    gui.run()

    print("End!")

if __name__ == "__main__":
    main()