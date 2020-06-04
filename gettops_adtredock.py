#Written by BSc. Gabriel Jimenez-Avalos for the "Ropon-Palacios" lab.
#This script creates complexes (Protein-Ligand) of the 10 best compounds based on the results of the "redocking_adtgpu.py" tool
from pymol import cmd
import subprocess
import pandas as pd
import os

subprocess.call('mkdir top10complexes', shell = True)
allredocksum = pd.read_csv('allredocksum.csv')
templist = allredocksum['ligand'].tolist()
top10 = templist[0:10]

for i in top10:
    os.chdir(i)
    subprocess.call('grep \'^DOCKED\' *.dlg | cut -c9- > ligand_out.pdbqt', 
                    shell = True)
    cmd.load('ligand_out.pdbqt', multiplex = 1)
    run = int(allredocksum[allredocksum['ligand'] == i]['run']) 
    if len(str(run)) == 1:
        cmd.delete('!'+'ligand_out_' + '000' + str(run))
    if len(str(run)) == 2:
        cmd.delete('!'+'ligand_out_' + '00' + str(run))
    if len(str(run)) == 3:
        cmd.delete('!'+'ligand_out_' + '0' + str(run))
    cmd.load('../receptor.pdbqt')
    cmd.save('../top10complexes/complex_' + i + '.pdb')
    cmd.delete('all')
    os.chdir('..')
