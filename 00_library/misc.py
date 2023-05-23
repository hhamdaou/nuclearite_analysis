import os
#import time, random, os, sys, json
#import numpy as np
#import scipy.constants as sc
#import matplotlib
#from matplotlib.colors import LogNorm

#from icecube import icetray#, dataclasses, dataio, tableio, common_variables, improvedLinefit, portia#, recclasses, sim_services, phys_services
#from icecube.icetray import I3Units
#from icecube.dataclasses import I3MCTree, I3Particle, I3RecoPulseSeriesMap, I3RecoPulse, I3MapStringDouble
#from icecube.tableio import I3TableWriter
#from icecube.hdfwriter import I3HDFTableService
#from I3Tray import *



class ABVerbosePrint:
	def __init__(self,intime=-1,verb=1):
		self.script_verbose_level = verb
		self.label1               = "AB"
		self.label2               = ""
		self.label1_spaces        = "  "
		self.label2_spaces        = ""
		import time
		self.starttime            = intime if intime>0. else time.time()
		self.starttime_struct     = time.localtime(self.starttime)
		self.sts                  = self.starttime_struct
		self.endtime_struct       = -1
		self.ets                  = self.endtime_struct
	def set_label_spaces(self):
		self.label1_spaces = " "*len(self.label1)
		self.label2_spaces = " "*len(self.label2)
	def start(self):
		self.set_label_spaces()
		self.sts = self.starttime_struct
		print(  " ----------------------------------------- " )
		print((  "| Starting script at  {yr:04}-{mo:02}-{dy:02} {h:02}:{m:02}:{s:02} |".format( yr=self.sts.tm_year, mo=self.sts.tm_mon, dy=self.sts.tm_mday, h=self.sts.tm_hour, m=self.sts.tm_min, s=self.sts.tm_sec ) ))
		print(  " ----------------------------------------- " )
		print(  "" )
	def finish(self):
		self.set_label_spaces()
		import time
		self.endtime_struct = time.localtime(time.time())
		self.ets = self.endtime_struct
		print((  " {lab1} {lab2} ----------  ".format(             lab1="--"+self.label1_spaces.replace(" ","-") , lab2="--"+self.label2_spaces.replace(" ","-") ,                                                                     )              ))
		print(  "" )
		print(  " ----------------------------------------- " )
		print((  "| Finishing script at {yr:04}-{mo:02}-{dy:02} {h:02}:{m:02}:{s:02} |".format( yr=self.ets.tm_year, mo=self.ets.tm_mon, dy=self.ets.tm_mday, h=self.ets.tm_hour, m=self.ets.tm_min, s=self.ets.tm_sec ) ))
		print(  " ----------------------------------------- " )
	def vbprint(self,the_string,accepted_verbose_levels,info_level=0):
		if self.script_verbose_level in accepted_verbose_levels:
			self.set_label_spaces()
			self.label1      = str(self.label1)
			self.label2      = str(self.label2)
			self.the_string  = str(the_string)
			import time
			self.time_now    = int(time.time()-self.starttime)
			if info_level==0:
				print((  " {lab1} {lab2} ----------  ".format(             lab1="--"+self.label1_spaces.replace(" ","-") , lab2="--"+self.label2_spaces.replace(" ","-") ,                                                                     )              ))
				print((  "| {lab1} | {lab2} | {h:02}:{m:02}:{s:02} | ".format( lab1=self.label1        , lab2=self.label2        , h=self.time_now/3600, m=(self.time_now%3600)/60, s=self.time_now%60 ) + the_string ))
			if info_level==1:
				print((  "| {lab1} | {lab2} | {h:02}:{m:02}:{s:02} | ".format( lab1=self.label1_spaces , lab2=self.label2        , h=self.time_now/3600, m=(self.time_now%3600)/60, s=self.time_now%60 ) + the_string ))
			if info_level==2:
				print((  "| {lab1} | {lab2} | {h:02}:{m:02}:{s:02} | ".format( lab1=self.label1_spaces , lab2=self.label2_spaces , h=self.time_now/3600, m=(self.time_now%3600)/60, s=self.time_now%60 ) + the_string ))


