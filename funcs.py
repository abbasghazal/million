import json

def write(file_path, data):
    
    with open(file_path, "w") as jsonfile:
        json.dump(data, jsonfile, indent=2)
        
def read(file_path):
    
    with open(file_path, "r") as jsonfile:
        return json.load(jsonfile)