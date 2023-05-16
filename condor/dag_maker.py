import pydag
from datetime import datetime
import os
today = datetime.now()

condor_path="/home/hhamdaoui/condor/nuclearites/" + today.strftime("%m_%d_%Y_%H_%M_%S")+'/'
os.mkdir(condor_path)
os.mkdir(condor_path+"log/")

print(condor_path)
job = pydag.htcondor.HTCondorSubmit(condor_path+"OneJob.sub", "/data/user/hhamdaoui/nuclearite_analysis/genscripts/wrap_gen_prop_trigg.sh")
job.commands["initialdir"] = '/data/ana/BSM/IC86_MagneticMonopoles_AboveCherenkovThreshold/'

#job.commands["getenv"] = True
#job.commands["initialdir"] = "$ENV(HOME)"
job.commands["log"] = '$(LOGFILE).log'
job.commands["output"] = '$(LOGFILE).out'
job.commands["error"] = '$(LOGFILE).err'
job.commands["request_memory"] = '2.0 GB'
job.commands["request_disk"] = '1.0 GB'
job.commands["request_gpus"] = '1'
job.commands["should_transfer_files"] = 'YES'
job.commands["when_to_transfer_output"] = 'ON_EXIT'
job.commands["notification"] = 'ALWAYS'
job.commands["requirements"] = 'HAS_CUDA'
job.commands["requirements"] = 'CUDACapability'
job.commands["arguments"] = ' -n 10000 -d /data/user/hhamdaoui/MC_nuclearites/MC0_generated   -e /data/user/hhamdaoui/MC_nuclearites/MC1_L0_triggered -p $(Process) -r 1400  -s baseline  $(MASS) -t new_dir_R500_d700 -a 500 -c 700'

####end

masses=[5e12, 1e13,  1e14, 1e15,  1e16, 1e17]
#systematics=['p0=0.0_p1=0.0_domeff=1.00'] #baseline
#systematics=['a+.10' ,  'p0=0.0_p1=0.0_domeff=0.90' , 'p0=0.0_p1=-0.2_domeff=1.00' , 'p0=-1.0_p1=0.0_domeff=1.00' , 'p0=-2.0_p1=0.0_domeff=1.00',
# 'p0=0.0_p1=0.0_domeff=1.10' , 'p0=0.0_p1=0.2_domeff=1.00' ,  'p0=1.0_p1=0.0_domeff=1.00' ,  's+.10']
i=0


nodes = []
for mass in masses:
    mass_str='{:.0e}'.format(float(mass))
    mass_str=str(mass_str)
    node = pydag.dagman.DAGManNode(str(i), job)
    node.keywords["VARS"] = pydag.dagman.Macros(LOGFILE=condor_path+"log/"+mass_str+'_',MASS="-z "+mass_str)
    nodes.append(node)
    #print(systematic)
    #print(node)
    i += 1

#print('nodes:',nodes)
dag = pydag.dagman.DAGManJob(condor_path+"submit.dag", nodes)
#print('dag',dag)
dag.dump()
print(dag.written_to_disk)
