#!/bin/env python

from icecube import icetray, dataio, dataclasses,simclasses,common_variables,phys_services
from I3Tray import I3Tray
from icecube.hdfwriter import I3HDFWriter
from icecube.hdfwriter import I3SimHDFWriter
import glob,os
from optparse import OptionParser
usage = "usage: %prog [options] inputfile"
parser = OptionParser(usage)

parser.add_option("-f", "--dataset", type="str", default='21813', dest="DATASET", help="dataset number")
(options,args) = parser.parse_args()
print("options", options)
print("args", args)
dataset = options.DATASET


# Specify path
outdir = '/data/user/hhamdaoui/MC_nuclearites/h5/corsika/level2/'+dataset+'/'
print('output is ',outdir)
# Check whether the specified
# path exists or not
isExist = os.path.exists(outdir)
if isExist:
    print("directory already exist!")
print(isExist)
if not isExist:
    os.makedirs(outdir)
    print("The new directory is created!")

keys_list=['SLOPDSTPulseMask',
'CVMultiplicity',
'LineFit',
'LineFitParams',
'CVStatistics',
'SLOPKalman_Chi2Pred',
'SLOPKalman_LineFit',
'SLOPKalman_Map',
'SLOPKalman_NHits',
'SLOPKalman_P',
'SLOPLaunchMapTuples',
'SLOPPulseMask',
'SLOPPulseMaskHyperClean',
'SLOPPulseMaskMPClean',
'SLOPPulseMaskSuperClean',
'SLOPPulseMaskUltraClean',
'SLOPTuples_CosAlpha_Launches',
'SLOPTuples_LineFit',
'SLOPTuples_RelV_Launches']
SubEv_Streams=['InIceSplit','NullSplit','SLOPSplit']
# import required module
import os
# assign directory
#directory = '/data/user/hhamdaoui/NuGen/cscd/level2/i3'

directories = glob.glob('/data/sim/IceCube/2016/filtered/level2/CORSIKA-in-ice/'+dataset+'/0000000-0000999/')
print('directories:',directories)

def write():
    i=0
    for directory in directories:
        print(directory)
        for filename in os.listdir(directory):
            i=i+1
            print('number of files procceced: ',i)
            if 'Level2_IC86.2016_corsika' in filename:
                f = os.path.join(directory, filename)
                Outputfile=outdir+filename.rstrip('.i3.zst')+'.h5'
                print('output file :',Outputfile)
                if os.path.exists(Outputfile):
                        print("The file already exist will be removed")
                        os.remove(Outputfile)
                else:
                        print("The file does not exist")

                tray = I3Tray()
                tray.Add('I3Reader', Filename=f)
                tray.Add(I3HDFWriter,
                #Output='/data/user/hhamdaoui/input_NNMFit/'+dataset+'/'+filename.rstrip('i3.zst')+'.h5',
                Output=Outputfile,Keys= keys_list,     SubEventStreams=SubEv_Streams)
                tray.Execute()

    print('writing Done')  
merged_path='/data/user/hhamdaoui/MC_nuclearites/h5/corsika/level2/'+'/'+'merged/'

def merge():
    isExist = os.path.exists(merged_path)
    if isExist:
        print("merge directory already exist!")
    if not isExist:
        os.makedirs(merged_path)
        print("The new directory is created!")
    print('output is ',outdir)
    # import required module
    # assign directory
    #directory = '/data/user/hhamdaoui/NuGen/cscd/level2/i3'
    command='hdfwriter-merge  -o '+merged_path+dataset+'.hdf'+'  '+outdir+'*.h5'
    print(command)
    os.system(command)
    print('merging Done')
write()
merge()