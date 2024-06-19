import json, os

def admin(arg):
    with open(f'./users/{arg}.json') as f:
        data = json.load(f)

        return data['admin']