def add_to_list_uniquely(thelist,theaddition):
	thelist += [add for add in theaddition if add not in thelist]
	return thelist

def float_equalish(f1,f2,threshold=1e-9):
#	return -threshold<=(2*(f1-f2)/(f1+f2))<=threshold
	return -threshold<=(f1-f2)<=threshold

def float_inish(f,arr,threshold=1e-9):
	return any([ float_equalish(f,arrf,threshold) for arrf in arr ])

def str_to_prob(thestr):
	import hashlib, codecs
	thehash = hashlib.sha512
	maxhashplusone = 2**(thehash().digest_size*8)
	theseed = thestr.encode()
	hash_digest = thehash(theseed).digest()
	hash_int = int(codecs.encode(hash_digest, 'hex'), 16)
	return float(hash_int) / float(maxhashplusone)








def get_random_seed(run, process, time):
#	return run*1e12*process*1e6+int((time-int(time))*1e6)
#	return  int("1{r:06}{p:06}{t:06}".format(r=int(run),p=int(process),t=int((time-int(time))*1e6)))
	return  int("1{r:03}{p:04}{t:06}".format(r=int(run),p=int(process),t=int((time-int(time))*1e6)))





#:--
# OUTDATED BELOW HERE, EVEN?
#:--





def get_filenames_in_dir(indir,infiletype):
	inapp=".i3.bz2"
	if infiletype.lower()=="i3":
		inapp=".i3.bz2"
	if infiletype.lower()=="i3gz":
		inapp=".i3.gz"
	if infiletype.lower()=="hdf":
		inapp=".hd5"

	indir = os.path.abspath(indir)
	indir = indir if indir[-1] == "/" else indir+"/"
	indir = indir if indir[0] == "/"  else "/"+indir

	inlist = sorted(os.listdir(indir))
	inlist = [ inname for inname in inlist if inapp in inname ]
	inlist = [ indir + inname for inname in inlist ]

	return inlist

def get_icecube_level_from_key(LX):
	return int(LX.split("_")[0].split("L")[1])

def get_icecube_mc_i3file_name_template(num_dataset):
	template = "ERROR_you_need_to_give_a_dataset_number_that_we_have"
	if int(num_dataset)==11057 or int(num_dataset)==11937:
		template = "Level2_ICXX.YEAR_GENTYPE.RUNNUM.PROCNUM.i3.bz2"
	elif int(num_dataset)==11069 or int(num_dataset)==11070:
		template = "Level2_GENTYPE_PARTICLETYPE_ICXX.YEAR.RUNNUM.PROCNUM.i3.bz2"
	return template


def get_icecube_mc_missing_particletype(num_dataset):
	particletype = "any"
	if int(num_dataset)==11057 or int(num_dataset)==11937:
		particletype = "5-comp"
	return particletype


def get_icecube_mc_missing_otherspec(num_dataset):
	otherspec = "ERROR_you_need_to_give_a_dataset_number_that_we_have"
	if int(num_dataset)==11057 or int(num_dataset)==11937:
		otherspec = "energy-1e5GeV-1e11GeV-spectral-index-minus2"
	elif int(num_dataset)==11069:
		otherspec = "energy-1e2GeV-1e7GeV-spectral-index-minus1"
	elif int(num_dataset)==11070:
		otherspec = "energy-1e7GeV-1e9GeV-spectral-index-minus1"
	return otherspec


