import yaml
import os

def load_yaml(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Failed to load {file_path}: {e}")
        return None
    
def compare_keys(dict1, dict2):
    """
    Compare the keys of two dictionaries, including nested dictionaries, and find:
    - Keys missing in each dictionary.
    - Keys present in both but with a None value in one of them.
    """
    # Normalize and collect all keys and values from both dictionaries
    dict1_keys = {normalize_key(key): value for key, value in iterate_dict_recursively(dict1)}
    dict2_keys = {normalize_key(key): value for key, value in iterate_dict_recursively(dict2)}

    # Find keys that are in one dictionary but not the other
    missing_in_dict1 = dict2_keys.keys() - dict1_keys.keys()
    missing_in_dict2 = dict1_keys.keys() - dict2_keys.keys()

    # Print the results
    print("Keys missing in dict1:")
    for key in missing_in_dict1:
        print(f"- {key}")
    
    print("\nKeys missing in dict2:")
    for key in missing_in_dict2:
        print(f"- {key}")
        
def iterate_dict_recursively(d, parent_key=""):
    for key, value in d.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            yield from iterate_dict_recursively(value, full_key)
        else:
            yield full_key, value

def normalize_key(full_key):
    parts = full_key.split(".", 1)
    return parts[1] if len(parts) > 1 else full_key

def translateFile():
    answer = input("Do you want to translate" + file2Path + "to" + file1Path + "? (Y/N):").capitalize()
    while answer != "Y" and answer != "N":        
        answer = input("Do you want to translate" + file2Path + "to" + file1Path + "? (Y/N):").capitalize
    if answer == "Y":
        #TODO translate file
        print("Translating file...")
    elif answer == "N":
        print("Tsk, why do you even bother me then...")

def main(file1, file2):
    yaml1 = load_yaml(file1)
    yaml2 = load_yaml(file2)
    if yaml1 is None or yaml2 is None:
        print("Error loading YAML files.")
        return
    compare_keys(yaml1, yaml2)
    #translateFile()

if __name__ == "__main__":
    #CHANGE THESE TO YOUR FILES PATHS
    file1Path = 'en.yml'
    file2Path = 'es.yml'
    main(file1Path, file2Path)