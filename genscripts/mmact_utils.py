from icecube import dataclasses, icetray
from icecube.icetray import I3Units
from icecube.dataclasses import I3MCTree, I3Particle
from icecube import icetray, dataclasses, dataio, tableio, common_variables, linefit, portia, recclasses, phys_services#, sim_services
from icecube import photonics_service, millipede
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

gen_params        = { "beta_spectrum":  [0.001,0.001], # [  0.750,  0.995  ],
											 
						"MeanFreePath":1 * I3Units.m,
                      "disk_distance":    1000.0    * I3Units.m,
                      "disk_radius":      1100.0    * I3Units.m,
                      "monopole_mass":       1.0e11 * I3Units.GeV,
                      "dist_to_cent_max": 2000.0    * I3Units.m,
                      "step_length_max":    10.0    * I3Units.m,   }

default_settings = { "n_events": 1000,
                     "icemodel": "$I3_BUILD/ppc/resources/ice/",
                     "gcd":      "/mnt/ceph1-npx/user/hhamdaoui/GeoCalibDetectorStatus_2016.57531_V0_SLOPified.i3.gz", }

supported_systematics = [ "baseline"            ,
                          "domeff_plus"         ,
                          "domeff_minus"        ,
                          "scat_plus_abs_plus"  ,
                          "scat_plus_abs_minus" ,
                          "scat_minus_abs_plus" ,
                          "scat_minus_abs_minus",
                          "angsens_set05"       ,
                          "angsens_set09"       ,
                          "angsens_set10"       ,
                          "angsens_set14"       , ]
#                          "p1_0.20_p2_0"        ,
#                          "p1_0.25_p2_-3"       ,
#                          "p1_0.25_p2_-1"       ,
#                          "p1_0.25_p2_0"        ,
#                          "p1_0.25_p2_+1"       ,
#                          "p1_0.30_p2_-3"       ,
#                          "p1_0.30_p2_-1"       ,
#                          "p1_0.30_p2_0"        ,
#                          "p1_0.30_p2_+1"       ,
#                          "p1_0.35_p2_0"        , ]

#systematic_icemodels  = { "baseline"             : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__baseline"             ,
#                          "domeff_plus"          : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__domeff_plus"          ,
#                          "domeff_minus"         : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__domeff_minus"         ,
#                          "scat_plus_abs_plus"   : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__scat_plus_abs_plus"   ,
#                          "scat_plus_abs_minus"  : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__scat_plus_abs_minus"  ,
#                          "scat_minus_abs_plus"  : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__scat_minus_abs_plus"  ,
#                          "scat_minus_abs_minus" : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__scat_minus_abs_minus" ,
#                          "p1_0.20_p2_0"         : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__p1_0.20_p2_0"         ,
#                          "p1_0.25_p2_-3"        : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__p1_0.25_p2_-3"        ,
#                          "p1_0.25_p2_-1"        : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__p1_0.25_p2_-1"        ,
#                          "p1_0.25_p2_0"         : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__p1_0.25_p2_0"         ,
#                          "p1_0.25_p2_+1"        : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__p1_0.25_p2_+1"        ,
#                          "p1_0.30_p2_-3"        : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__p1_0.30_p2_-3"        ,
#                          "p1_0.30_p2_-1"        : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__p1_0.30_p2_-1"        ,
#                          "p1_0.30_p2_0"         : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__p1_0.30_p2_0"         ,
#                          "p1_0.30_p2_+1"        : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__p1_0.30_p2_+1"        ,
#                          "p1_0.35_p2_0"         : "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1__p1_0.35_p2_0"         , }

icemodel_base = "/home/aburgman/icecode/sandbox/aburgman/systematics/systematics_ice_models/spice_3.2.1"
systematic_icemodels = { syskey: icemodel_base+"__{}".format(syskey) if "domeff" not in syskey else icemodel_base+"__baseline" for syskey in supported_systematics } # use with combo stable
#systematic_icemodels = { syskey: icemodel_base+"__{}".format(syskey)                                                           for syskey in supported_systematics } # use with simulation V06-01-01
systematic_domeff    = { syskey: 1.0                                 if "domeff" not in syskey else ( 1.1 if "plus" in syskey else 0.9 if "min" in syskey else np.nan ) for syskey in supported_systematics }


filename_template      = "TITLE_FLAVOR_IC86__beta_BETALOW_BETAHIGH__DATALEVEL_level__proc_PROCESSNUMBER.i3.gz"
filename_template_syst = "TITLE_FLAVOR_IC86__beta_BETALOW_BETAHIGH__DATALEVEL_level__SYSTEMATICVARIATION__proc_PROCESSNUMBER.i3.gz"


def get_systematics_icemodel(systematic):
	"""Returns the icemodel of the chosen systematic variation"""
	if systematic not in supported_systematics:
		exit("You are trying to simulate your sample using a non-supported systematic setting - switch to a supported one before I start wasting your time simulating something that you don't want!")
	return systematic_icemodels[systematic]








