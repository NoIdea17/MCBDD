from chembl_webresource_client.new_client import new_client
import requests, json
import pandas as pd

drugs = new_client.drug

#could not recreate this function, which is why we had to use the reference
def get_INN(drug: list):
    """returns INN name, use ; as concatenator if more than one value is available"""
    inn = [x['molecule_synonym'] for x in drug['molecule_synonyms'] if x['syn_type'] == 'INN']
    res = ';'.join(inn)
    return(res)

years = []
names = []
ids = []

for x in drugs:
    years.append(x['first_approval'])
    names.append(get_INN(x)) 
    ids.append(x['molecule_chembl_id'])
  

dataFrame1 = pd.DataFrame({'ID':ids, 'Name':names, 'FirstApproval':years})
dataFrame1.sort_values(by=['Name', 'FirstApproval'], axis=0, inplace=True)

approved_2011 = dataFrame1.query('FirstApproval >= 2011').sort_values(by='FirstApproval', axis=0)

#Print out drugs retreived from DB above
print("Drugs approved since 2011:" + str(len(approved_2011)) + "\n") 



#Adjust number for amount of drugs - we were not able to implement the usage of "chunks" by ourselves, which is why we left it out
drugs_to_query = approved_2011.ID[0:10]

component2target = dict()
for drug in drugs_to_query:
    component2target[drug] = set()

keys = list(component2target.keys())

activities = new_client.activity.filter(molecule_chembl_id__in=keys).only(['molecule_chembl_id', 'target_chembl_id'])

for activity in activities:
    component2target[activity['molecule_chembl_id']].add(activity['target_chembl_id'])

for key, value in component2target.items():

    val_list = list(value)
    uniprots = set()
    targets = new_client.target.filter(target_chembl_id__in=val_list).only(['target_components'])
    uniprots = {component['accession'] for t in targets for component in t['target_components']}
    component2target[key] = uniprots

#Put results in DataFrame
component2target_df = pd.DataFrame([(i, uniprot) for i, j in component2target.items() for uniprot in j], columns=['ID','UniProt'])


#FOR MEDIAN CALCULATION
col_one_list = component2target_df['ID'].tolist()
counter = {i:col_one_list.count(i) for i in col_one_list}
print(counter)


uniq_uniprot = set(component2target_df.UniProt)
sel_uniprot = list(uniq_uniprot)[:100]          #did not understand this part of the code to be honest, so we had to copy
sel_uniprot_queryid = ','.join(sel_uniprot)

url = 'https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&accession='+sel_uniprot_queryid
r = requests.get(url, headers={'Accept': 'application/json'})


#get keys, sort them and print them out by number of appearances, the highest is at the bottom
keys=[]
for list_json in r.json():
    for k in list_json['keywords']:
        keys.extend([list(k.values())[0]])
        
numbers = {i:keys.count(i) for i in keys}

sort_numbers = sorted(numbers.items(), key=lambda x: x[1])

for i in sort_numbers:
	print(i[0], i[1])




