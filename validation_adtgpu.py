#Written by Bsc. Gabriel Jimenez-Avalos for the "Ropon-Palacios lab"
#This script performs a validation docking with autodock-GPU, using the results generated by the "vs.py" script. 
#IMPORTANT: pythonsh and prepare_gpf4.py have to be in the same directory as this script

import pandas as pd
import subprocess
import os
import re
import fileinput
import math

gridcenter = input('enter the gridcenter: ')
npts = input ('enter the number of points: ')

top1000 = pd.read_csv ('top1000.csv', index_col = False, skipinitialspace=True)
templist = top1000['compound'].tolist()
hits = templist[0:100]

for hit in hits:
    subprocess.call ('mkdir ' + hit, shell = True)
    subprocess.call('cp receptor.pdbqt ' + hit + '/', shell = True)
#    subprocess.call('cp prepare_dpf4.py ' + hit + '/', shell = True)
    subprocess.call('cp prepare_gpf4.py ' + hit + '/', shell = True)
#    subprocess.call('cp pythonsh ' + hit + '/', shell = True)
    subprocess.call('cp ../pdbqts/' + hit.replace('r','') + '.pdbqt ' + hit + '/', shell = True)
    
for hit in hits:
    os.chdir(hit + '/')
    subprocess.call('pythonsh prepare_gpf4.py -l ' + hit.replace('r','') + 
                    '.pdbqt -r receptor.pdbqt -p gridcenter=' + gridcenter + ' -p npts=' + npts +
                     ' -p spacing=0.375 -o grid_map.gpf', shell = True)
    subprocess.call('autogrid4 -p grid_map.gpf -l grid_map.glg', shell = True)
    subprocess.call('autodockgpu -ffile receptor.maps.fld -lfile ' + hit.replace('r','') +
                    '.pdbqt -nev 25000000 -nrun 150 -psize 350', shell = True)
    os.chdir('..')
    
for hit in hits:
    print(hit)
    os.chdir(hit + '/')
    with open('docking.dlg', 'r') as docking:
        lines = docking.readlines()
        i = 0
        for line in lines:
            if re.search(r'CLUSTERING HISTOGRAM',line):
                clusfirst = i + 10
                break
            else:
                i = i + 1
        i = 0
        for line in lines:
            if re.search(r'RMSD TABLE',line):
                clusend = i - 4
                break
            else:
                i = i + 1
        rmsdfirst = clusend + 14
        i = 0
        for line in lines:
            if re.search(r'Run time',line):
                rmsdend = i  - 2
                break
            else:
                i = i + 1
        with open('raw_clustable.txt', 'a+') as raw_clustable:
            for line in lines[clusfirst:clusend+1]:
                raw_clustable.write(line)
        with open('raw_rmsdtable.txt','a+') as raw_rmsdtable:
            for line in lines[rmsdfirst:rmsdend+1]:
                raw_rmsdtable.write(line)
    with fileinput.FileInput('raw_clustable.txt', inplace=True, backup='.bak') as infile:
        for line in infile:
            print(line.replace('|',''), end='')
    with fileinput.FileInput('raw_clustable.txt', inplace=True, backup='.bak') as infile:
        for line in infile:
            print(line.replace('#',''),end='')
    with fileinput.FileInput('raw_rmsdtable.txt', inplace=True, backup='.bak') as infile:
        for line in infile:
            print(line.replace('|',''), end='')
    clustable = pd.read_table('raw_clustable.txt',delim_whitespace = True, header=None,index_col=False,names=['cluster','lbe','run','mbe','clustpop'])
    rmsdtable = pd.read_table('raw_rmsdtable.txt', delim_whitespace = True, header=None,index_col=False, names = ['rank', 'subrank', 'run','be',
                                                        'clustrmsd','refrmsd'])
    clustable.to_csv('clustable.csv', index = False)
    rmsdtable.to_csv('rmsdtable.csv', index = False)
    
#    clusters = rmsdtable['rank'].tolist()
#    clustpop = []
#    for cluster in clusters:
#       clustpop.append(int(clustable[clustable['cluster'] == cluster]['clustpop']))
    redock = clustable
#    redocksumm['clustpop'] = clustpop
    redock['normpop'] = (redock['clustpop'] - redock['clustpop'].mean())/(redock['clustpop'].std())
    redock['normbe'] = (redock['mbe'] - redock['mbe'].mean())/(redock['mbe'].std())
    redock['2dscore'] = redock['normpop'] - redock['normbe']
    redock['ligand'] = hit
    redock_sorted = redock.sort_values(by = ['2dscore'], ascending = False)
    redock_sorted.to_csv('redocksumm_sorted.csv', index = False)
    os.chdir('..')

with open('allredocksum.csv', 'a+') as allredocksum:
    allredocksum.write('cluster,lbe,run,mbe,clustpop,normpop,normbe,2dscore,ligand\n')
    for hit in hits:
        os.chdir(hit + '/')
        with open ('redocksumm_sorted.csv','r') as infile:
            lines = infile.readlines()
            allredocksum.write(lines[1])
        os.chdir('..')
allredocksum = pd.read_csv('allredocksum.csv', index_col=False)
allredocksum_sorted = allredocksum.sort_values(by = ['mbe'])
BindingEnergies = allredocksum_sorted.mbe.tolist()
Kds_nM = []
for BindingEnergy in BindingEnergies:
    Kd_nM = math.exp((BindingEnergy*1000)/(1.98*298.15))*1000000000
    Kds_nM.append(Kd_nM)
allredocksum_sorted['Kds_nM'] = Kds_nM
allredocksum_sorted.to_csv('allredocksum.csv', index = False)
print('Thats\'s all folks')
