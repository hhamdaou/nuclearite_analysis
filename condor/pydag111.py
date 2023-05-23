import pydag
from datetime import datetime
import os
today = datetime.now()

condor_path="/home/hhamdaoui/condor/nuclearites/corsika_l2/" + today.strftime("%m_%d_%Y_%H_%M_%S")+'/'
os.mkdir(condor_path)
os.mkdir(condor_path+"log/")

print(condor_path)
job = pydag.htcondor.HTCondorSubmit(condor_path+"job.sub", "/data/user/hhamdaoui/nuclearite_analysis/analysis_scripts/corsika_l2_h5writer_grid.py")
job.commands["arguments"] = '$(DATASET) '
job.commands["getenv"] = True
job.commands["initialdir"] = "$ENV(HOME)"
job.commands["log"] = '$(LOGFILE).log'
job.commands["output"] = '$(LOGFILE).out'
job.commands["error"] = '$(LOGFILE).err'
job.commands["request_memory"] = '5.0 GB'


#corsika
datasets=[20783	,  20782, 20781	,  20780	, 20779	, 20778	,  20777	,  20783]

#systematics=['a+.10' ,  'p0=0.0_p1=0.0_domeff=0.90' , 'p0=0.0_p1=-0.2_domeff=1.00' , 'p0=-1.0_p1=0.0_domeff=1.00' , 'p0=-2.0_p1=0.0_domeff=1.00',
# 'p0=0.0_p1=0.0_domeff=1.10' , 'p0=0.0_p1=0.2_domeff=1.00' ,  'p0=1.0_p1=0.0_domeff=1.00' ,  's+.10']
i=0
nodes = []
for dataset in datasets:
    node = pydag.dagman.DAGManNode(str(i), job)
    node.keywords["VARS"] = pydag.dagman.Macros(LOGFILE=condor_path+"log/"+str(dataset)+'_',DATASET="--dataset "+str(dataset))
    nodes.append(node)
    #print(systematic)
    #print(node)
    i += 1
#print('nodes:',nodes)
dag = pydag.dagman.DAGManJob(condor_path+"example.dag", nodes)
#print('dag',dag)
dag.dump()
print(dag.written_to_disk)
