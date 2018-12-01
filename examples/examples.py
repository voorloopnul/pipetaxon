import requests


# Get a taxonomy from pipetaxon.voorloop.com anonymously
#

response = requests.get('http://pipetaxon.voorloop.com/api/taxonomy/4373')
print(response.json())


# Get a taxonomy from pipetaxon.voorloop.com using a token ( http://pipetaxon.voorloop.com/register/ )
#

token = 'Token 2ea7fa00-YOUR-REAL-KEY-HERE-bc2aa7caf531'
response = requests.get('http://pipetaxon.voorloop.com/api/taxonomy/4373', headers={'Authorization': token})
print(response.json())


# Get a taxonomy from your local pipetaxon instance
#

response = requests.get('http://localhost:8000/api/taxonomy/4373')
print(response.json())


# Retrieve the lineage of taxid 4373
#

response = requests.get('http://pipetaxon.voorloop.com/api/taxonomy/4373/lineage')
print(response.json())

# Get all taxonomies at rank 'Order'
#

response = requests.get('http://pipetaxon.voorloop.com/api/taxonomy/?rank=order')
print(response.json())


# Get all taxonomies at division 4
#

response = requests.get('http://pipetaxon.voorloop.com/api/taxonomy/?division=4')
print(response.json())


# Search for taxonomies named *Clostridium*
#

response = requests.get('http://pipetaxon.voorloop.com/api/taxonomy/?search=clostridium')
print(response.json())


# Execute an LCA query on a taxid list
#

response = requests.get('http://pipetaxon.voorloop.com/api/taxonomy/lca/?taxid_list=2363,37487,87346')
print(response.json())
