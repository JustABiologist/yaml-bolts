# YAML Bolts

A Python GUI application for generating YAML configuration files for protein-ligand systems, built with Tkinter and PyYAML. This tool allows users to define protein sequences, ligands (with CCD or SMILES codes), and constraints, producing a structured YAML file for downstream use.

## Features

- **Protein Input**: Specify multiple protein copies with IDs, a stripped sequence (no newlines/spaces), and an optional MSA path (defaults to `"empty"`).
- **Ligand Input**: Add ligands with CCD or SMILES codes, supporting multiple copies with unique IDs.
- **Constraints**: Define binding constraints with a ligand binder and multiple protein chain-residue contacts.
- **Output**: Generates a YAML file (`config.yaml`) with flow-style lists for `id` and `contacts`, and block-style mappings.

Example output:

yaml
version: 1  # Optional, defaults to 1
sequences:
- protein:
    id: [A, B]
    sequence: MKFLPYIFLLCCGLWSTISFADEDYIEYRGISSNNRVTLDPLRLSNKELRWLASKKNL...
    msa: empty
- ligand:
    id: [C, D]
    smiles: ATP
constraints:
- pocket:
    binder: C
    contacts: [[A, 152], [B, 152]]

Installation
Clone the Repository:
bash

git clone https://github.com/JustABiologist/yaml-bolts.git
cd yaml-bolts

Install Dependencies:
Ensure you have Python 3.6+ installed.

Install required packages:
bash

pip install pyyaml

Tkinter comes with Python by default, but if it’s missing (e.g., on some Linux systems), install it:
bash

sudo apt-get install python3-tk  # Ubuntu/Debian

Usage
Run the Application:
bash

python yaml_builder.py

Using the GUI:
Proteins Tab: Enter the number of copies, comma-separated IDs, sequence, and optional MSA path. Click "Add Protein".

Ligands Tab: Specify copies, IDs, select CCD or SMILES, and enter a value. Click "Add Ligand".

Constraints Tab: Choose a binder (ligand ID with type/value), add chain-residue contacts, and finalize each constraint.

Generate YAML: Click "Generate YAML" to save config.yaml and view the output.

Output:
The generated config.yaml file will be saved in the project directory.

Requirements
Python 3.6+

PyYAML (pip install pyyaml)

Tkinter (usually included with Python)

Contributing
Feel free to fork this repo, submit pull requests, or open issues for bugs/features. To contribute:
Fork the repository.

Create a new branch:
bash

git checkout -b feature/your-idea

Commit your changes:
bash

git commit -m "Add your message"

Push to your branch:
bash

git push origin feature/your-idea

Open a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details (add one if you want!).
Contact
GitHub: JustABiologist

Email: [your-email@example.com (mailto:your-email@example.com)] (optional)

Happy YAML building!

