#Written by BSc. Gabriel Jimenez-Avalos for the Zimic-Sheen lab
#This script continues the vina's virtual screening from where it left off
import glob
import os
import subprocess

ligands = glob.glob('pdbqts/*.pdbqt')
ligand_filenames = [os.path.basename(x) for x in ligands]
ligand_basenames = []

for ligand_filename in ligand_filenames:
    ligand_basename = ligand_filename.replace('.pdbqt','')
    ligand_basenames.append(ligand_basename)

results = glob.glob('results/*.pdbqt')
results_filenames = [os.path.basename(x) for x in results]

results_basenames = []

for result_filename in results_filenames:
    result_basename = result_filename.replace('r.pdbqt','')
    results_basenames.append(result_basename)

for ligand in ligand_basenames:
    if ligand in results_basenames:
        pass
    else:
        subprocess.call ('vina --config config.dat --ligand pdbqts/' 
                         + ligand +'.pdbqt --out results/' + ligand + 'r.pdbqt --log logs/' + ligand 
                         + 'r.log --cpu 4 --exhaustiveness 20', shell = True)
