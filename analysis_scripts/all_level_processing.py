#!/bin/sh /cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/icetray-start
#METAPROJECT: /data/user/slatseva/i3/icetray/build

import time
script_start_time = time.time()

combo_stable = "/combo/stable_rev175960/"
icesim_v06   = "/icesim/V06-01-01/"
# tried this from sandbox/aburgman:
#/data/user/hhamdaoui/nuclearite_analysis/analysis_scripts/all_level_processing.py --filename /data/user/hhamdaoui/MC_nuclearites/MC3_L2_northprocessed/nuclearite_m_1e+13_nevent_10000_nuclearite_IC86__beta_0001_0002__trigger_level__baseline__proc_0000.i3.gz --gen mpsim --num 00002 --flav monopole
# data/user/hhamdaoui/nuclearite_analysis/analysis_scripts/all_level_processing.py --gen exprm --num 86009 --flav unknown --filename /data/exp/IceCube/2019/filtered/level2/0101/Run00131986/Level2_*GCD.i3.zst /data/exp/IceCube/2019/filtered/level2/0101/Run00131986/Level2_*00000000.i3.zst
import random, os, sys, json
import numpy as np
import scipy as sp
import scipy.constants as spco
import scipy.stats as spst
import argparse,warnings
#import subprocess
#from subprocess import call

from icecube import icetray, dataclasses, dataio, phys_services#, sim_services
#from icecube import monopole_generator
from icecube.icetray import I3Units
#from icecube.simprod.segments import DetectorSim, Calibration

from icecube.dataclasses import I3Double, I3String

from icecube import icetray, dataclasses, dataio, tableio, common_variables, linefit, portia, recclasses, phys_services#, sim_services
from icecube import photonics_service, millipede, DomTools
from icecube.icetray import I3Units
from icecube.dataclasses import I3MCTree, I3Particle, I3RecoPulseSeriesMap, I3RecoPulse, I3MapStringDouble
from icecube.recclasses import I3PortiaEvent, I3DirectHitsValues, I3TrackCharacteristicsValues
from icecube.tableio import I3TableWriter
from icecube.hdfwriter import I3HDFTableService
from icecube.common_variables import direct_hits
from icecube.common_variables import hit_multiplicity
from icecube.common_variables import hit_statistics
from icecube.common_variables import track_characteristics
from icecube.common_variables import time_characteristics
from I3Tray import *

import I3Tray
from I3Tray import *
from I3Tray import load

load("millipede")

from icecube import icetray
from icecube.icetray import I3Units

from icecube.pybdtmodule import PyBDTModule

currworkdir         = os.path.dirname(os.path.realpath(__file__)) + ("/" if os.path.dirname(os.path.realpath(__file__))[-1]!="/" else "")
currworkdir_subdir  = currworkdir.split("/")[-1] if currworkdir.split("/")[-1] else currworkdir.split("/")[-2]
currworkdir_library = currworkdir.replace( currworkdir_subdir, "00_library" )
sys.path.insert( 0, currworkdir         )
sys.path.insert( 0, currworkdir_library )
import shutil

#shutil.copy('/data/user/hhamdaoui/nuclearite_analysis/analysis_scripts/mmact_analysis_utils.py', currworkdir)
#shutil.copy('/data/user/hhamdaoui/nuclearite_analysis/analysis_scripts/mmact_analysis_funcs.py', currworkdir)

# 2nd option
#print 'currworkdir', currworkdir
#print 'currworkdir_library', currworkdir_library


import mmact_analysis_utils    as utils
import mmact_analysis_funcs    as funcs
from Add_Variables import AddVariables
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#from matplotlib.colors import LogNorm
#from matplotlib import cm
#
#matplotlib.rcParams['font.family']='serif'
#matplotlib.rcParams['font.size']=14
#matplotlib.rcParams['axes.grid']=True
#matplotlib.rcParams['xtick.labelsize']='x-small'
#matplotlib.rcParams['ytick.labelsize']='x-small'
#matplotlib.rcParams['legend.fontsize']='x-small'
#matplotlib.rcParams['legend.numpoints']=1

