#!/bin/bash
# This is a wrapper script for submitting the MMACT generation script (necessary for the OGPU parameter)
# copied from /data/user/aburgman/icecode/sandbox/aburgman/mmact_genscripts/mmact_wrap_gen_prop_trigg.sh
while getopts n:d:e:p:r:g:m:s:t:v:B:z:a:c: option
do
case "${option}"
in
n) numevents=$OPTARG;;
d) outputdirgen=$OPTARG;;
e) outputdirtrigg=$OPTARG;;
p) iprocess=$OPTARG;;
r) nprocess=$OPTARG;;
g) gcdfilepath=$OPTARG;;
m) icemodelpath=$OPTARG;;
s) systematic=$OPTARG;;
t) title=$OPTARG;;
v) verbosity=$OPTARG;;
B) beta=$OPTARG;;
z) mass=$OPTARG;;
a) adius=$OPTARG;;
c) distance=$OPTARG;;

esac
done

export OGPU=1

export exestring="/data/user/hhamdaoui/nuclearite_analysis/genscripts/gen_prop_trigg.py"
if [ ${#numevents}      != 0 ] ; then export exestring="$exestring -n $numevents"      ; fi
if [ ${#outputdirgen}   != 0 ] ; then export exestring="$exestring -d $outputdirgen"   ; fi
if [ ${#outputdirtrigg} != 0 ] ; then export exestring="$exestring -e $outputdirtrigg" ; fi
if [ ${#iprocess}       != 0 ] ; then export exestring="$exestring -p $iprocess"       ; fi
if [ ${#nprocess}       != 0 ] ; then export exestring="$exestring -r $nprocess"       ; fi
if [ ${#gcdfilepath}    != 0 ] ; then export exestring="$exestring -g $gcdfilepath"    ; fi
if [ ${#icemodelpath}   != 0 ] ; then export exestring="$exestring -m $icemodelpath"   ; fi
if [ ${#systematic}     != 0 ] ; then export exestring="$exestring -s $systematic"     ; fi
if [ ${#title}          != 0 ] ; then export exestring="$exestring -t $title"          ; fi
if [ ${#verbosity}      != 0 ] ; then export exestring="$exestring -v $verbosity"      ; fi
if [ ${#beta}           != 0 ] ; then export exestring="$exestring -B $beta"           ; fi
if [ ${#mass}           != 0 ] ; then export exestring="$exestring -z $mass"           ; fi
if [ ${#radius}           != 0 ] ; then export exestring="$exestring -a $radius"           ; fi
if [ ${#distance}           != 0 ] ; then export exestring="$exestring -c $distance"           ; fi



echo "|            |     $exestring "

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
