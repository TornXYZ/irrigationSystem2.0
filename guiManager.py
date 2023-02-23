import tkinter as tk
import flowerpotManager

class GUI:
    "This class controls the GUI."

    def __init__(self, irr_system: flowerpotManager):
        self.irr_system = irr_system
        self.flowerpot_labels = []

        self.root = tk.Tk()
        tk.Label(self.root, text="IRRIGATION SYSTEM").grid(row=0)
        tk.Label(self.root, text="Add flowerpot: ").grid(row=1, column=0)
        tk.Label(self.root, text="Flowerpot list: ").grid(row=2, column=0)
        new_pot_slot_entry = tk.Entry(self.root)
        new_pot_slot_entry.insert(0, 0)
        new_pot_slot_entry.grid(row=1, column=1)
        new_pot_name_entry = tk.Entry(self.root)
        new_pot_name_entry.insert(0, "pot0")
        new_pot_name_entry.grid(row=1, column=2)

        new_pot_button = tk.Button(self.root, text="Add pot.", command=lambda: self.add_flowerpot_get_label(new_pot_slot_entry.get(), new_pot_name_entry.get())).grid(row=2, column=3)

        self.num_pots_str = tk.StringVar()
        self.num_pots_str.set("0")
        num_pots_label = tk.Label(self.root, textvariable=self.num_pots_str).grid(row=6, column=1)

        self.root.mainloop()
        return

    
    def add_flowerpot(self, slot: int, name: str) -> flowerpotManager.flowerpot:
        pot = self.irr_system.add_pot(slot, name)
        return pot

    def add_flowerpot_get_label(self, slot: int, name: str) -> tk.Label:
        pot = self.add_flowerpot(slot, name)
        pot_label = tk.Label(self.root, text=name)
        pot_label.grid(row=2 + int(slot), column=0)
        self.flowerpot_labels.append(pot_label)
        self.num_pots_str.set(str(len(self.flowerpot_labels)))

        return pot_label
