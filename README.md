# Redborder YAML Translation Tool

This project provides a script for comparing and translating Redborder YAML files while ensuring hierarchical structures are preserved and merged correctly. It is designed to handle nested dictionaries and integrate with the DeepL API for language translation.

---

## Requirements

- Python 3.x
- Pip
- Libraries:
  - `pyyaml`
  - `requests`
- DeepL API key

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/yaml-translation-tool.git
   cd yaml-translation-tool
   ```

2. Install the required dependencies:
   ```bash
   pip install pyyaml requests
   ```

3. Register in DeepL and paste your API key in the line 102 of the yamlComparer.py script:
   ```bash
   "auth_key": "INSERT YOUR API KEY"
   ```
---

## Usage

1. **Prepare Your YAML Files**:
   - Place the script in the same directory as your .yaml files or edit the script file paths to match the path to your .yaml files.
  
2. **Select both languages**:
   - In the line 138 and 139 of the script you can change the languages you want to translate from and to.
   ```python
    file1Path = 'en.yml'
    file2Path = 'es.yml'
   ```

4. **Run the Script**:
   ```bash
   python yamlComparer.py
   ```

5. **Translation Workflow**:
   - The script will:
     1. Load the two YAML files.
     2. Compare the keys between them.
     3. Prompt you to translate missing keys.
     4. Write the updated translations back into the target YAML file.

## License

This project is licensed under the MIT License.
