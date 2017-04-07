import os, sys
import requests
from prody import *
from xml.etree.ElementTree import fromstring
from sys import argv

if not os.path.isdir("./ProteinsMSAs/"):
		os.makedirs("./ProteinsMSAs/")

cmplx = list()
pdb_id_1 = list()
pdb_id_2 = list()

print "Enter the number of pairs:"
total = input()

for x in range(0, total):
	print "Pair no. " + str(x+1)
	cmplx.append(raw_input("Enter complex id:"))
	pdb_id_1.append(raw_input("Enter pdbid 1:"))
	pdb_id_2.append(raw_input("Enter pdbid 2:"))

for x in range(0, total):
	pdb_mapping_url = 'http://www.rcsb.org/pdb/rest/das/pdb_uniprot_mapping/alignment'
	uniprot_url = 'http://www.uniprot.org/uniprot/{}.xml'

	def get_uniprot_accession_id(response_xml):
		root = fromstring(response_xml)
		return next(
			el for el in root.getchildren()[0].getchildren()
			if el.attrib['dbSource'] == 'UniProt'
		).attrib['dbAccessionId']

	def get_uniprot_protein_name(uniport_id):
		uinprot_response = requests.get(
			uniprot_url.format(uniport_id)
		).text
		return fromstring(uinprot_response).find(
			'.//{http://uniprot.org/uniprot}recommendedName/{http://uniprot.org/uniprot}fullName'
		).text

	def map_pdb_to_uniprot(pdb_id):
		pdb_mapping_response = requests.get(
			pdb_mapping_url, params={'query': pdb_id}
		).text
		target = open('mapping+', 'a+')
		uniprot_id = get_uniprot_accession_id(pdb_mapping_response)
		uniprot_name = get_uniprot_protein_name(uniprot_id)
		target.write(pdb_id)
		target.write("\t")
		target.write(uniprot_id)
		target.write("\t")
		target.write(uniprot_name)
		target.write("\n")
		target.close()
		return pdb_id, uniprot_id, uniprot_name

	if not os.path.isdir('./data1/'+cmplx[x]):
		os.makedirs('./data1/'+cmplx[x])
	pdb_id, uniprot_id, uniprot_name = map_pdb_to_uniprot(pdb_id_1[x])
	Pfam_id = searchPfam(uniprot_id).keys()[0]
	print "Downloading MSA for ", Pfam_id 
	try:
		fetchPfamMSA(Pfam_id, folder='./data1/'+cmplx[x], order='alphabetical', format='stockholm')
	except Exception as e: 
		print str(e)

	pdb_id, uniprot_id, uniprot_name = map_pdb_to_uniprot(pdb_id_2[x])
	Pfam_id = searchPfam(uniprot_id).keys()[0]
	print "Downloading MSA for ", Pfam_id 
	try:
		fetchPfamMSA(Pfam_id, folder='./data1/'+cmplx[x], order='alphabetical', format='stockholm')
	except Exception as e: 
		print str(e)


	
	
	
