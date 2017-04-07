import os, sys
import requests
from Bio import AlignIO
from prody import *

def get_immediate_subdirectories(a_dir):
	return [name for name in os.listdir(a_dir)
			if os.path.isdir(os.path.join(a_dir, name))]

raw_data_folder = "/home/madhav/CBP/CDS_MSAs/"
output_folder = "/home/madhav/CBP/Combined_CDSMSAs/"

if not os.path.exists(output_folder):
	os.makedirs(output_folder)

folder_lists = get_immediate_subdirectories(raw_data_folder)
for sub_folder in folder_lists:
	newloc = raw_data_folder+sub_folder+"/"
	filenames = list(os.listdir(newloc))
	if len(filenames) == 2:
		for filename in filenames:
			with open(newloc+filename, "rU") as handle:
				for records in list(AlignIO.read(handle, "fasta"))[0:10]:
					print records.id