#:--
# PREPARATIONS
#:--


# Argument parsing below

parser = argparse.ArgumentParser(description = "All analysis cuts in one fell swoop.")
parser.add_argument( "-f", "--filename",    dest="filename",    type=str, nargs="+", default="",    help="The input file to the sanity check script."           )
parser.add_argument( "-l", "--lunger",      dest="lunger",      action="store_true", default=False, help="Should this be processed by, and stored in the folder of, LUnger?" )
parser.add_argument( "-r", "--reprocexprm", dest="reprocexprm", action="store_true", default=False, help="Reprocess the experimental events that arrived at L5 but didn't come through the BDT variable making and BDT classifying." )
parser.add_argument(       "--gen",         dest="gen",         type=str,            default="",    help="Data generation tool (nugen, mpsim, juliet, exprm, etc.)."                                         )
parser.add_argument(       "--num",         dest="num",         type=str,            default="",    help="Dataset number." )
parser.add_argument(       "--flav",        dest="flav",        type=str,            default="",    help="Flavor." )
parser.add_argument(       "--altoutdatadir",  dest="altoutdatadir",  type=str,            default="",     help="Non-ABurgman directory: alternative 'outdatadir'."              )
parser.add_argument(       "--altoutplotdir",  dest="altoutplotdir",  type=str,            default="",     help="Non-ABurgman directory: alternative 'plotdir' and 'outputdir'." )
parser.add_argument( "-v", "--verbose",     dest="verbose",     type=int,            default=1,     help="How verbose is this script?"                          )
args = parser.parse_args()

#from statistics import listnorm
from misc import *
from cutting import *
from plotting import *
from statistics import *
from frameobject_manipulation import *

mmp = utils.mmact_print(script_start_time,args.verbose)
mmp.start()
mmp.label = "MMACT"
mmp.vbprint( "Imported Stuff",    [1,2] )
mmp.vbprint( "Loaded Stuff",      [1,2] )
mmp.vbprint( "Parsed Arguments",  [1,2] )


# Checking if alternative directories are set

# 'outdatadir'
if args.altoutdatadir:
	utils.outdatadir = { k: val.replace( utils.mmactdir, args.altoutdatadir ) for k,val in utils.outdatadir.items() }
	mmp.vbprint( "Set 'outdatadir' to '{}'".format(args.altoutdatadir), [1,2] )

# 'plotdir' and 'outputdir'
if args.altoutplotdir:
	utils.plotdir   = { k: val.replace( utils.mmactdir, args.altoutplotdir ) for k,val in utils.plotdir.items()   }
	utils.outputdir = { k: val.replace( utils.mmactdir, args.altoutplotdir ) for k,val in utils.outputdir.items() }
	mmp.vbprint( "Set 'plotdir' and 'outputdir' to '{}'".format(args.altoutplotdir), [1,2] )


gen = str( args.gen )
num = str( args.num )
syst = "baseline" if gen!="mpsim" else funcs.get_monopole_systematic_qad(args.filename[0])
flav = str( args.flav ) #funcs.get_flavor_qad(args.filename[0])


if gen=="mpsim":
	filename_i3  = str( str(args.filename[0]).split("/")[-1] ).replace("i3.bz2","i3.gz").replace("i3.zst","i3.gz")
	filename_hdf = str( str(args.filename[0]).split("/")[-1] ).replace("i3.gz","hd5").replace("i3.bz2","hd5").replace("i3.zst","hd5")
elif gen=="nugen":
	filename_i3  = funcs.get_nugen_custom_filename_qad( str(args.filename[0]), utils.datadir[gen][num], num ).replace("i3.bz2","i3.gz").replace("i3.zst","i3.gz")
	filename_hdf = funcs.get_nugen_custom_filename_qad( str(args.filename[0]), utils.datadir[gen][num], num ).replace("i3.gz","hd5").replace("i3.bz2","hd5").replace("i3.zst","hd5")
