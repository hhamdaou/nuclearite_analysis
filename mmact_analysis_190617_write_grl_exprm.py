#!/bin/sh /cvmfs/icecube.opensciencegrid.org/py2-v2/icetray-start
#METAPROJECT /data/user/aburgman/icecode/meta-projects/combo/stable_rev175960/RHEL_7_x86_64
# /data/user/aburgman/icecode/meta-projects/combo/stable_rev175960/RHEL_7_x86_64/

import time
script_start_time = time.time()

combo_stable = "/combo/stable_rev175960/"
icesim_v06   = "/icesim/V06-01-01/"

import random, os, sys
import numpy as np
import argparse,warnings
from icecube.phys_services import goodrunlist
import mmact_analysis_utils    as utils
\
#:--
# PREPARATIONS
#:--

parser = argparse.ArgumentParser(description = "Printing out the GRL for experimental files.")
parser.add_argument( "-v", "--verbose",  dest="verbose",    type=int,            default=1,     help="How verbose is this script?"                          )
args = parser.parse_args()

mmp = utils.mmact_print(script_start_time,args.verbose)
mmp.start()
mmp.label = "MMACT"
mmp.vbprint( "Imported Stuff",    [1,2] )
mmp.vbprint( "Loaded Stuff",      [1,2] )
mmp.vbprint( "Parsed Arguments",  [1,2] )


grl = goodrunlist.GRL_pass2()

#detyrs = [ "IC86.20{}".format(int(a)) for a in np.linspace(1,8,8) ]
#detyrs = [ "IC86.20{}".format(int(a)) for a in np.linspace(11,21,11) ]

detyrs = [ "IC86.20{}".format(int(a)) for a in np.linspace(19,19,1) ]

runnums_phys = { yr: [] for yr in detyrs }
runnums_burn = { yr: [] for yr in detyrs }

def is_burn(det,rn):
	this_is_burn = False
	# Burnsample only for IC86.2011 - IC86.2015
	if det[-4:] in [ "201{}".format(int(a)) for a in np.linspace(1,9,9) ]:
		# Burnsample only if runnumber ends with '0'
		if str(rn)[-1]=="0":
			this_is_burn = True
	return this_is_burn

def get_gcd_and_files(runinfo):
	return " ".join( [  ] + runinfo.get_files() )

mmp.vbprint( "Adding runnums to physics and burnsample lists", [1,2] )

for runnum in sorted(grl.keys()):
    if grl[runnum]["detector"] in detyrs and grl[runnum]["good_i3"] and grl[runnum]["good_it"]:
        if not is_burn( grl[runnum]["detector"], runnum ):
            runnums_phys[grl[runnum]["detector"]] += [runnum]
        else:
            runnums_burn[grl[runnum]["detector"]] += [runnum]

print_phys = { yr: "" for yr in detyrs }
print_burn = { yr: "" for yr in detyrs }
print(print_burn)
time_phys  = { yr: 0. for yr in detyrs }
time_burn  = { yr: 0. for yr in detyrs }

mmp.vbprint( "Adding physics files in list", [1,2] )


mmp.vbprint( "Adding burnsample files in list", [1,2] )

for yr in detyrs:
	rn_count = 0
	for rn in runnums_burn[yr]:
		mmp.vbprint( "burn season {}, run counter {:4}".format(yr,rn_count), [1,2], 2 ) 
		rn_count += 1
		print_burn[yr] += get_gcd_and_files(grl[rn])
		for file in print_burn[yr]:
			print(file)

		time_burn[yr]  += grl[rn]["livetime"]
		# print six files per line
		#print(print_burn[yr])
		print_burn[yr] += "\n"

mmp.vbprint( "Cropping and printing out the files", [1,2] )

for yr in detyrs:
	if print_phys[yr]:
		while print_phys[yr][-1]=="\n" or print_phys[yr][-1]==" ":
			print_phys[yr] = print_phys[yr][:-1]
	if print_burn[yr]:
		while print_burn[yr][-1]=="\n" or print_burn[yr][-1]==" ":
			print_burn[yr] = print_burn[yr][:-1]

#runnum_file_phys = { yr: open( utils.mmactdir+"/mmact_exprm__GRL_filtered__{}_{}.txt".format(yr,"phys"), "w" ) for yr in detyrs }
runnum_file_burn = { yr: open( utils.mmactdir+"/mmact_exprm__GRL_filtered__{}_{}.txt".format(yr,"burn"), "w" ) for yr in detyrs }

#time_file_phys = open( utils.mmactdir+"/mmact_exprm__livetime__{}.txt".format("phys"), "w" )
time_file_burn = open( utils.mmactdir+"/mmact_exprm__livetime__{}.txt".format("burn"), "w" )

for yr in detyrs:
	#runnum_file_phys[yr].write( print_phys[yr] )
	runnum_file_burn[yr].write( print_burn[yr] )

for yr in detyrs:
	#runnum_file_phys[yr].close()
	runnum_file_burn[yr].close()

#time_file_phys.write( "\n".join([ "{} {}".format(yr,time_phys[yr]) for yr in detyrs ]) )
time_file_burn.write( "\n".join([ "{} {}".format(yr,time_burn[yr]) for yr in detyrs ]) )

#time_file_phys.close()
time_file_burn.close()

mmp.finish()

