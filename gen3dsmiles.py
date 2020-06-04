#Adapted from PhD(c). Ropon-Palacios, G. by BSc. Gabriel Jimenez-Avalos
#This script generates 3D structures of small-drug compounds from its smiles registered in a ".csv" database

import pandas as pd
import glob
import os
import subprocess

df = pd.read_csv('*.csv') # replace the empty string with the csv you want to process
id = df.ID.tolist() # csv has to have a col named id
smiles = df.Smiles.tolist() # csv has to have a col named smiles 

i=0

subprocess.call('mkdir 2D', shell = True)
subprocess.call('mkdir prepre3D', shell = True)
subprocess.call('mkdir pre3D', shell = True)
subprocess.call('mkdir pre3D_min', shell = True)
subprocess.call('mkdir pdbqts', shell = True)
subprocess.call('mkdir smiles', shell = True)
subprocess.call('mkdir 3D_min', shell = True)

for smile in smiles:
    outfile = open('smiles/'+str(id[i])+'.smi','w')
    outfile.write(str(smile))
    outfile.close()
    i = i + 1

ligands = glob.glob('smiles/*.smi')
ligands_filenames = [os.path.basename(x) for x in ligands]
ligands_basenames = []

for ligand_filename in ligands_filenames:
    ligand_basename = ligand_filename.replace('.smi','')
    ligands_basenames.append(ligand_basename)

for ligand in ligands_basenames:
    print('generating 2d structure of ' + ligand)
    subprocess.call('obabel ' + ' smiles/' + ligand + '.smi -O 2D/' + ligand + '.sdf --gen2D', shell = True)

for ligand in ligands_basenames:
    print ('generating 3d structure of ' + ligand)
    subprocess.call('obabel ' + ' 2D/' + ligand + '.sdf -O prepre3D/' + ligand + '.sdf --gen3D', shell = True)

for ligand in ligands_basenames:
    print('protoning at pH of 7.4 ' + ligand)
    subprocess.call('obabel ' + ' prepre3D/' + ligand + '.sdf -O pre3D/' + ligand + '.sdf -p 7.4', shell = True)

for ligand in ligands_basenames:
    print('minimizing ' + ligand)
    subprocess.call('obminimize -o sdf -ff MMFF94 -n 25000 -sd -c 1e-7 ' + 'pre3D/' + ligand + '.sdf > ' + 'pre3D_min/' + ligand + 'min.sdf', shell = True)

for ligand in ligands_basenames:
    print('converting ' + ligand + ' to pdb')
    subprocess.call('obabel ' + ' pre3D_min/' + ligand + 'min.sdf -O 3D_min/' + ligand + 'min.pdb', shell = True)

for ligand in ligands_basenames:
    print('converting ' + ligand + ' to pdbqt')
    subprocess.call('pythonsh prepare_ligand4.py -l' + ' 3D_min/' + ligand + 'min.pdb -o pdbqts/' + ligand + 'min.pdbqt', shell = True)


