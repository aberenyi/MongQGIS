from pymongo import MongoClient


def get_var(input_dict, accessor_string):
    """Gets data from a dictionary using a dotted accessor-string"""
    current_data = input_dict
    for chunk in accessor_string.split('.'):
        current_data = current_data.get(chunk, {})
    return current_data

client = MongoClient('localhost', 27017)
dbs = client.database_names()
print dbs
db = client['animus']
print db.collection_names()
coll = db['positions']
idxs = coll.index_information();
print idxs
fields = [key for key in idxs]
for field in fields:
    idx = idxs[field]['key'][0]
    if idx[1] == '2d':
        field = idx[0]
        print '-->' + field
        doc = db['positions'].find_one()
        if doc is not None:
            geo = get_var(doc, 'geom.coordinates')
            print geo