#!/bin/sh /cvmfs/icecube.opensciencegrid.org/py2-v2/icetray-start
#METAPROJECT /data/user/aburgman/icecode/meta-projects/combo/stable_rev175960/RHEL_7_x86_64
# /data/user/aburgman/icecode/meta-projects/combo/stable_rev175960/RHEL_7_x86_64/

import time
script_start_time = time.time()

combo_stable = "/combo/stable_rev175960/"
icesim_v06   = "/icesim/V06-01-01/"

import random, os, sys, json
import numpy as np
import argparse

from icecube import icetray, dataclasses, dataio, sim_services, phys_services
from icecube import monopole_generator
from icecube.icetray import I3Units
from icecube.simprod.segments import DetectorSim, Calibration

import I3Tray
from I3Tray import *
from I3Tray import load

import mmact_utils as utils

load("xppc")
load("ppc")
load("libDOMLauncher")


#:--
# PREPARATIONS
#:--

# Argument parsing below

parser = argparse.ArgumentParser(description = "Simulating monopoles for the MMACT analysis")
parser.add_argument( "-n", "--numevents",   dest="nev",         type=int,  default=-1,    help="The number of events to simulate."                                            )
parser.add_argument( "-d", "--outdirgen",   dest="outdirgen",   type=str,  default="",    help="The directory where the gen files should be created."                             )
parser.add_argument( "-e", "--outdirtrigg", dest="outdirtrigg", type=str,  default="",    help="The directory where the trigg files should be created."                             )
parser.add_argument( "-p", "--iprocess",    dest="iprocess",    type=int,  default=-1,    help="The number of the current process."                                           )
parser.add_argument( "-r", "--nprocess",    dest="nprocess",    type=int,  default=-1,    help="The total number of processes."                                               )
parser.add_argument( "-g", "--gcdfile",     dest="gcdfile",     type=str,  default="",    help="The path to the GCD file."                                                    )
parser.add_argument( "-m", "--icemodel",    dest="icemodel",    type=str,  default="",    help="The path to the icemodel."                                                    )
parser.add_argument( "-s", "--systematic",  dest="systematic",  type=str,  default="",    help="The variation of the simulation settings for systematic uncertainty studies." ) 
parser.add_argument( "-t", "--title",       dest="title",       type=str,  default="nuclearite_m_",    help="The title of this sample, if you want a custom name."                          ) 
#DEPRECATED
#parser.add_argument( "-b", "--resubfailed", dest="resubfailed", type=bool, default=False, help="Is this a time when we resubmit previously failed jobs?" )
parser.add_argument( "-v", "--verbose",     dest="verbose",     type=int,  default=1,     help="How verbose is this script?"                                                  )
parser.add_argument( "-B", "--beta",   dest="beta",         type=list,  default=[0.001,0.0015],    help="beta."                                            )
parser.add_argument( "-z", "--mass",   dest="mass",         type=float,  default=1e15,    help="mass of nuc."   )
parser.add_argument( "-a", "--adius",   dest="radius",         type=float,  default=1100,    help="genertation disk radius."   )
parser.add_argument( "-c", "--distance",   dest="distance",         type=float,  default=1000,    help="genertation disk distance."   )


#DEPRECATED

args = parser.parse_args()

print 'args.mass:',args.mass

disk_radius=args.radius
disk_distance=args.distance


nuc_mass=args.mass
beta=args.beta
#DEPRECATED
#if "angsens" in args.systematic:
#	original_iprocess = args.iprocess
#	args.iprocess += 1000

mmp = utils.mmact_print(script_start_time,args.verbose)
mmp.start()
mmp.label = "MMACT"

mmp.vbprint( "Imported Stuff",    [1,2] )

mmp.vbprint( "Loaded Stuff",      [1,2] )

mmp.vbprint( "Parsed Arguments",  [1,2] )

#DEPRECATED
#if "angsens" in args.systematic and args.resubfailed:
#	mmp.vbprint( "Reprocessing a few failed jobs!", [1,2] )
#	resub_iprocess = [ 221, 220, 219, 218, 217, 216, 215, 214, 213, 210, 174, 173, 172, 171, 170, 169, 168, ]
#	if original_iprocess not in resub_iprocess:
#		mmp.vbprint( "Not reprocessing this one!", [1,2], 2 )
#		mmp.finish()
#		exit()

#:--
# SETTING UP SOME PARAMETERS
#:--
print "args.iprocess :",args.iprocess,'args.nprocess :',args.nprocess
if args.iprocess<0 or args.nprocess<0 or args.iprocess>=args.nprocess:
	exit("At least one invalid processing number input! Do you maybe have more than one 'queue' in your submit file? Sum all numbers of processes to get the total!")
nev      = utils.default_settings["n_events"] if 0 >= args.nev      else args.nev

temp_filename = utils.filename_template if not args.systematic else utils.filename_template_syst
temp_filename = temp_filename.replace( "TITLE",         args.title+str(nuc_mass)+'_nevent_'+str(nev)                 )
temp_filename = temp_filename.replace( "FLAVOR",        "nuclearite"                                                      )
temp_filename = temp_filename.replace( "BETALOW",       "{:04d}".format(int(utils.gen_params["beta_spectrum"][0]*1000)) )
temp_filename = temp_filename.replace( "BETAHIGH",      "{:04d}".format(int(utils.gen_params["beta_spectrum"][1]*1000)) )

