#Written by BSc. Gabriel Jimenez-Avalos for the Zimic-Sheen lab
#This script summarizes the virtual screening results from autodock's vina log's files inside the subfolder "logs"
import pandas as pd
import glob
import os
import math

logs = glob.glob('logs/*.log')
logs_filenames = [os.path.basename(x) for x in logs]
logs_basenames = []

for log_filename in logs_filenames:
    log_basename = log_filename.replace('.log','')
    logs_basenames.append(log_basename)

summary = open('summary', 'a+')
for log in logs_basenames:
    infile = open('logs/' + log + '.log', 'r')
    lineslist = infile.readlines()
    summary.write(log + '      ' +  lineslist[25])
    infile.close()
summary.close()

header = ["compound","mode","BindingEnergy", "rmsdlb", "rmsdub"]
summarydf = pd.read_table('summary', names = header,delim_whitespace = True)
BindingEnergies = summarydf.BindingEnergy.tolist()
Kds_nM = []

for BindingEnergy in BindingEnergies:
    Kd_nM = math.exp((BindingEnergy*1000)/(1.98*298.15))*1000000000
    Kds_nM.append(Kd_nM)
Kds_nMdf = pd.DataFrame ({'Kd_nM': Kds_nM})

summaryfinal = pd.concat([summarydf, Kds_nMdf], axis = 1)
summaryfinal.to_csv('summaryfinal.csv')
summary_sorted = summaryfinal.sort_values(by = ['BindingEnergy'])
summary_sorted.to_csv('summaryfinal_sorted.csv', index = False)
top1000 = summary_sorted.head(1000)
top1000.to_csv('top1000.csv', index = False)

