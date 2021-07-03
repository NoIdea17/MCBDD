from chembl_webresource_client.new_client import new_client

molecule = new_client.molecule


#res = molecule.search('viagra')
#print(res)
'''
#get all approved drugs by Year
approved_drugs_byYear = molecule.filter(max_phase=4).order_by('first_approval')

print(len(approved_drugs_byYear))
      
f = open('drugs_by_year.txt','w')
for x in approved_drugs_byYear:
    f.write(u'%s\n' % x)
f.close()


#get all approved drugs by Name and Year
approved_drugs_byName = molecule.filter(max_phase=4).order_by('pref_name', 'first_approval')

#print(len(approved_drugs_byName))
      
f = open('drugs_by_name.txt','w')
for x in approved_drugs_byName:
    f.write(u'%s\n' % x)
f.close()
'''

#get all approved drugs since 2011
approved_drugs_since2011 = molecule.filter(first_approval__gte=2011).order_by('first_approval')

f = open('drugs_since_2011.txt','w')
for x in approved_drugs_since2011:
    f.write(u'%s\n' % x)
f.close()
print("First approval 2011:" + str(len(approved_drugs_since2011)))

