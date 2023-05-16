import pydag
from datetime import datetime
import os
today = datetime.now()

condor_path="/home/hhamdaoui/condor/nuclearites/MC2_MC3_L1_L2_proc/" + today.strftime("%m_%d_%Y_%H_%M_%S")+'/'
os.mkdir(condor_path)
os.mkdir(condor_path+"log/")

print(condor_path)
job = pydag.htcondor.HTCondorSubmit(condor_path+"OneJob.sub", "/data/user/hhamdaoui/nuclearite_analysis/genscripts/wrap_L1_L2_proc.sh")
job.commands["initialdir"] = '/data/ana/BSM/IC86_MagneticMonopoles_AboveCherenkovThreshold/'
LOGFILE=condor_path+"log/$Fn(file).$(cluster).$(Process)"

#job.commands["getenv"] = True
#job.commands["initialdir"] = "$ENV(HOME)"
job.commands["log"] = LOGFILE+'.log'
job.commands["output"] = LOGFILE+'.out'
job.commands["error"] = LOGFILE+'.err'
job.commands["request_memory"] = '4.0 GB'
job.commands["request_disk"] = '2.0 GB'
job.commands["should_transfer_files"] = 'YES'
job.commands["when_to_transfer_output"] = 'ON_EXIT'
job.commands["notification"] = 'ALWAYS'
job.commands["arguments"] = '-i $Fp(file)/$Fnx(file) -b /data/user/hhamdaoui/MC_nuclearites/MC2_L1_poleprocessed/$Fnx(file) -o /data/user/hhamdaoui/MC_nuclearites/MC3_L2_northprocessed/$Fnx(file)'
job.queue = 'file from /data/user/hhamdaoui/MC_nuclearites/filenames_MC1.txt'
job.dump()
####end
