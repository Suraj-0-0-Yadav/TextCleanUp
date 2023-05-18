import json
with open('./data/abbreviations.json','r') as f:
    abb = json.load(f)

print(type(abb))