import tkinter as tk
import flowerpotManager
import configurationManager
import exceptions

class GUI:
    "This class controls the GUI."

    def __init__(self, irr_system: flowerpotManager):
        self.irr_system = irr_system

        self.root = tk.Tk()
        self.header_frame = tk.Frame(self.root, borderwidth=3, relief='sunken')
        self.pot_frame = tk.Frame(self.root, borderwidth=3, relief='sunken')
        self.status_frame = tk.Frame(self.root, borderwidth=3, relief='sunken', bg='white')

        self.header_frame.pack(fill='x')
        self.pot_frame.pack(fill='x')
        self.status_frame.pack(fill='x')
        

        tk.Label(self.header_frame, text="IRRIGATION SYSTEM").grid(row=0)
        tk.Label(self.header_frame, text="Add flowerpot: ").grid(row=1, column=0)
        tk.Label(self.header_frame, text="Flowerpot list: ").grid(row=2, column=0)

        self.new_pot_slot_entry = tk.Entry(self.header_frame)
        self.new_pot_slot_entry.grid(row=1, column=1)

        new_pot_name_entry = tk.Entry(self.header_frame)
        new_pot_name_entry.insert(0, "pot0")
        new_pot_name_entry.grid(row=1, column=2)

        new_pot_button = tk.Button(self.header_frame, text="Add pot.", command=lambda: self.add_flowerpot(int(self.new_pot_slot_entry.get()), str(new_pot_name_entry.get()))).grid(row=1, column=3)

        self.num_pots_str = tk.StringVar()
        self.num_pots_str.set("0")
        num_pots_label = tk.Label(self.status_frame, textvariable=self.num_pots_str, bg='white').grid(row=0, column=0)

        self.log_output = tk.StringVar()
        self.log_output.set("Booting complete!")
        log_label = tk.Label(self.status_frame, textvariable=self.log_output, bg='white').grid(row=1, column=0, columnspan=3)

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
        new_slot_label = tk.Label(self.pot_frame, text=pot.slot)
        new_slot_label.grid(row=3 + int(pot.slot), column=0)
        self.slot_label_collection.append(new_slot_label)

        new_name_label = tk.Label(self.pot_frame, text=pot.name)
        new_name_label.grid(row=3 + int(pot.slot), column=1)
        self.name_label_collection.append(new_name_label)

        new_actual_moisture_label = tk.Label(self.pot_frame, text=pot.actual_moisture)
        new_actual_moisture_label.grid(row=3 + int(pot.slot), column=2)
        self.actual_moisture_label_collection.append(new_actual_moisture_label)

        new_expected_moisture_label = tk.Label(self.pot_frame, text=pot.expected_moisture)
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

        self.log_output.set(f"Pot \'{new_pot.name}\' added at slot {new_pot.slot}.")
        self.build_pot_labels(new_pot)

        self.num_pots_str.set(str(len(self.name_label_collection)))
        self.update_new_pot_slot_insert()
        return


    def remove_flowerpot(self, slot: int):
        try:
            self.irr_system.remove_pot(slot)
        except exceptions.PotNotExistingError:
            self.log_output.set(f"Pot at slot {slot} is not existing! No pot has been deleted.")
            return

        # add functionality to remove widgets




def main():
    config = configurationManager.configuration('config.ini')
    irr_system = flowerpotManager.flowerpotManager(config)
    gui = GUI(irr_system)
    gui.run()

    print("End!")

if __name__ == "__main__":
    main()