#Adapted from PhD(c). Ropon-Palacios, G. by BSc. Gabriel Jimenez-Avalos
#This script generates 3D structures of small-drug compounds from its smiles registered in a ".csv" database

import pandas as pd
import glob
import os
import subprocess

df = pd.read_csv('finaldb.csv') # replace the empty string with the csv you want to process
id = df.ID.tolist() # csv has to have a col named id
smiles = df.Smiles.tolist() # csv has to have a col named smiles 

i=0

subprocess.call('mkdir smiles', shell = True)
subprocess.call('mkdir 2D', shell = True)
subprocess.call('mkdir 3Dsdf', shell = True)
subprocess.call('mkdir 3Dpsdf', shell = True)
subprocess.call('mkdir 3Dpsdf_min', shell = True)
subprocess.call('mkdir 3Dppdb_min', shell = True)
subprocess.call('mkdir pdbqts', shell = True)

for smile in smiles:
    outfile = open('smiles/'+str(id[i])+'.smi','w')
    outfile.write(str(smile))
    outfile.close()
    i = i + 1

ligands = glob.glob('2D/*.sdf')
ligands_filenames = [os.path.basename(x) for x in ligands]
ligands_basenames = []

for ligand_filename in ligands_filenames:
    ligand_basename = ligand_filename.replace('.sdf','')
    ligands_basenames.append(ligand_basename)

for ligand in ligands_basenames:
    print('generating 2d structure of ' + ligand)
    subprocess.call('obabel ' + ' smiles/' + ligand + '.smi -O 2D/' + ligand + '.sdf --gen2D', shell = True)

for ligand in ligands_basenames:
    print ('generating 3d structure of ' + ligand)
    subprocess.call('obabel ' + ' 2D/' + ligand + '.sdf -O 3Dsdf/' + ligand + '.sdf --gen3D', shell = True)

for ligand in ligands_basenames:
    print('protoning at pH of 7.4 ' + ligand)
    subprocess.call('obabel ' + ' 3Dsdf/' + ligand + '.sdf -O 3Dpsdf/' + ligand + '.sdf -p 7.4', shell = True)

for ligand in ligands_basenames:
    print('minimizing ' + ligand)
    subprocess.call('obminimize -o sdf -ff MMFF94 -n 25000 -sd -c 1e-7 ' + '3Dpsdf/' + ligand + '.sdf > ' + '3Dpsdf_min/' + ligand + 'min.sdf', shell = True)

for ligand in ligands_basenames:
    print('converting ' + ligand + ' to pdb')
    subprocess.call('obabel ' + ' 3Dpsdf_min/' + ligand + 'min.sdf -O 3Dppdb_min/' + ligand + 'min.pdb', shell = True)

for ligand in ligands_basenames:
    print('converting ' + ligand + ' to pdbqt')
    subprocess.call('pythonsh prepare_ligand4.py -l' + ' 3Dppdb_min/' + ligand + 'min.pdb -o pdbqts/' + ligand + 'min.pdbqt', shell = True)
