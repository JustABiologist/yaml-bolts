import tkinter as tk
from tkinter import ttk, messagebox
import yaml

# Custom class for flow-style lists in YAML
class FlowList(list):
    pass

# Tell YAML to use flow style for FlowList
def represent_flow_list(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

yaml.add_representer(FlowList, represent_flow_list)

class YAMLBuilderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YAML Builder")
        
        # Data storage
        self.data = {'version': 1, 'sequences': [], 'constraints': []}
        self.protein_ids = []  # For chain dropdown
        self.ligand_info = {}  # Ligand ID: (type, value)
        self.current_binder = None
        self.current_contacts = []
        
        # Create tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)
        
        self.protein_frame = ttk.Frame(self.notebook)
        self.ligand_frame = ttk.Frame(self.notebook)
        self.constraint_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.protein_frame, text="Proteins")
        self.notebook.add(self.ligand_frame, text="Ligands")
        self.notebook.add(self.constraint_frame, text="Constraints")
        
        # Set up each tab
        self.setup_protein_tab()
        self.setup_ligand_tab()
        self.setup_constraint_tab()
        
        # Generate YAML button
        ttk.Button(root, text="Generate YAML", command=self.generate_yaml).pack(pady=5)

    def setup_protein_tab(self):
        ttk.Label(self.protein_frame, text="Number of Copies:").grid(row=0, column=0, padx=5, pady=5)
        self.protein_copies = ttk.Spinbox(self.protein_frame, from_=1, to=10, width=5)
        self.protein_copies.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.protein_frame, text="IDs (comma-separated):").grid(row=1, column=0, padx=5, pady=5)
        self.protein_ids_entry = ttk.Entry(self.protein_frame, width=30)
        self.protein_ids_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.protein_frame, text="Sequence:").grid(row=2, column=0, padx=5, pady=5)
        self.protein_seq = tk.Text(self.protein_frame, height=5, width=50)
        self.protein_seq.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.protein_frame, text="MSA Path:").grid(row=3, column=0, padx=5, pady=5)
        self.msa_entry = ttk.Entry(self.protein_frame, width=30)
        self.msa_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(self.protein_frame, text="Add Protein", command=self.add_protein).grid(row=4, column=1, pady=10)

    def setup_ligand_tab(self):
        ttk.Label(self.ligand_frame, text="Number of Copies:").grid(row=0, column=0, padx=5, pady=5)
        self.ligand_copies = ttk.Spinbox(self.ligand_frame, from_=1, to=10, width=5)
        self.ligand_copies.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.ligand_frame, text="IDs (comma-separated):").grid(row=1, column=0, padx=5, pady=5)
        self.ligand_ids_entry = ttk.Entry(self.ligand_frame, width=30)
        self.ligand_ids_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.ligand_frame, text="Type:").grid(row=2, column=0, padx=5, pady=5)
        self.ligand_type = ttk.Combobox(self.ligand_frame, values=["CCD", "SMILES"], state="readonly")
        self.ligand_type.grid(row=2, column=1, padx=5, pady=5)
        self.ligand_type.set("CCD")
        
        ttk.Label(self.ligand_frame, text="Value:").grid(row=3, column=0, padx=5, pady=5)
        self.ligand_value = ttk.Entry(self.ligand_frame, width=30)
        self.ligand_value.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(self.ligand_frame, text="Add Ligand", command=self.add_ligand).grid(row=4, column=1, pady=10)

    def setup_constraint_tab(self):
        ttk.Label(self.constraint_frame, text="Binder:").grid(row=0, column=0, padx=5, pady=5)
        self.binder_var = tk.StringVar()
        self.binder_dropdown = ttk.Combobox(self.constraint_frame, textvariable=self.binder_var)
        self.binder_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.constraint_frame, text="Chain:").grid(row=1, column=0, padx=5, pady=5)
        self.chain_var = tk.StringVar()
        self.chain_dropdown = ttk.Combobox(self.constraint_frame, textvariable=self.chain_var, values=self.protein_ids)
        self.chain_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.constraint_frame, text="Residue Number:").grid(row=2, column=0, padx=5, pady=5)
        self.residue_entry = ttk.Entry(self.constraint_frame, width=10)
        self.residue_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(self.constraint_frame, text="Add Contact", command=self.add_contact).grid(row=3, column=1, pady=5)
        ttk.Button(self.constraint_frame, text="Finalize Constraint", command=self.finalize_constraint).grid(row=4, column=1, pady=5)

    def add_protein(self):
        copies = int(self.protein_copies.get())
        ids_str = self.protein_ids_entry.get().strip()
        sequence = ''.join(self.protein_seq.get("1.0", tk.END).split())  # Remove newlines and spaces
        msa = self.msa_entry.get().strip() or "empty"
        if not ids_str or len(ids_str.split(',')) != copies:
            messagebox.showerror("Error", "Number of IDs must match copies!")
            return
        ids = [id.strip() for id in ids_str.split(',')]
        protein = {'protein': {'id': FlowList(ids), 'sequence': sequence, 'msa': msa}}
        self.data['sequences'].append(protein)
        self.protein_ids.extend(ids)
        self.chain_dropdown['values'] = self.protein_ids
        self.protein_ids_entry.delete(0, tk.END)
        self.protein_seq.delete("1.0", tk.END)
        self.msa_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Protein added with copies")

    def add_ligand(self):
        copies = int(self.ligand_copies.get())
        ids_str = self.ligand_ids_entry.get().strip()
        ligand_type = self.ligand_type.get().lower()
        value = self.ligand_value.get().strip()
        if not ids_str or not value or len(ids_str.split(',')) != copies:
            messagebox.showerror("Error", "Number of IDs must match copies!")
            return
        ids = [id.strip() for id in ids_str.split(',')]
        ligand = {'ligand': {'id': FlowList(ids), ligand_type: value}}
        self.data['sequences'].append(ligand)
        for ligand_id in ids:
            self.ligand_info[ligand_id] = (ligand_type.upper(), value)
        self.update_binder_dropdown()
        self.ligand_ids_entry.delete(0, tk.END)
        self.ligand_value.delete(0, tk.END)
        messagebox.showinfo("Success", "Ligand added with copies")

    def update_binder_dropdown(self):
        binder_options = [f"{lid} ({info[0]}: {info[1]})" for lid, info in self.ligand_info.items()]
        self.binder_dropdown['values'] = binder_options

    def add_contact(self):
        binder_selection = self.binder_var.get()
        chain = self.chain_var.get()
        residue = self.residue_entry.get().strip()
        if not binder_selection or not chain or not residue:
            messagebox.showerror("Error", "Select binder, chain, and residue!")
            return
        binder = binder_selection.split(" ")[0]  # Extract just the ID
        try:
            residue_num = int(residue)
        except ValueError:
            messagebox.showerror("Error", "Residue must be a number!")
            return
        if self.current_binder is None:
            self.current_binder = binder
            self.current_contacts = []
        elif self.current_binder != binder:
            messagebox.showerror("Error", "Finish current binder or finalize!")
            return
        self.current_contacts.append([chain, residue_num])
        self.residue_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Added {chain}:{residue_num} to {binder}")

    def finalize_constraint(self):
        if self.current_binder is None or not self.current_contacts:
            messagebox.showerror("Error", "No contacts to finalize!")
            return
        pocket = {'pocket': {'binder': self.current_binder, 'contacts': FlowList(self.current_contacts)}}
        self.data['constraints'].append(pocket)
        self.current_binder = None
        self.current_contacts = []
        messagebox.showinfo("Success", "Constraint finalized")

    def generate_yaml(self):
        yaml_str = yaml.dump(self.data, default_flow_style=False, sort_keys=False)
        with open('config.yaml', 'w') as f:
            f.write(yaml_str)
        result_window = tk.Toplevel(self.root)
        result_window.title("Your YAML")
        text = tk.Text(result_window, height=20, width=80)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, yaml_str)
        messagebox.showinfo("Success", "YAML generated and saved as 'config.yaml'")

if __name__ == "__main__":
    root = tk.Tk()
    app = YAMLBuilderGUI(root)
    root.mainloop()