def get_icecube_mc_i3file_name_parts(name_file):
	parts     = {}
	name_file = name_file.replace(".i3.bz2","")

	parts["RUNNUM"]  = str( int( name_file.split(".")[-2] ) ).zfill(6)
	parts["PROCNUM"] = str( int( name_file.split(".")[-1] ) ).zfill(6)

	template  = get_icecube_mc_i3file_name_template( parts["RUNNUM"] )

	name_file = ".".join( name_file.split(".")[:-2] )
	template  = ".".join( template.split(".")[:-2] )

	name_file = name_file.replace("Level2_","")
	template  = template.replace("Level2_","")

	name_file = name_file.replace("_","/").replace(".","/")
	template  = template.replace("_","/").replace(".","/")

	name_file_parts = name_file.split("/")
	template_parts  = template.split("/")

	parts["ICXX"]         = name_file_parts[ template_parts.index("ICXX") ]
	parts["YEAR"]         = name_file_parts[ template_parts.index("YEAR") ]
	parts["GENTYPE"]      = name_file_parts[ template_parts.index("GENTYPE") ]

	if "PARTICLETYPE" in template_parts:
		parts["PARTICLETYPE"] = name_file_parts[ template_parts.index("PARTICLETYPE") ]
	else:
		parts["PARTICLETYPE"] = get_icecube_mc_missing_particletype( parts["RUNNUM"] )

	if "OTHERSPEC" in template_parts:
		parts["OTHERSPEC"]    = name_file_parts[ template_parts.index("OTHERSPEC") ]
	else:
		parts["OTHERSPEC"]    = get_icecube_mc_missing_otherspec( parts["RUNNUM"] )

	return parts


def get_aburgman_icecube_mc_i3file_name(name_template, name_icecube):
	parts = get_icecube_mc_i3file_name_parts(name_icecube)

	name_aburgman = name_template
	for key in list(parts.keys()):
		if key in name_aburgman:
			name_aburgman = name_aburgman.replace( key, parts[key] )
			# The keys should be ICXX, YEAR, GENTYPE, PARTICLETYPE, RUNNUM, PROCNUM, OTHERSPEC

	return name_aburgman


def get_aburgman_output_file_name(name_in, dir_out, type_out):
	app_i3  = ".i3.bz2"
	app_hdf = ".hd5"

	if dir_out.lower() == "same":
		dir_out = "/".join( name_in.split("/")[:-1] )
	if dir_out[-1]!="/":
		dir_out += "/"

	name_in = name_in.split("/")[-1]
	if name_in[-len(app_i3):] == app_i3:
		name_in = name_in[:-len(app_i3)]
	if name_in[-len(app_hdf):] == app_hdf:
		name_in = name_in[:-len(name_hdf)]

	if type_out.lower()=="i3":
		name_in += app_i3
	if type_out.lower()=="hdf":
		name_in += app_hdf

	return dir_out + name_in


def get_aburgman_next_level_directory(dir_in):
	app_i3    = ".i3"
	app_i3bz2 = ".i3.bz2"

#	print "\n\n",dir_in,"\n\n"

	dir_parts = dir_in.split("/")

	dir_parts = [ part for part in dir_parts if part!="" ]

#	print "\n\n",dir_parts,"\n\n"

	if dir_parts[-1][-len(app_i3):] == app_i3:
		dir_parts = dir_parts[:-1]
	if dir_parts[-1][-len(app_i3bz2):] == app_i3bz2:
		dir_parts = dir_parts[:-1]

#	print "\n\n",dir_parts,"\n\n"

	dir_new   = dir_parts[-1]

#	print "\n\n",dir_new,"\n\n"

	index_L = [ ind for ind in range(len(dir_new)) if dir_new.startswith("L", ind)]
	index_L = [ ind for ind in index_L if dir_new[ind+1].isdigit() ]

#	print "\n\n",index_L,"\n\n"

	if len(index_L) == 1:
		length_level = 0
		while dir_new[index_L[0]+1+length_level].isdigit():
			length_level += 1
		level_this = dir_new[index_L[0]:index_L[0]+1+length_level]
		level_next = "L"+str(int(level_this[1:])+1)
		dir_new = dir_new.replace( level_this, level_next )
	else:
		dir_new = "CANNOT_FIND_THE_LEVEL"

#	print "\n\n",dir_new,"\n\n"

	dir_out = "/".join( dir_parts[:-1] + [dir_new] )
	if dir_out[0]!="/":
		dir_out = "/" + dir_out

	return dir_out


