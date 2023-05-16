#!/bin/bash
# This is a wrapper script for submitting the MMACT generation script (necessary for the OGPU parameter)

while getopts i:b:o:g:v: option
do
case "${option}"
in
i) infile=$OPTARG;;
b) betwfile=$OPTARG;;
o) outfile=$OPTARG;;
g) gcdfile=$OPTARG;;
v) verbosity=$OPTARG;;
esac
done

# Using with meta-project combo (rev 175960)
export exestring="/data/user/hhamdaoui/nuclearite_analysis/genscripts/L1_L2_proc.py"
if [ ${#infile}    != 0 ] ; then export exestring="$exestring -i $infile"   ; fi
if [ ${#betwfile}  != 0 ] ; then export exestring="$exestring -b $betwfile" ; fi
if [ ${#outfile}   != 0 ] ; then export exestring="$exestring -o $outfile"  ; fi
if [ ${#gcdfile}   != 0 ] ; then export exestring="$exestring -g $gcdfile"  ; fi
if [ ${#verbosity} != 0 ] ; then export exestring="$exestring -v $verbosity"; fi


echo " ------------ "
echo "| MMACT WRAP | About to run the following script "
echo "|            |     $exestring "
echo " ------------ "
echo " "
$exestring
export WRAPPED_SCRIPT_EXIT_STATUS=$?
echo " "
echo " ------------ "
echo "| MMACT WRAP | Finished running the following script with status $WRAPPED_SCRIPT_EXIT_STATUS:"
echo "|            |     $exestring"
echo " ------------ "

exit $WRAPPED_SCRIPT_EXIT_STATUS
