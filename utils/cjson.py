import json, os

def load(arg):
    with open(f'./users/{arg}.json', 'r') as f:
        data = json.load(f)

    return data

def loaduser(arg):
    for file in os.listdir('./users'):
        with open(f'./users/{file}', 'r') as f:
            data = json.load(f)

            if data['username'] == arg:
                return data
            
def dump(data):
    with open(f'./users/{data["id"]}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)