elif gen=="exprm":
	if args.reprocexprm:
		filename_i3  = funcs.get_exprm_custom_filename_qad( str(args.filename[0]), str(args.filename[-1]), num, reproc=True ).replace("i3.bz2","i3.gz").replace("i3.zst","i3.gz")
		filename_hdf = funcs.get_exprm_custom_filename_qad( str(args.filename[0]), str(args.filename[-1]), num, reproc=True ).replace("i3.gz","hd5").replace("i3.bz2","hd5").replace("i3.zst","hd5")
	else:
		filename_i3  = funcs.get_exprm_custom_filename_qad( str(args.filename[0]), str(args.filename[-1]), num              ).replace("i3.bz2","i3.gz").replace("i3.zst","i3.gz")
		filename_hdf = funcs.get_exprm_custom_filename_qad( str(args.filename[0]), str(args.filename[-1]), num              ).replace("i3.gz","hd5").replace("i3.bz2","hd5").replace("i3.zst","hd5")
#else:
#	filename_i3  = str( filename_base.split("/")[-1] ).replace("i3.bz2","i3.gz").replace("i3.zst","i3.gz")
#	filename_hdf = str( filename_base.split("/")[-1] ).replace("i3.gz","hd5").replace("i3.bz2","hd5").replace("i3.zst","hd5")

outname = { "i3":  { lev: odd+filename_i3  for lev,odd in utils.outdatadir.items() } ,
            "hdf": { lev: odd+filename_hdf for lev,odd in utils.outdatadir.items() } , }
if args.lunger:
	outname = { "i3":  { lev: odd+filename_i3  for lev,odd in utils.outdatadir_lunger.items() } ,
                "hdf": { lev: odd+filename_hdf for lev,odd in utils.outdatadir_lunger.items() } , }


#if False:
#	testfile = open( dir_data + "TESTFILE__" + filename_i3.split(".")[0].split("__")[-1] + ".txt", "w" )
#	testfile.write(filename_i3+"\n"+filename_hdf)
#	testfile.close()


mmp.vbprint( "Constructed the output filenames", [1,2] )


filename_badfiles = [ "/data/ana/Cscd/StartingEvents/NuGen_new/NuTau/medium_energy/IC86_flasher_p1=0.3_p2=0.0/l2/2/l2_00001014.i3.zst" ]

args.filename = [ str(fn) for fn in args.filename if fn not in filename_badfiles ]


#
#-
#:--
#-
#   ##### ####    #   #   #
#     #   #   #  # #  #   #
#     #   ####  #   #  # #
#     #   #   # #####   #
#     #   #   # #   #   #
#-
#:--
#-
#


#:--
# STARTING THE TRAY
#:--

# Starting the tray.
tray = I3Tray()
mmp.vbprint( "Started the tray", [1,2] )

#:--
# INPUT
#:--

SlopVariableNames = ["SLOPKalman_Chi2Pred" , "SLOPKalman_LineFit","SLOPLineFit_Chi2",#"All_Q_frames",
                         "SLOPKalman_Map" , "SLOPKalman_NHits", "SLOPTime" , "SLOPLaunchMapTuples",
                         "SLOPTuples_Z","SLOPTuples_Y","SLOPTuples_X","SLOPTuples_Dist","Number_doms","BDT_NChannel","SLOPTuples_Dist2",
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
                       ]