'''
def get_aburgman_output_i3file_name(name_inputfile, origin_inputfile, nametemplate_inputfile, datatype_inputfile, directory_outputfile):
#def get_output_i3file_name(name_inputfile, nametemplate_inputfile, datatype_inputfile, directory_outputfile):


# STORE THE TEMPLATES OF BACKGROUND IN LIBRARY, AS BACKGROUNDTEMPLATES OR SOMETHING; AND THE KEY BEING THE RUN NUMBER
# THEN STUFF CAN JUST BE EXTRACTED FROM THERE


#	name_outputfile = "ERROR_you_must_set_the_parameter_called_origin_inputfile_to_either_aburgman_or_icecube"

#	if origin_inputfile.lower()=="aburgman" or origin_inputfile.lower()=="icecube":
#		if origin_inputfile.lower()=="aburgman":
##			EXTRACT PARTS OF FILENAME THIS WAY
#		elif origin_inputfile.lower()=="icecube":
##			EXTRACT PARTS OF FILENAME THIS WAY
##		PUT TOGETHER PARTS OF FILENAME


#	datatype is either background_mc, signal_mc or data
#	if origin_input==icecube then template is taken from function above, not from here 

	name_outputfile = "ERROR_STUFF_IS_NOT_WORKING"

	if origin_inputfile.lower()=="aburgman" or origin_inputfile.lower()=="icecube":
		if origin_inputfile.lower()=="aburgman":
#			EXTRACT PARTS OF FILENAME THIS WAY
		elif origin_inputfile.lower()=="icecube":
#			EXTRACT PARTS OF FILENAME THIS WAY
#		PUT TOGETHER PARTS OF FILENAME



	return name_outputfile
'''
'''
def get_aburgman_output_hdffile_name(XXXXXXXX):
	pass
'''











#:--
# OUTDATED BELOW?
#:--

def get_background_filename_icecube(descr, templ, direc, subdirec):
	dir_bg = direc
	app_bg = ".i3.bz2"
	sub_bg = "background_"+subdirec.split("_")[1]

	parts_descr = (descr.replace(dir_bg,"").replace(app_bg,"").replace(sub_bg,"")).split("_")
	parts_templ = (templ.replace(dir_bg,"").replace(app_bg,"").replace(sub_bg,"")).split("_")

	part_icxx         = parts_descr[parts_templ.index("ICXX")]
	part_year         = parts_descr[parts_templ.index("YEAR")]
	part_gentype      = parts_descr[parts_templ.index("GENTYPE")]
	part_particletype = parts_descr[parts_templ.index("PARTICLETYPE")]
	part_runnumber    = str(int(parts_descr[parts_templ.index("RUNNUMBER")])).zfill(6)
	part_subnumber    = str(int(parts_descr[parts_templ.index("SUBNUMBER")])).zfill(6)

	nam_bg = "background_L2__" + part_icxx + "_" + part_year + "_" + part_gentype

	if "nugen" in part_gentype.lower():
		nam_bg = nam_bg + "_" + part_particletype.lower()
		if int(part_runnumber)==11069:
			nam_bg = nam_bg + "_LE"
		if int(part_runnumber)==11070:
			nam_bg = nam_bg + "_HE"

	nam_bg = nam_bg +"/" + str(int(part_subnumber)-(int(part_subnumber)%1000)).zfill(5) + "-" + str(int(part_subnumber)-(int(part_subnumber)%1000)+999).zfill(5) + "/Level2_"

	if "nugen" in part_gentype.lower():
		nam_bg = nam_bg + part_gentype.lower() + "_" + part_particletype.lower() + "_"

	nam_bg = nam_bg + part_icxx + "."

	if "corsika" in part_gentype.lower():
		nam_bg = nam_bg + str(int(part_year)-1) + "_corsika"
	else:
		nam_bg = nam_bg + part_year

#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
	nam_bg = nam_bg + "." + str(int(part_runnumber)).zfill(6) + "." + str(int(part_subnumber)).zfill(6)

	filename = dir_bg + nam_bg + app_bg

	return str(filename)


