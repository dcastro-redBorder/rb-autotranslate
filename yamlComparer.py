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

def compare_keys(dict1, dict2, parent_key=''):
    """
    Compares the keys of two dictionaries and their nested dictionaries,
    returning the differences in keys between them.
    """
    differences1 = {}
    differences2 = {}

    # Extract keys from both dictionaries
    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())

    # Compare keys in dict1 with dict2
    for key in keys1:
        subkeys1 = set(dict1[key].keys())
        if key in keys2:
            subkeys2 = set(dict2[key].keys())
            for subkey in subkeys1:
                if subkey not in subkeys2:
                    differences1.setdefault(key, set()).add(subkey)
        else:
            differences1[key] = subkeys1

    # Compare keys in dict2 with dict1
    for key in keys2:
        subkeys2 = set(dict2[key].keys())
        if key in keys1:
            subkeys1 = set(dict1[key].keys())
            for subkey in subkeys2:
                if subkey not in subkeys1:
                    differences2.setdefault(key, set()).add(subkey)
        else:
            differences2[key] = subkeys2

    return differences1, differences2

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
    differences, differences2 = compare_keys(yaml1, yaml2)
    if differences:
        print("Exclusive to", file1Path, ":", differences)
    else:
        print("Nothing to different in", file1Path)
    if differences2:
        print("Exclusive to", file2Path, ":", differences2)
    else:
        print("No differences found in", file2Path)
    #translateFile()
    

if __name__ == "__main__":
    #CHANGE THESE TO YOUR FILES PATHS
    file1Path = 'en.yml'
    file2Path = 'es.yml'
    main(file1Path, file2Path)