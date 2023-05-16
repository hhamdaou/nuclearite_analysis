import os  
#from icecube import icetray, dataio, dataclasses
from icecube import icetray, dataio, dataclasses,simclasses,common_variables,phys_services
from icecube.icetray import I3Units
from icecube.simprod.segments import DetectorSim, Calibration

import I3Tray
from I3Tray import *

from I3Tray import I3Tray
from icecube.hdfwriter import I3HDFWriter
from icecube.hdfwriter import I3SimHDFWriter
import glob

######### CORSIKA-in-ice/
path='/data/sim/IceCube/2016/filtered/level2/CORSIKA-in-ice/*/0000000-0000999/Level2_IC86.2016_corsika.020783.000661.i3.zst'
#outdir="/data/user/hhamdaoui/MC_nuclearites/h5/corsika" 
###################################

######### Nucelarite
#path='/data/user/hhamdaoui/MC_nuclearites/MC3_L2_northprocessed'
#outdir="/data/user/hhamdaoui/MC_nuclearites/h5/MC3_L2_northprocessed/"

######### data
#path='/data/exp/IceCube/2019/filtered/level2/0101/Run00131986/'
#outdir="/data/user/hhamdaoui/MC_nuclearites/h5/data/"
 
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
if os.path.isdir(path):  
    print("\nIt is a directory")
    directories = glob.glob(path)
    for directory in directories:
        print(directory)
        for filename in os.listdir(directory):
            if 'new_dir_R1100_d10001e+14' in filename:
                f = os.path.join(directory, filename)
                print('input file :',f)
                tray = I3Tray()
                tray.Add('I3Reader', Filename=f)

                tray.Add(I3HDFWriter,
                #Output='/data/user/hhamdaoui/input_NNMFit/'+dataset+'/'+filename.rstrip('i3.zst')+'.h5',
                Output=outdir+filename.rstrip('i3.gz')+'.h5',

                Keys=keys_list ,     SubEventStreams=SubEv_Streams
                )
                print('output file :',outdir+filename.rstrip('i3.gz')+'.h5')


                tray.Execute()
elif os.path.isfile(path):
    print("\nIt is a normal file") 
    filename=path
    print(filename)
    if '' in filename:
        basename=os.path.basename(filename)
        print(outdir+basename.rstrip('i3.gz')+'.h5')
        tray = I3Tray()
        tray.Add('I3Reader', Filename=filename)
        tray.Add(I3HDFWriter,
        Output=outdir+basename.rstrip('i3.gz')+'.h5',
        Keys=keys_list ,     SubEventStreams=SubEv_Streams
        )

        tray.Execute()
        
    
else:  
    print("It is a special file (socket, FIFO, device file) or doesnt exist" )
print()

"""


#from optparse import OptionParser
#usage = "usage: %prog [options] inputfile"
#parser = OptionParser(usage)

#parser.add_option("-i", "--input", type="str", default='21813', dest="INPUT", help="input folder")
#(options,args) = parser.parse_args()
#print("options", options)
#print("args", args)
#dataset = options.INPUT

# import required module
import os
# assign directory
#directory = '/data/user/hhamdaoui/NuGen/cscd/level2/i3'
directories = glob.glob("nuclearite_1e16_nuclearite_IC86__beta_0001_0001__trigger_level__baseline__proc_0080.i3.gz")
for directory in directories:
    print(directory)
    #directory = '/data/ana/analyses/diffuse/cascades/pass2/sim/nugen/finallevel/'+dataset+'/p0=0.0_p1=0.0_domeff=1.00/*/final_cascade/'
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)
        tray = I3Tray()
        tray.Add('I3Reader', Filename=f)
        tray.Add(I3HDFWriter,
        #Output='/data/user/hhamdaoui/input_NNMFit/'+dataset+'/'+filename.rstrip('i3.zst')+'.h5',
        Output='/data/user/hhamdaoui/input_NNMFit/final_cascade/'+filename.rstrip('i3.zst')+'.h5',

        Keys=['I3MCWeightDict','cscdSBU_MonopodFit4','I3EventHeader'] ,     SubEventStreams=["InIceSplit"]
    )

        tray.Execute()

"""