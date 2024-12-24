import yaml
import os
import requests

def load_yaml(file_path):
    if not os.path.exists(file_path):
        answer = ""
        while answer not in ("Y", "N"):
            answer = input(f"File {file_path} doesn't exist, do you want to create it? (Y/N): ").capitalize()
        if answer == "Y":
            try:
                with open(file_path, "x") as file:
                    pass
                print(f"File '{file_path}' created successfully.")
            except Exception as e:
                raise RuntimeError(f"Failed to create file '{file_path}': {e}")
        elif answer == "N":
            print("Exiting script.")
            exit()
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise RuntimeError(f"Failed to load {file_path}: {e}")
    
def compare_keys(file1, file2, dict1, dict2):

    dict1_keys = {normalize_key(key): value for key, value in iterate_dict_recursively(dict1)}
    dict2_keys = {normalize_key(key): value for key, value in iterate_dict_recursively(dict2)}
    missing_in_dict1 = {key: dict2_keys[key] for key in dict2_keys.keys() - dict1_keys.keys()}
    missing_in_dict2 = {key: dict1_keys[key] for key in dict1_keys.keys() - dict2_keys.keys()}

    print(f"\nKeys missing in {file1}:")
    for key in missing_in_dict1:
        print(f"- {key}")
    targetLanguage = file1.split(".")[0]
    translateFile(file2, file1, missing_in_dict1, targetLanguage)
    
    print(f"\nKeys missing in {file2}:")
    for key in missing_in_dict2:
        print(f"- {key}")
    targetLanguage = file2.split(".")[0]
    translateFile(file1, file2, missing_in_dict2, targetLanguage)


def iterate_dict_recursively(d, parent_key=""):
    try:
        for key, value in d.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                yield from iterate_dict_recursively(value, full_key)
            else:
                yield full_key, value
    except Exception as e:
        return

def normalize_key(full_key):
    parts = full_key.split(".", 1)
    return parts[1] if len(parts) > 1 else full_key

def translateFile(file1, file2, missing_in_dict, targetLanguage):
    answer = ""
    if missing_in_dict:
        while answer not in ("Y", "N"):
            answer = input("Do you want to translate it from " + file1 + "? (Y/N): ").capitalize()
        if answer == "Y":
            print("Translating file...")
            try:
                with open(file2, "r", encoding="utf-8") as f:
                    existing_data = yaml.safe_load(f) or {}
            except FileNotFoundError:
                existing_data = {}
            if targetLanguage not in existing_data:
                existing_data[targetLanguage] = {}
            
            formatted_dict = {}
            for missingKey, value in missing_in_dict.items():
                translatedValue = translate_text_deepl(value, targetLanguage)
                print(f"{missingKey} : {translatedValue}")
                format_dict(formatted_dict, missingKey, translatedValue)

            existing_data[targetLanguage] = merge_dicts(existing_data.get(targetLanguage, {}), formatted_dict)

            with open(file2, "w", encoding="utf-8") as f:
                yaml.dump(
                    existing_data,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                )
            return True
        elif answer == "N":
            print("Not translated.")
            return False
    else:
        print("Nothing to translate!")
        return False

def translate_text_deepl(text, target_language):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": "INSERT YOUR API KEY",
        "text": text,
        "target_lang": target_language.upper()
    }
    
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    else:
        raise Exception(f"DeepL API error: {response.status_code}, {response.text}")
    
def format_dict(formatted_dict, dotted_key, value):
    parts = dotted_key.split(".")
    current = formatted_dict
    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]
    current[parts[-1]] = value

def merge_dicts(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            merge_dicts(dict1[key], value)
        else:
            dict1[key] = value
    return dict1

def main(file1, file2):
    yaml1 = load_yaml(file1)
    yaml2 = load_yaml(file2)
    compare_keys(file1, file2, yaml1, yaml2)

if __name__ == "__main__":
    #CHANGE THESE TO YOUR FILES PATHS
    file1Path = 'en.yml'
    file2Path = 'zh.yml'
    main(file1Path, file2Path)