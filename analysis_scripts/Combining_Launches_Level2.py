#!/bin/sh /cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/icetray-start
#METAPROJECT: /data/user/slatseva/i3/icetray/build


import sys
from glob import glob
from GetTriplets import SplitGlobalTrigger
from Add_Variables import AddVariables
from Build_Angles import BuildAngles
from Geometry import geom
from Combining_Module import Launch_Combi
from Score_Level2 import GetScoreLevel2
import os
import time
import argparse
import numpy as np
import random
from os.path import expandvars
from I3Tray import *
from icecube import dataclasses, dataio, icetray, trigger_sim
from icecube.filterscripts import filter_globals
from icecube.KalmanFilter import MyKalman, MyKalmanSeed
from icecube.filterscripts.slopfilter import SLOPSplitter, SLOPFilter
from icecube.filterscripts.offlineL2.level2_Reconstruction_SLOP import SLOPLevel2
from icecube.hdfwriter import I3HDFTableService
from icecube.tableio import I3TableWriter


if __name__ == "__main__":
    os.putenv("HDF5_USE_FILE_LOCKING", "FALSE")
    parser = argparse.ArgumentParser()
    parser.add_argument("-year", help = "Input directory", dest="year", required=True)
    parser.add_argument("-month", help = "Input directory", dest="month", required=True)
    parser.add_argument("-o", help = "Output file prefix", dest="outfile", required=True)
    parser.add_argument("-N", help = "Number of Snips per frame", dest="N_snips", required=True)
    parser.add_argument("-Nq", help = "Number of total q-frames", dest="N_q", required=True)
    parser.add_argument("-AP", help = "Should AP be added", dest="AP", required=True)
    parser.add_argument("-Trigger", help = "Apply trigger algorithm", dest="Trigger", required=True)
    args = parser.parse_args()
    gcdFile = expandvars("/cvmfs/icecube.opensciencegrid.org/data/GCD/GeoCalibDetectorStatus_2016.57531_V0.i3.gz")
    if args.year in ['2012', '2013', '2014', '2015', '2016']:
        indir = '/data/ana/BSM/IC86_SubRelativisticMonopoles/Background/TriggeredRawData/' + args.year + "/" + args.month +"/"
    else:
        indir = '/data/ana/BSM/IC86_SubRelativisticMonopoles/Background/new/Snipped_Launches/'
    # indir = '/data/ana/BSM/IC86_SubRelativisticMonopoles/Background/UntriggeredBackground/' #"/data/user/jbottcher/Monopoles/"
    infiles = glob(indir+ "*Snipped_Launches_"+args.year + "_" + args.month+".i3.zst")
    #print(indir+ "*Snipped_Launches_"+args.year + "_" + args.month+".i3.zst")
    print(infiles)
    #print(infiles[0])
    #indir = '/data/user/jbottcher/Monopoles/Sys_Test/'
    t_sleep= np.random.rand()*30 #When working with condor, not every job should work on the infile at the same time
    time.sleep(t_sleep)
    # The Infile Should contain a list of qframes with the snips in it. See the Snipping tool for that

    N_snips = int(args.N_snips) # Number of Snips to use in one frame. Determines the length of one Snip
    N_q = int(args.N_q) #Number of Q-frames to be produced. Produced lifetime = N_snips*<dt_snips>

    #Variables that would be saved in a HDF file
    SlopVariableNames = ["SLOPKalman_Chi2Pred" , "SLOPKalman_LineFit","SLOPLineFit_Chi2",#"All_Q_frames",
                         "SLOPKalman_Map" , "SLOPKalman_NHits", "SLOPTime" , "SLOPLaunchMapTuples",
                         "SLOPTuples_Z","SLOPTuples_Y","SLOPTuples_X","SLOPTuples_Dist","SLOPTuples_Dist2",
                         "SLOPTuples_CosAlpha_Launches" , "SLOPTuples_LineFit" ,
                        "SLOPTuples_RelV_Launches","SLOPTuples_Vel",
                     "BDT_NHits",'BDT_DistToTrack',"BDT_NTuple",
                     "BDT_NTriplet","BDT_Triplet_HLC",
                     "BDT_MeanAngle","BDT_VarAngle",
                     "BDT_Velocity","BDT_Gap_Min",
                     "BDT_Gap_Ratio","BDT_Gap_Max",
                     "BDT_Chi2Pred","BDT_TriggerLength",
                     "BDT_Invvel_max","BDT_Invvel_mean",
                     "BDT_Invvel_median", # new!!!
                     "BDT_Invvel_min","BDT_Invvel_var",
                     "BDT_Invvel_90per","BDT_Invvel_10per", # new!!!
                     "BDT_Invvel_75per","BDT_Invvel_25per", # new!!!
                     "BDT_Invvel_skewness","BDT_Invvel_kurtosis",  # new!!!
                     "BDT_Innerangle_var", "BDT_Innerangle_mean",
                     "BDT_Innerangle_median", # new!!!
                     "BDT_Innerangle_min", 
                     "BDT_Innerangle_90per","BDT_Innerangle_10per", # new!!!
                     "BDT_Innerangle_75per","BDT_Innerangle_25per", # new!!!
                     "BDT_Innerangle_skewness","BDT_Innerangle_kurtosis",  # new!!!
                     "BDT_Smoothness",
                     "BDT_Innerangle_max", "BDT_Gap_Median",
                     "BDT_Gap_Mean","SLOPTuples_LineFitCharacteristics",
                     "CylinderIntersection", "DistToCenter", "Number_PE",
                     "Random_Variable", 
                     "Score_Level1_B001L001", "Score_Level1_B001L01", "Score_Level1_B001L1", "Score_Level1_B001L10",
                     "Score_Level1_B0001L001", "Score_Level1_B0001L01", "Score_Level1_B0001L1", "Score_Level1_B0001L10",
                     "Score_Level2_B001L001", "Score_Level2_B001L01", "Score_Level2_B001L1", "Score_Level2_B001L10",
                     "Score_Level2_B0001L001", "Score_Level2_B0001L01", "Score_Level2_B0001L1", "Score_Level2_B0001L10"
                       ]

    tray = I3Tray()
    tray.AddModule("I3InfiniteSource","infinite",
                   Prefix = gcdFile,
                   Stream=icetray.I3Frame.DAQ)
    #Background generating module
    tray.Add(Launch_Combi, 'Reshuffleing',
                SnipFileName= infiles[0], #input Snip File
                N_Snips = N_snips, #Number of Snips per output frame, t_frame = N_snips*<t_snip>
                AP = int(args.AP), #Version of "After pulses" to append to Snip pulses (0: No AP; 1: Two classes; 2: After t_prox; 3: One class)
                N_q = int(N_q) #Number of q frames to be produced
                )

    if int(args.Trigger)==1: #Triggering is optional
        gcd_file = dataio.I3File(gcdFile)
        fr = gcd_file.pop_frame()
        while "I3DetectorStatus" not in fr :
            fr = gcd_file.pop_frame()
        tsmap = fr.Get("I3DetectorStatus").trigger_status
        for tkey, ts in tsmap:
            if tkey.type == dataclasses.SLOW_PARTICLE:
                tray.Add("SlowMonopoleTrigger", TriggerConfigID = tkey.config_id) #We only want the SLOP trigger

        tray.AddModule("I3GlobalTriggerSim","TriggerSim_global_trig",
                       RunID = 1234,
                       FilterMode = True)
        tray.AddModule(SplitGlobalTrigger,  "Splitter", )       #Split Multiple SLOP Trigger per frame

        tray.AddModule("Rename", '_trigrename',
                        keys=[filter_globals.triggerhierarchy,filter_globals.qtriggerhierarchy]
                            )

        tray.AddSegment(SLOPSplitter, filter_globals.SLOPSplitter,  #Create the P-frames
                       InputPulses = 'InIcePulses'
                       )

        tray.AddSegment(SLOPFilter, 'SLOPFilter', # Apply Online Level 2 Filter
                         use_pulses = False)

        tray.AddModule(MyKalmanSeed, "Seed_launches", # Part of the Old Offline Level 2 Filter
                InputMapName="SLOPLaunchMapTuples",
                OutputTrack="SLOPTuples_LineFit2",
                )

        tray.AddModule(BuildAngles, "Angles")    # Create New Variables

        tray.AddModule(AddVariables, "AddVar")   # Compress used Variables into single quantities
        tray.AddModule(geom,'geom')
        tray.AddModule(GetScoreLevel2, 'score2') # Calculate Level 2 scores for all BDTs


        tray.Add("I3Writer", Filename=os.path.join("/data/ana/BSM/IC86_SubRelativisticMonopoles/Background/new/Level_3/"+args.year+"/"+args.month+"/Run_"+args.year+"_"+args.month+"_"+args.outfile+".i3.zst"),
                       Streams = [icetray.I3Frame.DAQ, icetray.I3Frame.Physics, 
                           icetray.I3Frame.DetectorStatus, icetray.I3Frame.Geometry],
                       DropOrphanStreams=[icetray.I3Frame.DAQ]    
                        )

        hdf = I3HDFTableService(os.path.join("/data/ana/BSM/IC86_SubRelativisticMonopoles/Background/new/Level_3/"+args.year+"/"+args.month+"/Run_"+args.year+"_"+args.month+"_"+args.outfile+"_Processed.hd5"))
        tray.AddModule(I3TableWriter,'writer', tableservice = hdf,   keys  = SlopVariableNames,  SubEventStreams = ["SLOPSplit"])



    import cProfile, pstats, io
    pr = cProfile.Profile()
    pr.enable()
    tray.Execute(int(N_q)+3)
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    #ps.print_stats()
    #print(s.getvalue())

print('ready')