def get_background_filename_aburgman(descr, templ, direc, subdirec):
	dir_bg = direc
	app_bg = ".i3.bz2"
	sub_bg = "background_"+subdirec.split("_")[1]

	parts_descr = (descr.replace(dir_bg,"").replace(app_bg,"").replace("background_L2__","")).split("_")

	part_icxx    = parts_descr[0]
	part_year    = parts_descr[1]
	part_gentype = parts_descr[2].split("/")[0]

	if "nugen" in part_gentype.lower():
		part_particletype = parts_descr[3]
	if "corsika" in part_gentype.lower():
		part_particletype = "any"

	part_runnumber    = str(int(parts_descr[-1].split(".")[-2])).zfill(6)
	part_subrunnumber = str(int(parts_descr[-1].split(".")[-1])).zfill(6)

	nam_bg = (templ.split("/")[0]).replace(app_bg,"")
	nam_bg = nam_bg.replace("ICXX",part_icxx)
	nam_bg = nam_bg.replace("YEAR",part_year)
	nam_bg = nam_bg.replace("GENTYPE",part_gentype)
	nam_bg = nam_bg.replace("PARTICLETYPE",part_particletype)
	nam_bg = nam_bg.replace("RUNNUMBER",part_runnumber)
	nam_bg = nam_bg.replace("SUBNUMBER",part_subrunnumber)

	filename = dir_bg + sub_bg + nam_bg + app_bg

	return str(filename)


def get_beta(gamma="",beta="",betagamma=""):
	import numpy as np
	in_beta      = True if beta else False
	in_gamma     = True if gamma else False
	in_betagamma = True if betagamma else False
	if int(in_beta)+int(in_gamma)+int(in_betagamma)!=1:
		exit("You need to input one and only one input argument!")
	if in_beta:
		beta = float(beta)
		if beta>1. or beta<0.:
			return np.nan # Beta is out of range!
		return beta
	if in_gamma:
		gamma = float(gamma)
		if gamma<0.:
			return np.nan # Gamma is out of range!
		return np.sqrt(1.-gamma**(-2))
	if in_betagamma:
		return np.nan # Betagamma is not implmented yet

def get_gamma(beta="",gamma="",betagamma=""):
	import numpy as np
	in_beta      = True if beta else False
	in_gamma     = True if gamma else False
	in_betagamma = True if betagamma else False
	if int(in_beta)+int(in_gamma)+int(in_betagamma)!=1:
		exit("You need to input one and only one input argument!")
	if in_beta:
		beta = float(beta)
		if beta>1. or beta<0.:
			return np.nan # Beta is out of range!
		return 1./np.sqrt(1.-beta**2)
	if in_gamma:
		gamma = float(gamma)
		if gamma<0.:
			return np.nan # Gamma is out of range!
		return gamma
	if in_betagamma:
		return np.nan # Betagamma is not implmented yet

def get_betagamma(gamma="",beta="",betagamma=""):
	import numpy as np
	in_beta      = True if beta else False
	in_gamma     = True if gamma else False
	in_betagamma = True if betagamma else False
	if int(in_beta)+int(in_gamma)+int(in_betagamma)!=1:
		exit("You need to input one and only one input argument!")
	if in_beta:
		beta = float(beta)
		if beta>1. or beta<0.:
			exit("Beta is out of range!")
		return 1./np.sqrt(beta**(-2)-1.)
	if in_gamma:
		gamma = float(gamma)
		if gamma<0.:
			exit("Gamma is out of range!")
		return np.sqrt(gamma**(2)-1.)
	if in_betagamma:
		betagamma = float(betagamma)
		beta  = get_beta(betagamma=betagamma)
		gamma = get_gamma(betagamma=betagamma)
		if np.isnan(beta) or np.isnan(gamma):
			return np.nan
		if betagamma!=beta*gamma:
			return "FUCK! This wasn't supposed to happen!"
		return betagamma

