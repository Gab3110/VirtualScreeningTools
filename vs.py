#Written by BSc. Gabriel Jimenez-Avalos for the Zimic-Sheen lab
#This script performs molecular docking with autodock vina of ligands inside the folder "pdbqts"
import glob
import os
import subprocess

subprocess.call('mkdir results', shell = True)
subprocess.call('mkdir logs', shell = True)

ligands = glob.glob('pdbqts/*.pdbqt')
ligands_filenames = [os.path.basename(x) for x in ligands]
ligands_basenames = []

for ligand_filename in ligands_filenames:
    ligand_basename = ligand_filename.replace('.pdbqt','')
    ligands_basenames.append(ligand_basename)

for ligand in ligands_basenames:
    subprocess.call ('vina --config config.dat --ligand pdbqts/' + ligand +'.pdbqt --out results/' + ligand + 'r.pdbqt --log logs/'
                     + ligand + 'r.log --exhaustiveness 24', shell = True)
