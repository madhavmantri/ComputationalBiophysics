import os, sys
import requests
from Bio import AlignIO
from prody import *

def get_immediate_subdirectories(a_dir):
	return [name for name in os.listdir(a_dir)
			if os.path.isdir(os.path.join(a_dir, name))]

raw_data_folder = "/home/madhav/CBP/ProteinsMSAs/"
output_folder = "/home/madhav/CBP/Combined_ProteinsMSAs/"

if not os.path.exists(output_folder):
	os.makedirs(output_folder)

folder_lists = get_immediate_subdirectories(raw_data_folder)
for sub_folder in folder_lists:
	newloc = raw_data_folder+sub_folder+"/"
	filenames = list(os.listdir(newloc))
	if len(filenames) == 2:
		try:
			filename = raw_data_folder+sub_folder+'/'+filenames[0]
			msa1 = parseMSA(filename, format = "fasta")
		except Exception as e: 
			print str(e)
		try:
			filename = raw_data_folder+sub_folder+'/'+filenames[1]
			msa2 = parseMSA(filename, format = "fasta")
		except Exception as e: 
			print str(e)
		try:
			merged = mergeMSA(msa1, msa2)
			# filename = output_folder+sub_folder+'.fasta'
			# writeMSA(filename, merged, format='fasta')
			filename = output_folder+sub_folder+'.sth'
			writeMSA(filename, merged, format='Stockholm')
		except Exception as e: 
			print str(e)