def check_monopole_lengths_10m(frame):
	"""Checking that all particles in the MCTree are monopoles, and that none of them have a too long length"""
	flavor = "monopole"
	tree   = frame["I3MCTree"]
	maxlength = 10. * I3Units.m
	#if any([ int(str(mm.type).lower()!=flavor) for mm in tree ]):
	#	exit( "Found non-monopole particle(-s) in the MCTree! This should never happen!" )
	#if any([ int(float(mm.length)>maxlength) for mm in tree ]):
		#exit( "Found too long monopole track segment(-s) in the MCTree! This is a bug that should have been fixed in the monopole-generator trunk!" )


class mmact_print:
	"""A class for printing info"""
	def __init__(self,intime=-1,verb=1):
		"""Print class initializer"""
		self.script_verbose_level = verb
		self.label                = "MMACT"
		self.label_spaces         = "     "
		import time
		self.starttime            = intime if intime>0. else time.time()
		self.starttime_struct     = time.localtime(self.starttime)
		self.sts                  = self.starttime_struct
		self.endtime_struct       = -1
		self.ets                  = self.endtime_struct
	def set_label_spaces(self):
		self.label_spaces = " "*len(self.label)
	def start(self):
		self.set_label_spaces()
		self.sts = self.starttime_struct
		print(  " ----------------------------------------- " )
		print(  "| Starting script at  {yr:04}-{mo:02}-{dy:02} {h:02}:{m:02}:{s:02} |".format( yr=self.sts.tm_year, mo=self.sts.tm_mon, dy=self.sts.tm_mday, h=self.sts.tm_hour, m=self.sts.tm_min, s=self.sts.tm_sec ) )
		print(  " ----------------------------------------- " )
		print(  "" )
	def finish(self):
		self.set_label_spaces()
		import time
		self.endtime_struct = time.localtime(time.time())
		self.ets = self.endtime_struct
		print(  " -{l}- ----------  ".format( l=self.label_spaces.replace(" ","-") ) )
		print(  "" )
		print(  " ----------------------------------------- " )
		print(  "| Finishing script at {yr:04}-{mo:02}-{dy:02} {h:02}:{m:02}:{s:02} |".format( yr=self.ets.tm_year, mo=self.ets.tm_mon, dy=self.ets.tm_mday, h=self.ets.tm_hour, m=self.ets.tm_min, s=self.ets.tm_sec ) )
		print(  " ----------------------------------------- " )
	def vbprint(self,the_string,accepted_verbose_levels,info_level=0):
		if self.script_verbose_level in accepted_verbose_levels:
			self.set_label_spaces()
			self.label      = str(self.label)
			self.the_string = str(the_string)
			import time
			self.time_now    = int(time.time()-self.starttime)
			if info_level==0:
				print(  " -{l}- ----------  ".format(             l=self.label_spaces.replace(" ","-") ) )
				print(  "| {l} | {h:02}:{m:02}:{s:02} | ".format( l=self.label        , h=self.time_now/3600, m=(self.time_now%3600)/60, s=self.time_now%60 ) + the_string )
			if info_level==1:
				print(  "| {l} | {h:02}:{m:02}:{s:02} | ".format( l=self.label_spaces , h=self.time_now/3600, m=(self.time_now%3600)/60, s=self.time_now%60 ) + the_string )
			if info_level==2:
				print(  "| {l} | {h:02}:{m:02}:{s:02} | ".format( l=self.label_spaces , h=self.time_now/3600, m=(self.time_now%3600)/60, s=self.time_now%60 ) + the_string )


def add_MCPrimaryParticle(frame):
	"""Adding the primary monopole as a separate object in the frame"""
	if "I3MCTree" in frame and "MCPrimaryParticle" not in frame:
		accepted_primaries = ["monopole","nue","nuebar","numu","numubar","nutau","nutaubar"]
		try:
			primaries = [ p for p in frame["I3MCTree"].get_primaries() if str(p.type).lower() in accepted_primaries ]
		except AttributeError:
			primaries = [ p for p in [ frame["I3MCTree"][0] ] if str(p.type).lower() in accepted_primaries ]
		if len(primaries)!=1:
			exit("Event nr {} has {} primary particles (neutrinos and monopoles counted) in it's MCTree! Deal with this case!".format(frame["I3EventHeader"].event_id,len(primaries)))
		primary = primaries[0]
		frame["MCPrimaryParticle"] = primary

def add_SystematicsMask(frame,syst):
	if "SystematicsMask" in frame:
		del frame["SystematicsMask"]
	syst = str(syst)
	systmask = { sk: (1 if sk==syst else 0) for sk in supported_systematics }
	if 1!=sum(systmask.values()):
		exit("You have {} values set in the systematics mask - this should always be 1!".format(sum(systmask.values())))
	frame["SystematicsMask"] = I3MapStringDouble( systmask )


#
#def get_key_from_filename(template, filename, key):
#	filename = (filename.split("/")[-1]).replace(".","_")
#	template = (template               ).replace(".","_")
#	filename = filename.replace("i3_bz2","i3.bz2").replace("i3_gz","i3.gz")
#	temp_dict = { t: f for t, f in zip(template.split("_"),filename.split("_")) }
#	part = "YOUR_KEY_DOES_NOT_MATCH_ANY_KEY_IN_THE_TEMPLATE"
#	part = temp_dict[key.upper()]
#	return part
#
# def SOME_RANDOM_SEED
