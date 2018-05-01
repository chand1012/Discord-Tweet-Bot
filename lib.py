from json import loads

def get_keys(filename="keys.json"):
    parsed = None
    with open(filename) as keyfile:
        raw = keyfile.read()
        parsed = loads(raw)
    return parsed
   
def get_list(filename="list.txt"):
    clist = []
    with open(filename) as listfile:
        clist = listfile.readlines()
    return clist