temp_filename = temp_filename.replace( "PROCESSNUMBER", "{:04d}".format(int(args.iprocess))                             )
if args.systematic:
	temp_filename = temp_filename.replace( "SYSTEMATICVARIATION", str(args.systematic)                     )


outname_gen   = args.outdirgen   + "/" + temp_filename.replace( "DATALEVEL",     "generator"                            )
outname_trigg = args.outdirtrigg + "/" + temp_filename.replace( "DATALEVEL",     "trigger"                              )

gcdname  = utils.default_settings["gcd"]      if  not args.gcdfile  else args.gcdfile
if not args.systematic:
	icemodel = utils.default_settings["icemodel"] if not args.icemodel else args.icemodel
else:
	icemodel = args.icemodel if args.icemodel else utils.get_systematics_icemodel(args.systematic)




os.putenv("PPCTABLESDIR",os.path.expandvars(icemodel))

#:--
# STARTING THE TRAY
#:--

tray = I3Tray()

mmp.vbprint( "Started the tray.", [1,2] )

tray.AddService( "I3SPRNGRandomServiceFactory",
                 Seed      = 0,
                 NStreams  = args.nprocess,
                 StreamNum = args.iprocess )
tray.AddModule( "I3InfiniteSource", Prefix = gcdname )

mmp.vbprint( "Added random service to the tray.", [1,2] )

# Generation below

tray.AddModule("I3MonopoleGenerator",
	Mass       = nuc_mass,
	BetaRange  = beta,
	Disk_dist  =disk_distance,# utils.gen_params["disk_distance"],
	Disk_rad   = disk_radius,# utils.gen_params["disk_radius"],
	NEvents    = nev,
	)
mmp.vbprint( "Added monopole generator to the tray.", [1,2] )

# Propagation below

tray.AddModule("I3MonopolePropagator",
	MaxDistanceFromCenter = utils.gen_params["dist_to_cent_max"],
	MaxLength             = utils.gen_params["step_length_max"],
	StepSize              = np.nan,
	MeanFreePath =utils.gen_params['MeanFreePath'] # slow monopole only

	)
mmp.vbprint( "Added monopole propagator to the tray.", [1,2] )

tray.Add(utils.check_monopole_lengths_10m, streams = [icetray.I3Frame.DAQ])
mmp.vbprint( "Added check_monopole_lengths_10m to the tray.", [1,2] )

tray.Add(utils.add_MCPrimaryParticle, streams = [icetray.I3Frame.DAQ])
mmp.vbprint( "Added add_MCPrimaryParticle to the tray.", [1,2] )

tray.Add(utils.add_SystematicsMask, syst=args.systematic, streams = [icetray.I3Frame.DAQ])
mmp.vbprint( "Added add_SystematicsMask to the tray.", [1,2] )

# Printing out the generated stuff

tray.AddModule( "I3Writer",
	filename = outname_gen,
	streams  = [ icetray.I3Frame.DAQ ],
	SkipKeys = [ "I3MCPulseSeriesMapPrimaryIDMap" ],
	)
mmp.vbprint( "Added I3Writer to the tray, to write out the generator level I3 file.", [1,2] )

# Light production below

tray.AddModule("i3ppc",
	efficiency_scaling_factor = utils.systematic_domeff[args.systematic],
	gpu = 0,
	)
#tray.AddModule("i3ppc",
#	gpu = 0,
#	)
mmp.vbprint( "Added PPC to the tray.", [1,2] )

# Unify name for rest of icecube
tray.Add( "Rename", "PPCRename", Keys=["MCPESeriesMap", "I3MCPESeriesMap"] )

tray.Add( DetectorSim, "DetectorTrigger",
		  RandomService        = 'I3RandomService',
		  GCDFile              = gcdname,
		  InputPESeriesMapName = 'I3MCPESeriesMap',
		  SkipNoiseGenerator   = False,
		  RunID                = 0,
		  KeepPropagatedMCTree = True,
		  KeepMCHits           = True,
		  KeepMCPulses         = True,
		  LowMem               = False,
		  BeaconLaunches       = True,
		  TimeShiftSkipKeys    = [],
		  FilterTrigger        = True
	)
mmp.vbprint( "Added DetectorSim to the tray.", [1,2] )


# Writing out the files

tray.AddModule( "I3Writer",
	filename = outname_trigg,
	streams  = [ icetray.I3Frame.DAQ, icetray.I3Frame.Physics] ,
	SkipKeys = [ "I3MCPulseSeriesMapPrimaryIDMap" ],
	)
mmp.vbprint( "Added I3Writer to the tray, to write out the trigger level I3 file.", [1,2] )
print "nuclearite mass:", nuc_mass

print "NEV",nev
print "GCD",gcdname
print "SYSTEMATIC",args.systematic
print "ICEMODEL",icemodel
#print "DOMEFF",utils.systematic_domeff[args.systematic]
print "OUT GEN", outname_gen
print "OUT TRIGG", outname_trigg

# Finishing and executing

tray.AddModule("TrashCan","Trash") # perhaps not needed anymore
mmp.vbprint( "TrashCan added.", [1,2] )
mmp.vbprint( "Execution upcoming!", [1,2] )
tray.Execute()
mmp.vbprint( "Execution done!", [1,2] )
tray.Finish()
mmp.vbprint( "Tray finished!", [1,2] )
del tray
mmp.vbprint( "Tray deleted!", [1,2] )

mmp.finish()
