#!/bin/sh /cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/icetray-start
#METAPROJECT /cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/RHEL_7_x86_64/metaprojects/combo/stable
# /data/user/aburgman/icecode/meta-projects/combo/stable_rev175960/RHEL_7_x86_64/


import time
script_start_time = time.time()

combo_stable = "/combo/stable_rev175960/"
icesim_v06   = "/icesim/V06-01-01/"

import os, sys
import argparse
import subprocess
from subprocess import call

import mmact_utils as utils

parser = argparse.ArgumentParser(description = "Wrapper L1 and L2.")
parser.add_argument( "-i", "--infile",   dest="infile",   type=str, default="", help="The input file to the L1 script."  )
parser.add_argument( "-b", "--betwfile", dest="betwfile", type=str, default="", help="The output file to the L1 script, and input file to the L2 script (the 'between file')." )
parser.add_argument( "-o", "--outfile",  dest="outfile",  type=str, default="", help="The output file to the L2 script." )
parser.add_argument( "-g", "--gcdfile",  dest="gcdfile",  type=str, default="", help="The GCD file to the L1 script."    )
parser.add_argument( "-v", "--verbose",  dest="verbose",  type=int, default=1,  help="How verbose is this script?"       )
args = parser.parse_args()

mmp = utils.mmact_print(script_start_time,args.verbose)
mmp.start()
mmp.label = "MMACT"
mmp.vbprint( "Imported Stuff",    [1,2] )
mmp.vbprint( "Loaded Stuff",      [1,2] )
mmp.vbprint( "Parsed Arguments",  [1,2] )

gcdname  = utils.default_settings["gcd"] if not args.gcdfile else args.gcdfile



mmp.vbprint( "Wrapper script running Level 1 and Level 2 (input {i}, output {o})".format(i=args.infile,o=args.outfile), [1,2] )
mmp.vbprint( "  Level 1:  input: {f}".format(f=args.infile),   [1,2], 1 )
mmp.vbprint( "           output: {f}".format(f=args.betwfile), [1,2], 1 )
mmp.vbprint( "  Level 2:  input: {f}".format(f=args.betwfile), [1,2], 1 )
mmp.vbprint( "           output: {f}".format(f=args.outfile),  [1,2], 1 )



mmp.vbprint( "Wrapping Level 1!", [1,2] )

mmp.vbprint( " start SimulationFiltering.py!", [1,2] )

#run_command  = "/home/aburgman/icecode/meta-projects/combo/stable_rev175960/src/filterscripts/resources/scripts/SimulationFiltering.py"
run_command  = '/data/user/hhamdaoui/nuc-analysis/SimulationFiltering.py'
run_command += " -i {i}".format( i=args.infile  )
run_command += " -o {o}".format( o=args.betwfile )
run_command += " -g {g}".format( g=gcdname      )
#run_command += " --disable-gfu"                   # No need for this, it has been switched to '--enable-gfu' with opposite functionality

exitstatus_L1 = subprocess.call( run_command.split(" ") )
mmp.vbprint( " end SimulationFiltering.py!", [1,2] )

mmp.vbprint( "Wrapped with status {s}!\n".format(s=exitstatus_L1), [1,2] )

if exitstatus_L1:
	sys.exit(exitstatus_L1)


mmp.vbprint( "Wrapping Level 2!", [1,2] )

#run_command  = "/home/aburgman/icecode/meta-projects/combo/stable_rev175960/src/filterscripts/resources/scripts/offlineL2/process.py"
run_command  = "/data/user/hhamdaoui/nuc-analysis/process.py"

run_command += " -i {i}".format( i=args.betwfile  )
run_command += " -o {o}".format( o=args.outfile )
run_command += " -g {g}".format( g=gcdname      )
run_command += " -s"

exitstatus_L2 = subprocess.call( run_command.split(" ") )

mmp.vbprint( "Wrapped with status {s}!\n".format(s=exitstatus_L2), [1,2] )

if exitstatus_L2:
	sys.exit(exitstatus_L2)



mmp.vbprint( "Everything seems to have gone as planned!\n", [1,2] )

exit()