keys_list=['SLOPDSTPulseMask',
'BDT_NChannel',
'BDT_NTuple',
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
# Reading the input file
if gen!="exprm":
	tray.AddModule( "I3Reader", filenameList = [utils.gcdfile[gen][num]] + args.filename, )
else:
	tray.AddModule( "I3Reader", filenameList = args.filename, ) # The GCD file is already in the list given in args.filename, as there is a separate one for each run
mmp.vbprint( "Added I3Reader to the tray", [1,2] )

skip_for_i3 = [ "InIceRawData", "I3MCTree", "Cascade*", "Muon*", "Pole*", "Offline*", "Online*", "I3MCPESeriesMap", "I3MCPulseSeriesMap", "I3MCPulseSeriesMapParticleIDMap", ]

#book_this_hdf = []
#book_this_hdf = add_to_list_uniquely(book_this_hdf, ["EHEPortiaEventSummarySRT","EHEOpheliaSRT_ImpLF","EHEOpheliaParticleSRT_ImpLF","Homogenized_Qtot"])
#book_slim     = ["ABurgmanVars"]
book_slim=keys_list
mmp.vbprint( "Set some parameters", [1,2] )


#
#-
#:--
#-
#   #   #   #   ####   ###    #   ####  #     #####  ####
#   #   #  # #  #   #   #    # #  #   # #     #     #
#   #   # #   # ####    #   #   # ####  #     ###    ###
#    # #  ##### #   #   #   ##### #   # #     #         #
#     #   #   # #   #  ###  #   # ####  ##### ##### ####
#-
#:--
#-
#


#:--
# INTERMEDIARY VARIABLE CALCULATION
#:--

# MCPrimaryParticle
if gen!="exprm":
	tray.Add(add_MCPrimaryParticle, streams = [icetray.I3Frame.Physics])
	#book_this_hdf = add_to_list_uniquely(book_this_hdf,["MCPrimaryParticle"])
	mmp.vbprint( "Added add_MCPrimaryParticle to the tray", [1,2] )


if gen!="exprm":
	def add_DeterministicZeroToOneFloat(frame,filenamestring,frameobjectname="DeterministicZeroToOneFloat"):
		if add_DeterministicZeroToOneFloat.eventnum == 0:
			add_DeterministicZeroToOneFloat.prev_eventid = 0
		add_DeterministicZeroToOneFloat.eventnum += 1
		if frame["I3EventHeader"].event_id < add_DeterministicZeroToOneFloat.prev_eventid:
			add_DeterministicZeroToOneFloat.filenum += 1
		add_DeterministicZeroToOneFloat.prev_eventid = frame["I3EventHeader"].event_id
		filename = filenamestring.split(",")[add_DeterministicZeroToOneFloat.filenum-1]
		seedstring  = "seedstring_for_construction_of_deterministic_float_between_zero_and_one"
		seedstring += "____FILENAME__{}".format(filename)
		seedstring += "____FILENUMBER__{}".format(add_DeterministicZeroToOneFloat.filenum-1)
		seedstring += "____EVENTNUMBER__{}".format(add_DeterministicZeroToOneFloat.eventnum-1)
		frame[frameobjectname] = I3Double(str_to_prob(seedstring))

	add_DeterministicZeroToOneFloat.eventnum = 0
	add_DeterministicZeroToOneFloat.filenum  = 0

	def add_BDTTrainTest(frame,bdttrainfrac=0.5,bdtsep="BDTSeparator"):
		if "BDTTrainTest" in frame:
			del frame["BDTTrainTest"]
		frame["BDTTrainTest"] = I3MapStringDouble( { "train": float(frame[bdtsep]<=bdttrainfrac), "test": float(frame[bdtsep]>bdttrainfrac),  } )

	# BDT training/testing set separator
	tray.Add( add_DeterministicZeroToOneFloat, filenamestring = ",".join(args.filename), frameobjectname="BDTSeparator", streams = [icetray.I3Frame.Physics] )
	#book_this_hdf = add_to_list_uniquely(book_this_hdf,["BDTSeparator"])
	mmp.vbprint( "Added add_DeterministicZeroToOneFloat to the tray", [1,2] )


if gen!="exprm":
	# Cutting too low primary neutrino energy
	if gen=="nugen":
		tray.Add(funcs.keep_nugen_mcprimaryenergy_above_1e5GeV, streams = [icetray.I3Frame.Physics])

	# OrphanStreamDrop
	tray.AddModule(OrphanStreamDrop, "osd_too_low_mcenergy", OrphanStream = utils.physicsstream[gen][num])
	mmp.vbprint( "Added OrphanStreamDrop (too low MC energy) to the tray", [1,2] )

# Removing Standard Candle Events
if gen=="exprm":
	tray.Add(funcs.cut_standard_candle_events, streams = [icetray.I3Frame.Physics])
	mmp.vbprint( "Removed Standard Candle induced events", [1,2] )

# GeometricTrack
if gen!="exprm":
	#tray.Add(funcs.add_GeometricTrack, trackname = "EHEOpheliaParticleSRT_ImpLF", streams = [icetray.I3Frame.Physics])
	tray.Add(funcs.add_GeometricTrack, trackname = "MCPrimaryParticle",           streams = [icetray.I3Frame.Physics])
	#book_this_hdf = add_to_list_uniquely(book_this_hdf,["GeometricTrackEHEOpheliaParticleSRT_ImpLF","GeometricTrackMCPrimaryParticle"])
	mmp.vbprint( "Added GeometricTrack to the tray", [1,2] )

# Centrality
if gen!="exprm":
	#tray.Add(funcs.add_Centrality, trackname = "EHEOpheliaParticleSRT_ImpLF", streams = [icetray.I3Frame.Physics])
	tray.Add(funcs.add_Centrality, trackname = "MCPrimaryParticle",           streams = [icetray.I3Frame.Physics])
	#book_this_hdf = add_to_list_uniquely(book_this_hdf,["Centrality_EHEOpheliaParticleSRT_ImpLF","Centrality_MCPrimaryParticle"])
	mmp.vbprint( "Added Centrality to the tray", [1,2] )



# CountingWeightFactor
tray.Add(funcs.add_CountingWeightFactor, streams = [icetray.I3Frame.Physics])
#book_this_hdf = add_to_list_uniquely(book_this_hdf,["CountingWeightFactor"])
mmp.vbprint( "Added add_CountingWeightFactor to the tray", [1,2] )

tray.Add(funcs.add_ABurgmanGenNum, gen=gen, num=num, streams = [icetray.I3Frame.Physics])

if not args.reprocexprm:
	# OneWeight
	tray.Add(funcs.add_OneWeightDict, gen=gen, num=num, flav=flav, syst=syst, streams = [icetray.I3Frame.Physics])
	mmp.vbprint( "Added add_OneWeightDict to the tray", [1,2] )

## FIX EXPRM - consider what can be written out
## Output issue for experimental
#if "exp" in gen:
#	exit("cannot write out L0, L1 HDF files for experimental data, as this will be too large. Wait until L2?")

#
#-
#:--
#-
#    #### #   # #####  ####
#   #     #   #   #   #
#   #     #   #   #    ###
#   #     #   #   #       #
#    ####  ###    #   ####
#-
#:--
#-
#



#:--
# L0
#:--

# L0 cut --- trigger
tray.Add( funcs.cut_analysis, lev="trigger", gen=gen, streams = [icetray.I3Frame.Physics] )
mmp.vbprint( "Added cut_eheana_L0 to the tray", [1,2] )
tray.AddModule(AddVariables, "AddVar") #Compress used Variables into single quantities

# Output HDF
tray.AddModule( I3TableWriter, tableservice = [I3HDFTableService( outname["hdf"]["trigg"] )], keys = SlopVariableNames, SubEventStreams = SubEv_Streams )
mmp.vbprint( "Added I3TableWriter (post L1) to the tray", [1,2] )
print(outname["hdf"]["trigg"])




# Finishing and executing
tray.AddModule("TrashCan","Trash") # perhaps not needed anymore
mmp.vbprint( "Added TrashCan to the tray", [1,2] )
mmp.vbprint( "Tray execution upcomming!", [1,2] )
tray.Execute()
mmp.vbprint( "Tray executed!", [1,2] )
tray.Finish()
mmp.vbprint( "Tray finished", [1,2] )
del tray
mmp.vbprint( "Tray deleted", [1,2] )
mmp.vbprint( "Now totally done", [1,2] )
mmp.finish()
