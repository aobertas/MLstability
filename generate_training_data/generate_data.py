import rebound
import numpy as np
from subprocess import call
import sys
import warnings
warnings.filterwarnings('ignore') # to suppress warnings about REBOUND versions that I've already tested

datapath = '/mnt/ssd/workspace/stability/stabilitydataset/data/'
repopath = '/mnt/ssd/workspace/stability/MLstability/'
sys.path.append(repopath + 'generate_training_data/')
from training_data_functions import gen_training_data, runorbtseries

Norbits = 1e4
Nout = 1729
datasets = 'all'
runfunc = runorbtseries

gendatafolder = repopath + 'generate_training_data/'
foldername = runfunc.__name__ + 'Norbits' + '{:.1e}'.format(Norbits) + 'Nout' + str(Nout)

already_exists = call('mkdir ' + gendatafolder + foldername, shell=True)
if not already_exists: # store a copy of this script in generate_data so we can always regenerate what we had
    call('cp ' + gendatafolder + '/generate_data.py ' + gendatafolder + foldername, shell=True)
    call('python ' + gendatafolder + foldername + '/generate_data.py ', shell=True)
    exit()
    # we always run the copied script so that we do the same thing whether we're running for first time or regenerating
# if it does exist don't overwrite since we don't want to overwrite history

def allsystems():
    return ['random', 'resonant'] + ttvsystems()

def ttvsystems():
    folders = ['Kepler-431', 'KOI-0115', 'KOI-0168', 'EPIC-210897587-2', 'Kepler-446', 'KOI-0085', 'KOI-0156', 'KOI-1576', 'LP-358-499', 'KOI-2086', 'KOI-0314'] 
    return ['TTVsystems/' + folder for folder in folders]

if datasets == 'all':
    datasets = allsystems()

if datasets == 'ttv':
    datasets = ttvsystems()

for dataset in list(datasets):
    if dataset == 'random':
        if rebound.__githash__ != 'db3ae2cea8f3462463d3e0c5788a34625bb49a9c':
            print('random dataset not run. Check out rebound commit db3ae2cea8f3462463d3e0c5788a34625bb49a9c and rerun script if needed')
            continue 
    else:
        if rebound.__githash__ != '25f856dc2f79e0ad17b2f6bd604225f550593376':
            print('{0} dataset not run. Check out rebound commit 25f856dc2f79e0ad17b2f6bd604225f550593376 and rerun script if needed'.format(dataset))
            continue 

    safolder = datapath + dataset + '/simulation_archives/runs/'
    trainingdatafolder = repopath + 'training_data/' + dataset + '/'

    already_exists = call('mkdir ' + trainingdatafolder + foldername, shell=True)
    if already_exists:
        print('output folder already exists at {0}. Remove it if you want to regenerate'.format(trainingdatafolder+foldername))
        continue
    call('cp ' + trainingdatafolder + 'labels.csv ' + trainingdatafolder + foldername, shell=True)
    call('cp ' + trainingdatafolder + 'masses.csv ' + trainingdatafolder + foldername, shell=True)
    call('cp ' + trainingdatafolder + 'runstrings.csv ' + trainingdatafolder + foldername, shell=True)

    Norbits = float(Norbits)
    Nout = int(Nout)
    times = np.linspace(0, Norbits, Nout)
    print(trainingdatafolder + foldername)
    gen_training_data(times, trainingdatafolder + foldername, safolder, runorbtseries)
