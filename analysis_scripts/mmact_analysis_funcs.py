import time
import random, os, sys, json
import numpy as np
import scipy as sp
import scipy.constants as spco
import scipy.stats as spst

from icecube import icetray, dataclasses, dataio, tableio, common_variables, linefit, portia, recclasses, phys_services#, sim_services
from icecube import photonics_service, millipede, DomTools
from icecube.icetray import I3Units
from icecube.dataclasses import I3Double, I3String
from icecube.dataclasses import I3MCTree, I3Particle, I3RecoPulseSeriesMap, I3RecoPulse, I3MapStringDouble
from icecube.recclasses import I3PortiaEvent, I3DirectHitsValues, I3TrackCharacteristicsValues
from icecube.tableio import I3TableWriter
from icecube.hdfwriter import I3HDFTableService
from icecube.common_variables import direct_hits
from icecube.common_variables import hit_multiplicity
from icecube.common_variables import hit_statistics
from icecube.common_variables import track_characteristics
from icecube.common_variables import time_characteristics
from icecube import dataclasses, icetray
from icecube.icetray import I3Units
from icecube.dataclasses import I3MCTree, I3Particle

#:--
# MISC FUNTIONS
#:--


def float_equalish(f1,f2,threshold=1e-9):
#	return -threshold<=(2*(f1-f2)/(f1+f2))<=threshold
	return -threshold<=(f1-f2)<=threshold

def float_inish(f,arr,threshold=1e-9):
	return any([ float_equalish(f,arrf,threshold) for arrf in arr ])

#:--
# CUT FUNCTIONS
#:--

# MCPrimaryParticle energy
def keep_mcprimaryenergy_above_value(frame, gen, value):
	passed_cut = False
	if gen!="nugen":
		exit("Hang on, only NUGEN events should arrive to this function!?!")
	elif frame.Has("MCPrimaryParticle"):
		if frame["MCPrimaryParticle"].energy/I3Units.GeV>=value:
			passed_cut = True
	return passed_cut
def keep_nugen_mcprimaryenergy_above_1e5GeV(frame):
	return keep_mcprimaryenergy_above_value(frame,"nugen",1e5*I3Units.GeV)

# Checking for EHE objects
def keep_has_ehe_objects(frame):
	passed_cut = False
	passed_cut = frame.Has("EHEOpheliaParticleSRT_ImpLF") and frame.Has("EHEOpheliaSRT_ImpLF") and frame.Has("EHEPortiaEventSummarySRT")
	#if passed_cut is True:
		#print 'passed EHE cut :', passed_cut
	return passed_cut

# slop filter 
def keep_slop(frame):
	passed_cut = False
	if frame.Has("SLOPTuples_CosAlpha_Launches"):
		passed_cut = True
		#if passed_cut is True:
			#print 'passed SLOP cut :', passed_cut
	return passed_cut


	
# npe
def keep_npe_above_value(frame, value):
	passed_cut = False
	if frame.Has("EHEPortiaEventSummarySRT"):
		if frame["EHEPortiaEventSummarySRT"].GetTotalBestNPE()>=value:
			passed_cut = True
		if passed_cut is True:
			print('passed npe cut :', passed_cut)
	return passed_cut
#def cut_eheana_npe_above_25000(frame):
#	return cut_eheana_npe_above_value(frame,25000.)

# nch
def keep_nch_above_value(frame, value):
	passed_cut = False
	if frame.Has("EHEPortiaEventSummarySRT"):
		if frame["EHEPortiaEventSummarySRT"].GetTotalNch()>=value:
			passed_cut = True
		if passed_cut is True:
			print('passed Nch cut :', passed_cut)
	return passed_cut
#def cut_eheana_nch_above_100(frame):
#	return cut_eheana_nch_above_value(frame,100.)

# fit_quality
def keep_fitquality_above_value(frame, value):
	passed_cut = False
	if frame.Has("EHEOpheliaSRT_ImpLF"):
		if frame["EHEOpheliaSRT_ImpLF"].fit_quality>=value:
			passed_cut = True
		if passed_cut is True:
			print('passed fit_quality cut :', passed_cut)
	return passed_cut
#def cut_eheana_fitquality_above_30(frame):
#	return cut_eheana_fitquality_above_value(frame,30.)

# log10(npe)
def keep_log10npe_above_value(frame, value):
	passed_cut = False
	if frame.Has("EHEPortiaEventSummarySRT"):
		if np.log10(frame["EHEPortiaEventSummarySRT"].GetTotalBestNPE())>=value:
			passed_cut = True
		if passed_cut is True:
			print('passed log10(npe) cut :', passed_cut)
	return passed_cut

# log10(npe) depending on fit_quality
def keep_log10npe_depending_on_fitquality(frame):
	log10npe_limit = -1.
	fitquality     = -1.
	passed_cut = False
	if frame.Has("EHEOpheliaSRT_ImpLF"):
		fitquality = frame["EHEOpheliaSRT_ImpLF"].fit_quality
	else:
		return passed_cut
	if fitquality < 30:
		return passed_cut
	if fitquality < 80:     # i.e. if 30 < fit_quality <= 80
		log10npe_limit = 4.6
	elif fitquality < 120:  # i.e. if 80 < fit_quality <= 120
		log10npe_limit = 4.6+0.015*(fitquality-80)
	else:                    # i.e. if 120 < fit_quality
		log10npe_limit = 5.2
	passed_cut = keep_log10npe_above_value(frame,log10npe_limit)
	if passed_cut is True:
		print('passed log10(npe) depending on fit_quality :', passed_cut)
	return passed_cut

# log10(npe) depending on cos(zenith)
def keep_log10npe_depending_on_coszenith(frame):
	log10npe_limit = -1.
	coszenith      = 2.
	passed_cut = False
	if frame.Has("EHEOpheliaParticleSRT_ImpLF"):
		coszenith = np.cos(frame["EHEOpheliaParticleSRT_ImpLF"].dir.zenith)
	else:
		return passed_cut
	if coszenith < 0.06:
		log10npe_limit = 4.6
	else:
		log10npe_limit = 4.6 + 1.85*np.sqrt(1-((coszenith-1.)/0.94)**2)
	passed_cut = keep_log10npe_above_value(frame,log10npe_limit)
	if passed_cut is True:
		print('log10(npe) depending on cos(zenith):', passed_cut)
	return passed_cut

# decrease counting weight of each event
def keep_icetop_count_decrease(frame):
	add_CountingWeightFactor(frame)
	old_cwf=frame["CountingWeightFactor"].value
	new_cwf=I3Double(old_cwf*0.894)
	del frame["CountingWeightFactor"]
	frame["CountingWeightFactor"]=new_cwf
	passed_cut = True
	return passed_cut

## BDT E score must be above 0.087XXXXXXXXX
#def cut_bdt_e_below_0p108(frame):
#	bdt_score_cut = 0.108
#	passed_cut    = False
#	if frame.Has("BDTEScore"):
#		bdt_score = frame["BDTEScore"]
#	else:
#		return passed_cut
#	passed_cut = ( bdt_score >= bdt_score_cut )
#	return passed_cut



def cut_analysis(frame,lev,gen):
	passed_cut = False

	# Trigger Level
	if lev=="trigger":
		passed_cut = True
		if passed_cut is False:
			print('Trigger Failed')
	# Trigger Level
	if lev=="ehefilter":
		passed_cut = keep_slop(frame)
		#if passed_cut is True:
		#	print 'Slop passed'
			
		
	# Filter Level
	if lev=="ehefilter":
		passed_cut = keep_has_ehe_objects(frame)
		#if passed_cut is True:
			#print 'ehefilter passed'

	# Level 2
	if lev=="L2":
		passed_cut_1 = keep_npe_above_value(frame,25000.)
		passed_cut_2 = keep_nch_above_value(frame,100.)
		passed_cut_3 = keep_fitquality_above_value(frame,30.)
		passed_cut = passed_cut_1 and passed_cut_2 and passed_cut_3
		#if passed_cut is True:
			#print 'L2 passed'
		

	# Level 3
	if lev=="L3":
		passed_cut = keep_log10npe_depending_on_fitquality(frame)
		#if passed_cut is True:
			#print 'L3 passed'

	# Level 4
	if lev=="L4":
		passed_cut = keep_log10npe_depending_on_coszenith(frame)
		#if passed_cut is True:
			#print 'L4 passed'

	# Level 5
	if lev=="L5":
		if gen!="exprm":
			passed_cut = keep_icetop_count_decrease(frame)
		else:
			passed_cut = True
		#if passed_cut is True:
			#print 'L5 passed'
#			warnings.warn("Implement IceTop Veto for EXPRM data!")

	# Level 6
	if lev=="L6":
	#	passed_cut = cut_bdt_e_below_0p108(frame)
		passed_cut = True
		#if passed_cut is True:
			#print 'L6 passed'

	return passed_cut



## L1
#def cut_eheana_L1(frame):
#	passed_cut = False
##	passed_cut = cut_eheana_npe_above_1000(frame)
#	passed_cut = cut_eheana_has_ehe_objects(frame)
#	return passed_cut
#
## L2
#def cut_eheana_L2(frame):
#	passed_cut = False
#	passed_cut_1 = cut_eheana_npe_above_25000(frame)
#	passed_cut_2 = cut_eheana_nch_above_100(frame)
#	passed_cut_3 = cut_eheana_fitquality_above_30(frame)
#	passed_cut = passed_cut_1 and passed_cut_2 and passed_cut_3
#	return passed_cut
#
## L3
#def cut_eheana_L3(frame):
#	passed_cut = False
#	passed_cut = cut_eheana_log10_npe_depending_on_fitquality(frame)
#	return passed_cut
#
## L4
#def cut_eheana_L4(frame):
#	passed_cut = False
#	passed_cut = cut_eheana_log10_npe_depending_on_coszenith(frame)
#	return passed_cut
#
## L5
#def cut_eheana_L5(frame):
#	passed_cut = False
#	passed_cut = cut_eheana_icetop_count_decrease(frame)
#	return passed_cut
#
## L6
#def cut_L6(frame):
#	passed_cut = False
#	passed_cut = cut_bdt_e_below_0p108(frame)
##	passed_cut = True
#	return passed_cut

def is_standard_candle_event(runid,eventid):
	# Standard Candle events, ( run_ID, event_ID )
	# https://wiki.icecube.wisc.edu/index.php/Standard_Candle#Light_Contamination
	run_event_IDs = [ ( 117442, 479006   ),
		              ( 117442, 716661   ),
		              ( 120937, 38666872 ),
		              ( 120937, 38666982 ),
		              ( 120937, 38667723 ),
		              ( 120944, 26997195 ),
		              ( 120944, 26997282 ), # Calliandra
		              ( 120944, 26998041 ),
		              ( 125911, 18778204 ), ]
	return ( (runid,eventid) in run_event_IDs )

def cut_standard_candle_events(frame):
	passed_cut = True
	if is_standard_candle_event( int(frame["I3EventHeader"].run_id), int(frame["I3EventHeader"].event_id) ):
		passed_cut = False
	return passed_cut

#:--
# QUICK AND DIRTY
#:--

def get_flavor_qad(filename):
	filename = str(filename).split("/")[-1]
	accepted_flavors = [ "monopole", "nue", "numu", "nutau" ]
	detected_flavors = [ af for af in accepted_flavors if "_{}_".format(af) in filename ]
	if len(detected_flavors)!=1:
		exit("Not 1 flavor detected in filename! Detected {}!".format(len(detected_flavors)))
	return detected_flavors[0]

def get_monopole_systematic_qad(filename):
	filename = str(filename).split("/")[-1]
	syst = filename.split("__")[-2]
	systlist = [ "base", "domeff", "scat", "p1", "angse" ]
	if not any([ sk in syst for sk in systlist ]):
		exit("Did not detect any systematic for this file!")
	return syst

def get_nugen_custom_filename_qad(filename, maindir, num ):
	filename = ("/"+str(filename)).replace("//","/")
	maindir  = ("/"+str(maindir)+"/").replace("//","/")
	filename = filename.replace(maindir,"")

	if num in ["00000","00001","00002"]:
		filename_parts = filename.split("/")
		filename_parts = ["nugen"] + filename_parts
		filename_parts[1] = filename_parts[1].lower()
		filename_parts[3] = filename_parts[3].replace(".","").replace("=","_")
		filename_parts[5] = "{:04}".format(int(filename_parts[5]))
		filename = "__".join(filename_parts)
	if num in ["11070","11297"]:
		filename       = filename.split("/")[-1]
		filename_parts = filename.replace(".i3.",":i3:").replace(".","_").split("_")
		filename_parts = filename_parts[1:]
		filename_parts[4] = filename_parts[4][1:]
		filename = "__".join(filename_parts).replace(":",".")

	return filename

def get_exprm_custom_filename_qad(filenamefirst, filenamelast, num, reproc=False ):
	if not reproc:
		runnumfirst = filenamefirst.split("/Run")[1].split("/")[0]
		runnumlast  = filenamelast.split("/Run")[1].split("/")[0]
		filename    = "exprm__IC86_{}__runs_{}_{}.i3.gz".format(num[-2:],runnumfirst,runnumlast)
	else:
		runnum   = filenamefirst.split("/Run")[1].split("/")[0]
		filename = "reprocessed_BDTscoring_exprm__IC86_{}__run_{}.i3.gz".format(num[-2:],runnum)

	return filename


def get_bdte_vardict(frame):
	import mmact_analysis_bdtutils as bdtut
	varlist = bdtut.bdtvars["bdte"]
	vardict = { varname: frame["ABurgmanVars"][varname] for varname in varlist }
	return vardict



#:--
# GEOMETRIC TRACK AND CENTRALITY
#:--

# Point inside detector

def get_angle_between_vectors_2d(vec1,vec2):
	import numpy as np
	vec1 = np.array(vec1) / np.linalg.norm( vec1 )
	vec2 = np.array(vec2) / np.linalg.norm( vec2 )
	angle = np.arccos(np.dot(vec1,vec2))
	return angle

def get_xyz_from_zenazi(zen,azi):
	x,y,z = np.cos(zen)*np.sin(azi), np.sin(zen)*np.sin(azi), np.cos(azi)
	return x,y,z

def get_angle_between_vectors_3d(vec1,vec2):
	import numpy as np
	vec1 = np.array(vec1) / np.linalg.norm( vec1 )
	vec2 = np.array(vec2) / np.linalg.norm( vec2 )
	angle = np.arccos(np.dot(vec1,vec2))
	return angle

def point_is_inside_detector_horizontal(point):
	import numpy as np
	from icecube import icetray
	from icecube.icetray import I3Units
	point = np.array( point ) # implicitly in I3Units, here and below
	vec_A = np.array([ -632.59, -135.16 ]) - point
	vec_B = np.array([ -387.24,  500.07 ]) - point
	vec_C = np.array([  291.60,  607.46 ]) - point
	vec_D = np.array([  638.00,  181.34 ]) - point
	vec_E = np.array([  400.36, -471.38 ]) - point
	vec_F = np.array([ -278.47, -579.46 ]) - point
	angle_sum = 0
	angle_sum += get_angle_between_vectors_2d( vec_A, vec_B )
	angle_sum += get_angle_between_vectors_2d( vec_B, vec_C )
	angle_sum += get_angle_between_vectors_2d( vec_C, vec_D )
	angle_sum += get_angle_between_vectors_2d( vec_D, vec_E )
	angle_sum += get_angle_between_vectors_2d( vec_E, vec_F )
	angle_sum += get_angle_between_vectors_2d( vec_F, vec_A )
	return ( angle_sum >= (2*np.pi-1e-9) )

def point_is_inside_detector_vertical(point):
	from icecube import icetray
	from icecube.icetray import I3Units
	return ( (point[0]*I3Units.m<=562.5*I3Units.m) and (point[0]*I3Units.m>=-562.5*I3Units.m) )

def point_is_inside_detector(x,y,z):
	is_inside = ( point_is_inside_detector_horizontal([float(x),float(y)]) and point_is_inside_detector_vertical([float(z)]) )
	return is_inside

# Geometric Track

def add_GeometricTrack(frame,trackname):
	import numpy as np
	from icecube import icetray, dataclasses
	from icecube.icetray import I3Units
	from icecube.dataclasses import I3Double, I3Particle, I3MapStringDouble


	if trackname not in frame:
		import warnings
		warnings.warn("No track named {}!".format(trackname))
		return
	geoname = "GeometricTrack_"+trackname
	if geoname in frame:
		del frame[geoname]
	particle = frame[trackname]

	px, py, pz, pt = particle.pos.x, particle.pos.y, particle.pos.z,    particle.time
	dx, dy, dz, dt = particle.dir.x, particle.dir.y, particle.dir.z, 1./particle.speed

	n_points       = 5001
	l_point        = 1.*I3Units.m # the interval with which to check the line
	theline        = np.array( [ [ px+dx*n, py+dy*n, pz+dz*n, pt+dt*n ]                 for n     in np.linspace(-l_point*(n_points-1)/2,l_point*(n_points-1)/2,n_points) ] )
	inside_mask    = np.array( [ point_is_inside_detector( point[0],point[1],point[2] ) for point in theline                                                              ] )
	theline_inside = theline[inside_mask]
	if len(theline_inside):
		length         = np.linalg.norm( np.array(theline_inside[-1][:3]) - np.array(theline_inside[0][:3]) ) + l_point
		time           =                          theline_inside[-1][ 3]  -          theline_inside[0][ 3]    + l_point*dt
	else:
		length         = 0.
		time           = 0.

	frame[geoname] = I3MapStringDouble( { "length": length, "time": time } )

# Centrality

def add_Centrality(frame,trackname):
	import numpy as np
	from icecube import icetray, dataclasses
	from icecube.icetray import I3Units
	from icecube.dataclasses import I3Double, I3Particle, I3MapStringDouble


	if trackname not in frame:
		return
	centname = "Centrality_"+trackname
	if centname in frame:
		del frame[centname]
	particle = frame[trackname]

	px, py, pz, pt = particle.pos.x, particle.pos.y, particle.pos.z,    particle.time
	dx, dy, dz, dt = particle.dir.x, particle.dir.y, particle.dir.z, 1./particle.speed

	d    = np.array([ dx, dy, dz ])
	p    = np.array([ px, py, pz ])
	cent = p-np.dot(p,d)*d

	# perhaps switch this to be an I3Position object
	frame[centname] = I3MapStringDouble( { "x": cent[0], "y": cent[1], "z": cent[2], "length": np.linalg.norm(cent) } )

#def add_Centrality_EHEOpheliaParticleSRT_ImpLF(frame):
#	add_Centrality(frame,"EHEOpheliaParticleSRT_ImpLF")
#def add_Centrality_MCPrimaryParticle(frame):
#	add_Centrality(frame,"MCPrimaryParticle")
#def add_Centrality_BrightestMedianParticle(frame):
#	add_Centrality(frame,"BrightestMedianParticle")
#
#def add_GeometricTrack_EHEOpheliaParticleSRT_ImpLF(frame):
#	add_GeometricTrack(frame,"EHEOpheliaParticleSRT_ImpLF")
#def add_GeometricTrack_MCPrimaryParticle(frame):
#	add_GeometricTrack(frame,"MCPrimaryParticle")
#def add_GeometricTrack_BrightestMedianParticle(frame):
#	add_GeometricTrack(frame,"BrightestMedianParticle")

#:--
# CUSTOM VARIABLES
#:--

def get_fourvector(t,x,c):
	return np.array([t*c]+[xi for xi in x])

def get_fourvector_dotproduct(k1,k2):
	k = np.array(k1)*np.array(k2)
	return k[0]-np.sum(k[1:])

def hit_prod_point(t0,x0,dt,dx,th,xh,indref=1.34):
	# the parameters '*t*' denote times as floats, '*x*' denotes a vector of floats (x,y,z) that gives a position
	# '*0' denotes a point along the particle track
	# 'd*' denotes the travel vector of the particle (dt is |dx|/v_particle)
	# '*h' denotes the hitpoint of the detected photon

	import numpy as np
	import scipy as sp
	import scipy.constants as spco
	from icecube import icetray
	from icecube.icetray import I3Units

	c_water = spco.c*(I3Units.m/I3Units.s)/indref

	# making fourvectors
	k0   = get_fourvector(t0,x0,c_water)
	dk   = get_fourvector(dt,dx,c_water)
	kh   = get_fourvector(th,xh,c_water)
	k0kh = k0-kh

	dkdotdk     = get_fourvector_dotproduct( dk,   dk   )
	dkdotk0kh   = get_fourvector_dotproduct( dk,   k0kh )
	k0khdotk0kh = get_fourvector_dotproduct( k0kh, k0kh )

	a_plus  = ( np.sqrt( dkdotk0kh*dkdotk0kh - dkdotdk*k0khdotk0kh ) + dkdotk0kh ) / dkdotdk
	a_minus = ( np.sqrt( dkdotk0kh*dkdotk0kh - dkdotdk*k0khdotk0kh ) - dkdotk0kh ) / dkdotdk

	if not ( np.isreal(a_plus) and np.isreal(a_minus) ):
		exit("Imaginary values for photon production point!")

	k_prod_plus  = k0 + a_plus  * dk
	k_prod_minus = k0 + a_minus * dk

#	t_plus_physical  = ( ( kh[0] - k_prod_plus[0]  + 1.*I3Units.m) / c_water >= 0 )
#	t_minus_physical = ( ( kh[0] - k_prod_minus[0] + 1.*I3Units.m) / c_water >= 0 )
#	print "num physical:   {}".format(len([t for t in [t_plus_physical,t_minus_physical] if t]))

	return k_prod_plus[0], k_prod_plus[1:], k_prod_minus[0], k_prod_minus[1:]

#	if t_diff_plus<0 and t_diff_minus<0:
#		exit("Oh crap! There is no physical production!")
#	elif t_diff_plus>=0 and t_diff_minus<0:
#		print "Returning    PLUS               solution"
#		return k_prod_plus[0],k_prod_plus[1:]
#	elif t_diff_plus<0 and t_diff_minus>=0:
#		print "Returning              MINUS    solution"
#		return k_prod_minus[0],k_prod_minus[1:]
#	elif all([k_plus==k_minus for k_plus,k_minus in zip(k_prod_plus,k_prod_minus)]):
#		print "Returning         BOTH          solutions"
#		return k_prod_plus[0],k_prod_plus[1:]
#	else:
#		exit("Oh crap! There are two separate physical production points!")

def hit_prod_angle(t0,x0,dt,dx,th,xh,indref=1.34):
#	t_prod, x_prod = hit_prod_point(t0,x0,dt,dx,th,xh,indref=indref)
	t_prod_1, x_prod_1, t_prod_2, x_prod_2 = hit_prod_point(t0,x0,dt,dx,th,xh,indref=indref)
	dp1 = xh-x_prod_1
	dp2 = xh-x_prod_2
	angle_1 = np.arccos(np.dot(dx,dp1)/(np.linalg.norm(dx)*np.linalg.norm(dp1)))
	angle_2 = np.arccos(np.dot(dx,dp2)/(np.linalg.norm(dx)*np.linalg.norm(dp2)))
	rel_t_1 = th - t_prod_1
	rel_t_2 = th - t_prod_2
	return rel_t_1, angle_1, rel_t_2, angle_2

def get_hitprod(frame,particle_name,pulsemap_name):
	from icecube import dataclasses
	from icecube.dataclasses import I3MapStringDouble
	geo            = frame["I3Geometry"]
	particle       = frame[particle_name]
	pulsemap       = I3RecoPulseSeriesMap.from_frame(frame,pulsemap_name)
	p_pos, p_t     = np.array([ particle.pos.x, particle.pos.y, particle.pos.z ]), particle.time
	p_dir, p_speed = np.array([ particle.dir.x, particle.dir.y, particle.dir.z ]), particle.speed
	hitprod_name = "HitProd_{pn}_{pmn}".format(pn=particle_name,pmn=pulsemap_name)
	omgeo          = geo.omgeo
	indexofrefraction = 1.34

	p_tlength = np.linalg.norm(p_dir)/p_speed

	prod_angle_t = np.array([ hit_prod_angle( p_t, p_pos, p_tlength, p_dir, hit.time, np.array([x for x in omgeo[omkey].position]), indexofrefraction ) for omkey, hitlist in list(pulsemap.items()) for hit in hitlist ])
	prod_weights = np.array([ hit.charge for omkey, hitlist in list(pulsemap.items()) for hit in hitlist ])

	prod_angle_t = prod_angle_t.transpose()

	prod_rel_t_all   = np.concatenate((prod_angle_t[0],prod_angle_t[2]))
	prod_angle_all   = np.concatenate((prod_angle_t[1],prod_angle_t[3]))
	prod_weights_all = np.concatenate((prod_weights,prod_weights))

	rel_t_avg =          np.average(  prod_rel_t_all              , weights = prod_weights_all )
	rel_t_std = np.sqrt( np.average( (prod_rel_t_all-rel_t_avg)**2, weights = prod_weights_all ))
	rel_t_rsd = rel_t_std / rel_t_avg
	angle_avg =          np.average(  prod_angle_all              , weights = prod_weights_all )
	angle_std = np.sqrt( np.average( (prod_angle_all-angle_avg)**2, weights = prod_weights_all ))
	angle_rsd = angle_std / angle_avg

	hitprod_dict = { "t_rel_avg": t_rel_avg, "t_rel_std": t_rel_std, "t_rel_rsd": t_rel_rsd,
	                 "theta_avg": angle_avg, "theta_std": angle_std, "theta_rsd": angle_rsd, }
	frame[hitprod_name] = I3MapStringDouble( hitprod_dict )

# ClosestHitsMap

def closest_point_on_line(x0,dx,xh):
	x0, dx, xh = np.array(x0), np.array(dx), np.array(xh)
	x0xh = xh-x0
	xc = x0+(np.dot(x0xh,dx)/np.dot(dx,dx))*dx
	return xc

def add_ClosestHitsMap(frame,input_pm_name,input_track_name,output_pm_name,max_dist_m=100.):
	# input_pm_name is the name of the input pulsemap
	pm = I3RecoPulseSeriesMap.from_frame(frame,input_pm_name)
	track = frame[input_track_name]
	geo            = frame["I3Geometry"]
	omgeo          = geo.omgeo
	max_dist = max_dist_m*I3Units.m

	closeenough = { omkey: np.linalg.norm( np.array([w for w in omgeo[omkey].position]) \
	                                       - closest_point_on_line( np.array([w for w in track.pos]), \
	                                                                np.array([track.dir.x,track.dir.y,track.dir.z]), \
	                                                                np.array([w for w in omgeo[omkey].position]) ) ) \
	                       <= max_dist \
	                for omkey, hitlist in list(pm.items()) }

	# Deleting the output map if already there
	del frame[output_pm_name]
	# Constructing the output map and putting it in the frame:
	frame[output_pm_name] = dataclasses.I3RecoPulseSeriesMapMask( frame, input_pm_name, lambda omkey, index, pulse: int(closeenough[omkey]) )

#def add_ClosestHitsMap_InIcePulsesSRTTW_BrightestMedianParticle(frame):
#	add_ClosestHitsMap(frame,"InIcePulsesSRTTW","BrightestMedianParticle","ClosestHitsIIPBMP",100.)



def add_MillipedeFitStats(frame,millipedename):
	import numpy as np
	from icecube import dataclasses, icetray
	from icecube.dataclasses import I3Particle, I3MapStringDouble, I3Double, I3String
	from icecube.icetray import I3Units
#	shapes, energies, lengths = [], [], []
	shapes, energies          = [], []
	xs,     ys,       zs      = [], [], []

	statsname = millipedename+"_FitStats"
	if statsname in frame:
		del frame[statsname]


	shapes   = [   str(p.shape).split(".")[-1] for p in frame[millipedename] ]
	energies = [ float(p.energy)               for p in frame[millipedename] ]
	xs       = [ float(p.pos.x)                for p in frame[millipedename] ]
	ys       = [ float(p.pos.y)                for p in frame[millipedename] ]
	zs       = [ float(p.pos.z)                for p in frame[millipedename] ]


	is_any_cascade = np.array( [ ("cascade" in sh.lower())       for sh    in shapes        ] )
	is_any_track   = np.array( [ ("track"   in sh.lower())       for sh    in shapes        ] )
	is_inside      = np.array( [ point_is_inside_detector(x,y,z) for x,y,z in zip(xs,ys,zs) ] )

	section_inside_energies = np.array(energies)[np.logical_and(is_any_cascade,is_inside)] + np.array(energies)[np.logical_and(is_any_track,is_inside)]


	zeroenergy = 1e-16*I3Units.GeV

	stats_dict = { "avg_e": np.average(section_inside_energies),
	               "std_e": np.std(section_inside_energies),
	               "rsd_e": np.std(section_inside_energies)/max(np.average(section_inside_energies),zeroenergy),
	             }

	frame[statsname] = I3MapStringDouble( stats_dict )

#def add_MillipedeBrightestMedianOutputFitStats(frame):
#	add_MillipedeFitStats(frame,"MillipedeBrightestMedianOutput")





#:--
# ONEWEIGHT STUFF
#:--

def in_range(val,ran):
	return ( val>=ran[0] and val<ran[1] )

def get_astronu_flux_params(fitname,phigamma,centsigma):
	fluxdict = {}
	# Diffuse Muon Neutrino Fit, ICRC 2017
	# https://arxiv.org/pdf/1710.01191.pdf, pp 30-37 (fit on p 33), PoS(ICRC2017)1005
	# per-flavor, sum of nu-nubar
	fluxdict["numudif2017"] = { "phi":   { "central": 1.01, "plussigma": 1.27, "minussigma": 0.78 },
	                            "gamma": { "central": 2.19, "plussigma": 2.09, "minussigma": 2.29 }, }
	# Diffuse Muon Neutrino Fit, ICRC 2019
	# https://pos.sissa.it/cgi-bin/reader/contribution.cgi?id=PoS(ICRC2019)1017
	# per-flavor, sum of nu-nubar
	fluxdict["numudif2019"] = { "phi":   { "central": 1.44, "plussigma": 1.69, "minussigma": 1.20 },
	                            "gamma": { "central": 2.28, "plussigma": 2.20, "minussigma": 2.37 }, }
	# High Energy Starting Events Fit, ICRC 2019
	# https://pos.sissa.it/cgi-bin/reader/contribution.cgi?id=PoS(ICRC2019)1004
	# per-flavor, sum of nu-nubar (given as sum-of-flavors in paper, here divided by 3)
	fluxdict["hese2019"]    = { "phi":   { "central": 2.15, "plussigma": 2.64, "minussigma": 2.00 },
	                            "gamma": { "central": 2.89, "plussigma": 2.70, "minussigma": 3.09 }, }
	return fluxdict[fitname][phigamma][centsigma]

def get_astronu_flux(fitname,energy,centsigma):
	phi   = get_astronu_flux_params(fitname,"phi",centsigma)
	gamma = get_astronu_flux_params(fitname,"gamma",centsigma)
	Phi   = phi * 1e-18 * ( energy / (100.*I3Units.TeV) ) ** (-1.*gamma)
	return Phi

def get_nevgen_dict():
	nevgen_dict = { "mpsim": { "00002": { "baseline":             { "monopole":  400.*1000., },    # ABurgman
	                                      "domeff_plus":          { "monopole":  100.*1000., },
	                                      "domeff_minus":         { "monopole":   99.*1000., },
	                                      "scat_plus_abs_plus":   { "monopole":   97.*1000., },
	                                      "scat_plus_abs_minus":  { "monopole":   97.*1000., },
	                                      "scat_minus_abs_plus":  { "monopole":  100.*1000., },
	                                      "scat_minus_abs_minus": { "monopole":  100.*1000., },
	                                      "angsens_set05":        { "monopole":  100.*1000., },
	                                      "angsens_set09":        { "monopole":  100.*1000., },
	                                      "angsens_set10":        { "monopole":  100.*1000., },
	                                      "angsens_set14":        { "monopole":  100.*1000., },
	                                      "p1_0.20_p2_0":         { "monopole":  100.*1000., },
	                                      "p1_0.25_p2_-3":        { "monopole":  100.*1000., },
	                                      "p1_0.25_p2_-1":        { "monopole":  100.*1000., },
	                                      "p1_0.25_p2_0":         { "monopole":  100.*1000., },
	                                      "p1_0.25_p2_+1":        { "monopole":  100.*1000., },
	                                      "p1_0.30_p2_-3":        { "monopole":  100.*1000., },
	                                      "p1_0.30_p2_-1":        { "monopole":  100.*1000., },
	                                      "p1_0.30_p2_0":         { "monopole":  100.*1000., },
	                                      "p1_0.30_p2_+1":        { "monopole":  100.*1000., },
	                                      "p1_0.35_p2_0":         { "monopole":  100.*1000., }, }, },
	                "nugen": { "00001": { "baseline": { "nue": 12000.*1.0e4, "numu": 12000.*2.0e4, "nutau": 12000.*1.0e4, }, },      # Nancy
                               "00002": { "baseline": { "nue":  4948.*10.,   "numu":  4984.*20.,   "nutau":  4976.*10.,   }, },
                               "11070": { "baseline": {                      "numu":  5000.*400.,                         }, },      # Central Production
                               "11297": { "baseline": {                                            "nutau":  5000.*400.,  }, }, }, }
	return nevgen_dict

def get_energyrange_dict():
	energyrange_dict = { "00001": [  5.*I3Units.TeV,   10.*I3Units.PeV, ],
	                     "00002": [  1.*I3Units.PeV,  100.*I3Units.PeV, ],
	                     "11070": [ 10.*I3Units.PeV, 1000.*I3Units.PeV, ],
	                     "11297": [ 10.*I3Units.PeV, 1000.*I3Units.PeV, ], }
	return energyrange_dict

def overlap_weight(fitname,energy,num,flav,centsigma,overlapregion):
	import numpy as np
	from icecube import icetray
	from icecube.icetray import I3Units
	N            = get_nevgen_dict()
	energy_range = get_energyrange_dict()
	regionnum    = { "nancy_medium": { "nue": "00001", "numu": "00001", "nutau": "00001", },
	                 "nancy_high":   { "nue": "00002", "numu": "00002", "nutau": "00002", },
	                 "iceprod_high": { "nue": "",      "numu": "11070", "nutau": "11297", }, }
	numlist      = [ regionnum[region][flav] for region in overlapregion ]

	if "iceprod_high" in overlapregion and "nue" in flav:
		overlap_weight = 1.
		return overlap_weight
	else:
		this_num = num
		other_num = [n for n in numlist if n!=this_num][0]
		phi   = get_astronu_flux_params(fitname,"phi",centsigma)
		gamma = get_astronu_flux_params(fitname,"gamma",centsigma)
		this_I  = phi * ( 100.*I3Units.TeV )**( gamma ) * ( 1. / (1.-gamma) ) * (  energy_range[this_num][1]**(1.-gamma) -  energy_range[this_num][0]**(1.-gamma) )
		other_I = phi * ( 100.*I3Units.TeV )**( gamma ) * ( 1. / (1.-gamma) ) * ( energy_range[other_num][1]**(1.-gamma) - energy_range[other_num][0]**(1.-gamma) )
		overlap_weight = ( N["nugen"][this_num]["baseline"][flav] / this_I ) / ( ( N["nugen"][this_num]["baseline"][flav] / this_I ) + ( N["nugen"][other_num]["baseline"][flav] / other_I ) )
		return overlap_weight if all( [ in_range(energy,energy_range[num]) for num in numlist ] ) else 1.

#if gen=="nugen":
#	det = {}
#	with open(configs["data_sample_details"]["montecarlo_data"]["nugen"]["00000"]) as det_00000_file:
#		det["00000"] = json.load(det_00000_file)
#	with open(configs["data_sample_details"]["montecarlo_data"]["nugen"]["00001"]) as det_00001_file:
#		det["00001"] = json.load(det_00001_file)
#	with open(configs["data_sample_details"]["montecarlo_data"]["nugen"]["00002"]) as det_00002_file:
#		det["00002"] = json.load(det_00002_file)

# THIS LIVETIME COMES FROM EHE ACCOUNTING, AND ONLY HAS IC86-1 THROUGH -6
def get_t_live_IC86():
	t = { "t_live": { "IC40":    373.08, "IC59":    342.76, "IC79":     312.52,
                      "IC86-I":  341.77, "IC86-II": 329.65, "IC86-III": 360.34,
                      "IC86-IV": 365.91, "IC86-V":  359.30, "IC86-VI":  357.18, },
          "t_burn": { "IC40":     35.32, "IC59":     33.04, "IC79":     33.23,
                      "IC86-I":   33.56, "IC86-II":  34.70, "IC86-III": 33.98,
                      "IC86-IV":  34.71, "IC86-V":   37.17, "IC86-VI":   0.0,   }, }
	return sum([ t["t_live"][icxx]-t["t_burn"][icxx] for icxx in list(t["t_live"].keys()) if "IC86" in icxx ]) * I3Units.day

# THIS IS THE CORRECT EXPERIMENTAL LIVETIME
def t_live_IC86_exprm(startyr,endyr,whichsample="phys"):
	t_live_IC86 = { 2011: 26710631.19,
	                2012: 25483648.26,
	                2013: 27784683.01,
	                2014: 28079817.19,
	                2015: 28316611.70,
	                2016: 30827655.64,
	                2017: 35504074.30,
	                2018: 31865991.56, }
	t_burn_IC86 = { 2011:  2721082.25,
	                2012:  2804133.57,
	                2013:  2948421.03,
	                2014:  3027409.38,
	                2015:  3240420.18,
	                2016:        0.00,
	                2017:        0.00,
	                2018:        0.00, }
	if whichsample.lower()=="phys":
		# Physics livetime in seconds
		return sum([ t_live_IC86[2010+yr] for yr in np.linspace(startyr,endyr,endyr-startyr+1) ]) * I3Units.second
	elif whichsample.lower()=="burn":
		# Burnsample livetime in seconds
		return sum([ t_burn_IC86[2010+yr] for yr in np.linspace(startyr,endyr,endyr-startyr+1) ]) * I3Units.second
	else:
		# Total livetime in seconds
		return sum([ t_live_IC86[2010+yr]+t_burn_IC86[2010+yr] for yr in np.linspace(startyr,endyr,endyr-startyr+1) ]) * I3Units.second

def get_six_eight_year_livetime_ratio():
	return t_live_IC86_exprm(1,8)/get_t_live_IC86()

# THE RATIO BETWEEN PHYSICS LIVETIME IC86-1-6 AND IC86-1-8 IS 1.4 (1.399445670382436) (considering 6 yr from get_t_live_IC86(), and 8 yr from t_live_IC86_exprm())

def calc_monopole_oneweight(gen,num,syst,flav):

	misc_params = { "beta_spectrum": [     0.750, 0.995,     ],
					"disk_distance":    1000.0      *     I3Units.m,
					"disk_radius":      1100.0      *     I3Units.m,
					"monopole_mass":       1.0e11   *     I3Units.GeV,
					"dist_to_cent_max": 2000.0      *     I3Units.m,
					"step_length_max":    10.0      *     I3Units.m,
					"L5_decrease_factor":  0.894,
					"Phi_0":               3.46e-18 * (1/(I3Units.cm2*I3Units.s*I3Units.steradian)),   # Flux assumption - average of Jonas Posselt's limit at beta = 0.8, 0.9, 0.995, unit: cm^-2 s^-1 sr^-1
					"Omega":               4.*np.pi *     I3Units.steradian,                         } # Solid angle of analysis

	A_gen = misc_params["disk_radius"]*misc_params["disk_radius"]*np.pi

	# Regarding the width of the generated spectum
	# ----
	# # The spectrum width, W_spectrum, represents the width of the covered beta spectrum divided by the full spectrum, i.e.
	# #     W_spectrum = ( 0.995 - 0.750 ) / 1.0
	# spectrum_width = ( mpdet["Event_Info"]["spectrum"]["end"] - mpdet["Event_Info"]["spectrum"]["start"] ) / 1.
	# OneWeightReduced = Omega * t_live * Phi_0 * spectrum_width * A_gen / mpsim_00001__n_gen
	#
	# The spectrum_width factor should onle be used if I wanted to generalize my
	# limit to a beta range where I didn't generate events (e.g. the full beta
	# range) as it would then serve the purpose of artificially "pretending" to
	# have generated events over the full beta range, when this is not the case.
	# Otherwise, the spectrum width is included automatically, as n_gen is
	# changed accordingly when the beta range is canged.
	#

	OneWeightReduced = misc_params["Omega"] * get_t_live_IC86() * misc_params["Phi_0"] * A_gen / get_nevgen_dict()[gen][num][syst][flav]

	return OneWeightReduced



def add_OneWeightDict(frame,gen,num,flav,syst):
	from icecube import dataclasses
	from icecube.dataclasses import I3MapStringDouble

	if gen=="mpsim":
		t_live_s = get_t_live_IC86() / I3Units.s
		nev_gen  = get_nevgen_dict()[gen][num][syst][flav]
		ow_red_monopole = calc_monopole_oneweight(gen,num,syst,flav)

		owdict = {  "energy":                                                         -1.,
					"oneweight":                                                       1.,
					"nev_gen":                                                        nev_gen,
					"t_live":                                                         t_live_s * I3Units.s,
					"flux_numudif2017_central":                                       -1.,
					"flux_numudif2017_plussigma":                                     -1.,
					"flux_numudif2017_minussigma":                                    -1.,
					"oneweight_reduced_numudif2017_central":                          ow_red_monopole,
					"oneweight_reduced_numudif2017_plussigma":                        ow_red_monopole,
					"oneweight_reduced_numudif2017_minussigma":                       ow_red_monopole,
					"overlap_weight_numudif2017_central__nancy_medium__nancy_high":    1.,
					"overlap_weight_numudif2017_plussigma__nancy_medium__nancy_high":  1.,
					"overlap_weight_numudif2017_minussigma__nancy_medium__nancy_high": 1.,
					"overlap_weight_numudif2017_central__nancy_high__iceprod_high":    1.,
					"overlap_weight_numudif2017_plussigma__nancy_high__iceprod_high":  1.,
					"overlap_weight_numudif2017_minussigma__nancy_high__iceprod_high": 1.,
					"flux_numudif2019_central":                                       -1.,
					"flux_numudif2019_plussigma":                                     -1.,
					"flux_numudif2019_minussigma":                                    -1.,
					"oneweight_reduced_numudif2019_central":                          ow_red_monopole,
					"oneweight_reduced_numudif2019_plussigma":                        ow_red_monopole,
					"oneweight_reduced_numudif2019_minussigma":                       ow_red_monopole,
					"overlap_weight_numudif2019_central__nancy_medium__nancy_high":    1.,
					"overlap_weight_numudif2019_plussigma__nancy_medium__nancy_high":  1.,
					"overlap_weight_numudif2019_minussigma__nancy_medium__nancy_high": 1.,
					"overlap_weight_numudif2019_central__nancy_high__iceprod_high":    1.,
					"overlap_weight_numudif2019_plussigma__nancy_high__iceprod_high":  1.,
					"overlap_weight_numudif2019_minussigma__nancy_high__iceprod_high": 1.,
					"flux_hese2019_central":                                          -1.,
					"flux_hese2019_plussigma":                                        -1.,
					"flux_hese2019_minussigma":                                       -1.,
					"oneweight_reduced_hese2019_central":                             ow_red_monopole,
					"oneweight_reduced_hese2019_plussigma":                           ow_red_monopole,
					"oneweight_reduced_hese2019_minussigma":                          ow_red_monopole,
					"overlap_weight_hese2019_central__nancy_medium__nancy_high":       1.,
					"overlap_weight_hese2019_plussigma__nancy_medium__nancy_high":     1.,
					"overlap_weight_hese2019_minussigma__nancy_medium__nancy_high":    1.,
					"overlap_weight_hese2019_central__nancy_high__iceprod_high":       1.,
					"overlap_weight_hese2019_plussigma__nancy_high__iceprod_high":     1.,
					"overlap_weight_hese2019_minussigma__nancy_high__iceprod_high":    1., }

	elif gen=="nugen":
		t_live_s = get_t_live_IC86() / I3Units.s
		nev_gen  = get_nevgen_dict()[gen][num][syst][flav]
		energy   = frame["MCPrimaryParticle"].energy
		ow       = frame["I3MCWeightDict"]["OneWeight"]

		owdict = {  "energy":                                                          energy,
					"oneweight":                                                       ow,
					"nev_gen":                                                         nev_gen,
					"t_live":                                                          t_live_s * I3Units.s,
					"flux_numudif2017_central":                                      get_astronu_flux( "numudif2017", energy,            "central"   )                                 ,
					"flux_numudif2017_plussigma":                                    get_astronu_flux( "numudif2017", energy,            "plussigma" )                                 ,
					"flux_numudif2017_minussigma":                                   get_astronu_flux( "numudif2017", energy,            "minussigma")                                 ,
					"oneweight_reduced_numudif2017_central":                         get_astronu_flux( "numudif2017", energy,            "central"   ) * t_live_s * ow / nev_gen       ,
					"oneweight_reduced_numudif2017_plussigma":                       get_astronu_flux( "numudif2017", energy,            "plussigma" ) * t_live_s * ow / nev_gen       ,
					"oneweight_reduced_numudif2017_minussigma":                      get_astronu_flux( "numudif2017", energy,            "minussigma") * t_live_s * ow / nev_gen       ,
					"overlap_weight_numudif2017_central__nancy_medium__nancy_high":    overlap_weight( "numudif2017", energy, num, flav, "central"   , ["nancy_medium","nancy_high"] ) ,
					"overlap_weight_numudif2017_plussigma__nancy_medium__nancy_high":  overlap_weight( "numudif2017", energy, num, flav, "plussigma" , ["nancy_medium","nancy_high"] ) ,
					"overlap_weight_numudif2017_minussigma__nancy_medium__nancy_high": overlap_weight( "numudif2017", energy, num, flav, "minussigma", ["nancy_medium","nancy_high"] ) ,
					"overlap_weight_numudif2017_central__nancy_high__iceprod_high":    overlap_weight( "numudif2017", energy, num, flav, "central"   , ["nancy_high","iceprod_high"] ) ,
					"overlap_weight_numudif2017_plussigma__nancy_high__iceprod_high":  overlap_weight( "numudif2017", energy, num, flav, "plussigma" , ["nancy_high","iceprod_high"] ) ,
					"overlap_weight_numudif2017_minussigma__nancy_high__iceprod_high": overlap_weight( "numudif2017", energy, num, flav, "minussigma", ["nancy_high","iceprod_high"] ) ,
					"flux_numudif2019_central":                                      get_astronu_flux( "numudif2019", energy,            "central"   )                                 ,
					"flux_numudif2019_plussigma":                                    get_astronu_flux( "numudif2019", energy,            "plussigma" )                                 ,
					"flux_numudif2019_minussigma":                                   get_astronu_flux( "numudif2019", energy,            "minussigma")                                 ,
					"oneweight_reduced_numudif2019_central":                         get_astronu_flux( "numudif2019", energy,            "central"   ) * t_live_s * ow / nev_gen       ,
					"oneweight_reduced_numudif2019_plussigma":                       get_astronu_flux( "numudif2019", energy,            "plussigma" ) * t_live_s * ow / nev_gen       ,
					"oneweight_reduced_numudif2019_minussigma":                      get_astronu_flux( "numudif2019", energy,            "minussigma") * t_live_s * ow / nev_gen       ,
					"overlap_weight_numudif2019_central__nancy_medium__nancy_high":    overlap_weight( "numudif2019", energy, num, flav, "central"   , ["nancy_medium","nancy_high"] ) ,
					"overlap_weight_numudif2019_plussigma__nancy_medium__nancy_high":  overlap_weight( "numudif2019", energy, num, flav, "plussigma" , ["nancy_medium","nancy_high"] ) ,
					"overlap_weight_numudif2019_minussigma__nancy_medium__nancy_high": overlap_weight( "numudif2019", energy, num, flav, "minussigma", ["nancy_medium","nancy_high"] ) ,
					"overlap_weight_numudif2019_central__nancy_high__iceprod_high":    overlap_weight( "numudif2019", energy, num, flav, "central"   , ["nancy_high","iceprod_high"] ) ,
					"overlap_weight_numudif2019_plussigma__nancy_high__iceprod_high":  overlap_weight( "numudif2019", energy, num, flav, "plussigma" , ["nancy_high","iceprod_high"] ) ,
					"overlap_weight_numudif2019_minussigma__nancy_high__iceprod_high": overlap_weight( "numudif2019", energy, num, flav, "minussigma", ["nancy_high","iceprod_high"] ) ,
					"flux_hese2019_central":                                         get_astronu_flux( "hese2019",    energy,            "central"   )                                 ,
					"flux_hese2019_plussigma":                                       get_astronu_flux( "hese2019",    energy,            "plussigma" )                                 ,
					"flux_hese2019_minussigma":                                      get_astronu_flux( "hese2019",    energy,            "minussigma")                                 ,
					"oneweight_reduced_hese2019_central":                            get_astronu_flux( "hese2019",    energy,            "central"   ) * t_live_s * ow / nev_gen       ,
					"oneweight_reduced_hese2019_plussigma":                          get_astronu_flux( "hese2019",    energy,            "plussigma" ) * t_live_s * ow / nev_gen       ,
					"oneweight_reduced_hese2019_minussigma":                         get_astronu_flux( "hese2019",    energy,            "minussigma") * t_live_s * ow / nev_gen       ,
					"overlap_weight_hese2019_central__nancy_medium__nancy_high":       overlap_weight( "hese2019",    energy, num, flav, "central"   , ["nancy_medium","nancy_high"] ) ,
					"overlap_weight_hese2019_plussigma__nancy_medium__nancy_high":     overlap_weight( "hese2019",    energy, num, flav, "plussigma" , ["nancy_medium","nancy_high"] ) ,
					"overlap_weight_hese2019_minussigma__nancy_medium__nancy_high":    overlap_weight( "hese2019",    energy, num, flav, "minussigma", ["nancy_medium","nancy_high"] ) ,
					"overlap_weight_hese2019_central__nancy_high__iceprod_high":       overlap_weight( "hese2019",    energy, num, flav, "central"   , ["nancy_high","iceprod_high"] ) ,
					"overlap_weight_hese2019_plussigma__nancy_high__iceprod_high":     overlap_weight( "hese2019",    energy, num, flav, "plussigma" , ["nancy_high","iceprod_high"] ) ,
					"overlap_weight_hese2019_minussigma__nancy_high__iceprod_high":    overlap_weight( "hese2019",    energy, num, flav, "minussigma", ["nancy_high","iceprod_high"] ) , }

	elif gen=="exprm":
		owdict = { "oneweight": 1., }
#		owdict = {  "energy":                                                         -1.,
#					"oneweight":                                                       1.,
#					"nev_gen":                                                        -1.,
#					"t_live":                                                         -1.,
#					"flux_numudif2017_central":                                       -1.,
#					"flux_numudif2017_plussigma":                                     -1.,
#					"flux_numudif2017_minussigma":                                    -1.,
#					"oneweight_reduced_numudif2017_central":                           1.,
#					"oneweight_reduced_numudif2017_plussigma":                         1.,
#					"oneweight_reduced_numudif2017_minussigma":                        1.,
#					"overlap_weight_numudif2017_central__nancy_medium__nancy_high":    1.,
#					"overlap_weight_numudif2017_plussigma__nancy_medium__nancy_high":  1.,
#					"overlap_weight_numudif2017_minussigma__nancy_medium__nancy_high": 1.,
#					"overlap_weight_numudif2017_central__nancy_high__iceprod_high":    1.,
#					"overlap_weight_numudif2017_plussigma__nancy_high__iceprod_high":  1.,
#					"overlap_weight_numudif2017_minussigma__nancy_high__iceprod_high": 1.,
#					"flux_numudif2019_central":                                       -1.,
#					"flux_numudif2019_plussigma":                                     -1.,
#					"flux_numudif2019_minussigma":                                    -1.,
#					"oneweight_reduced_numudif2019_central":                           1.,
#					"oneweight_reduced_numudif2019_plussigma":                         1.,
#					"oneweight_reduced_numudif2019_minussigma":                        1.,
#					"overlap_weight_numudif2019_central__nancy_medium__nancy_high":    1.,
#					"overlap_weight_numudif2019_plussigma__nancy_medium__nancy_high":  1.,
#					"overlap_weight_numudif2019_minussigma__nancy_medium__nancy_high": 1.,
#					"overlap_weight_numudif2019_central__nancy_high__iceprod_high":    1.,
#					"overlap_weight_numudif2019_plussigma__nancy_high__iceprod_high":  1.,
#					"overlap_weight_numudif2019_minussigma__nancy_high__iceprod_high": 1.,
#					"flux_hese2019_central":                                          -1.,
#					"flux_hese2019_plussigma":                                        -1.,
#					"flux_hese2019_minussigma":                                       -1.,
#					"oneweight_reduced_hese2019_central":                              1.,
#					"oneweight_reduced_hese2019_plussigma":                            1.,
#					"oneweight_reduced_hese2019_minussigma":                           1.,
#					"overlap_weight_hese2019_central__nancy_medium__nancy_high":       1.,
#					"overlap_weight_hese2019_plussigma__nancy_medium__nancy_high":     1.,
#					"overlap_weight_hese2019_minussigma__nancy_medium__nancy_high":    1.,
#					"overlap_weight_hese2019_central__nancy_high__iceprod_high":       1.,
#					"overlap_weight_hese2019_plussigma__nancy_high__iceprod_high":     1.,
#					"overlap_weight_hese2019_minussigma__nancy_high__iceprod_high":    1., }
	frame["OneWeightDict"] = I3MapStringDouble( owdict )





#:--
# MISC FRAME OBJECTS
#:--

def add_CountingWeightFactor(frame):
	if "CountingWeightFactor" not in frame:
		frame["CountingWeightFactor"] = I3Double(1.)

def add_ABurgmanGenNum(frame,gen,num):
	from icecube import dataclasses
	from icecube.dataclasses import I3MapStringDouble
	if frame.Has("ABurgmanGen"):
		del frame["ABurgmanGen"]
	if frame.Has("ABurgmanNum"):
		del frame["ABurgmanNum"]
	gens = [ "mpsim", "nugen", "exprm" ]
	nums = [ "00000", "00001", "00002", "11070", "11297" ] + [ "86{}{:02}".format(str(physburn),int(yr)) for yr in np.linspace(1,10,10) for physburn in [0,9] ]
	frame["ABurgmanGen"] = I3MapStringDouble( { g: int(g==gen) for g in gens } )
	frame["ABurgmanNum"] = I3MapStringDouble( { n: int(n==num) for n in nums } )

def read_ABurgmanGenNum(frame):
	gen, num = "", ""
	gen = "__".join([g for g,k in list(frame["ABurgmanGen"].items()) if k])
	num = "__".join([n for n,k in list(frame["ABurgmanNum"].items()) if k])
	if "__" in gen:
		exit("More than one gen given")
	if "__" in num:
		exit("More than one num given")
	if not gen:
		exit("No gen given")
	if not num:
		exit("No num given")
	return { "gen": gen, "num": num }

def add_pulsemapWODC(frame,input_pm_name,output_pm_name):
	# input_pm_name is the name of the input pulsemap
	pm = I3RecoPulseSeriesMap.from_frame(frame,input_pm_name)
	frame[output_pm_name] = dataclasses.I3RecoPulseSeriesMapMask( frame, input_pm_name, lambda omkey, index, pulse: omkey[0] not in [79,80,81,82,83,84,85,86] )
#def add_SRTInIcePulsesWODC(frame):
#	add_pulsemapWODC(frame,"SRTInIcePulses","SRTInIcePulsesWODC")

def add_BrightestMedianMap(frame,input_pm_name,output_pm_name):
	# input_pm_name is the name of the input pulsemap
	pm = I3RecoPulseSeriesMap.from_frame(frame,input_pm_name)

	# Extracting a sorted list of the recorded charge of each DOM in the hit map
	alltotcharges = np.sort([ sum([hit.charge for hit in hitlist]) for hitlist in list(pm.values()) ])[::-1]

	# Recording the dimmest charge among the ten percent brightest DOMs
	dimmestbrightcharge = alltotcharges[int(0.1*len(alltotcharges))+1]

	# The DOMs that are bright enough, i.e. have a summed charge higher than the dimmest allowed charge
	brightenough = { omkey: sum([hit.charge for hit in hitlist])>dimmestbrightcharge for omkey, hitlist in list(pm.items()) }

	# The index of the median hit per hit DOM
	indexmedian = { omkey: int(0.5*len(hitlist)) for omkey, hitlist in list(pm.items()) }

	# Deleting the output map if already there
	del frame[output_pm_name]
	# Constructing the output map and putting it in the frame:
	#   - The DOM must be among the 10 % brightest in the input map
	#   - Only one pulse is kept for each bright enough DOM: the hit at median position
	frame[output_pm_name] = dataclasses.I3RecoPulseSeriesMapMask( frame, input_pm_name, lambda omkey, index, pulse: int(brightenough[omkey]) and index==indexmedian[omkey] )
#def add_BrightestMedianMap_InIcePulsesSRTTW(frame):
#	add_BrightestMedianMap(frame,"InIcePulsesSRTTW","BrightestMedianInIcePulsesSRTTW")

def delete_all_CV(frame):
	for framekey in list(frame.keys()):
		if "CV_" in framekey:
			del frame[framekey]

#:--
# ABURGMAN VARIABLES
#:--


def export_aburgman_variables(frame,lev,gen):
	if gen=="exprm" and lev=="trigger":
		return
	import numpy as np
	import scipy as sp
	import scipy.constants as spco
	from icecube import dataclasses
	from icecube.dataclasses import I3MapStringDouble

	if "ABurgmanVars" in frame:
		del frame["ABurgmanVars"]
	if "ABurgmanKeys" in frame:
		del frame["ABurgmanKeys"]

	vars_all = {}

	# MCPrimaryParticle
	vars_slop = {}
	if lev in ["trigger","ehefilter","L2","L3","L4","preBDT","L5","L6"]:
		vars_slop['SLOPTuples_CosAlpha_Launches']=frame["SLOPTuples_CosAlpha_Launches"]
	vars_all.update(vars_slop)



	vars_primary = {}
	if lev in ["trigger","ehefilter","L2","L3","L4","preBDT","L5","L6"] and gen!="exprm":
		vars_primary["mccoszen"]      =   np.cos( frame["MCPrimaryParticle"].dir.zenith )                               #if gen != "exprm" else  2. # Unphysical experimental value 
		vars_primary["mcazi"]         =           frame["MCPrimaryParticle"].dir.azimuth                                #if gen != "exprm" else -1. # Unphysical experimental value 
		vars_primary["mcbeta"]        =           frame["MCPrimaryParticle"].speed / ( spco.c * (I3Units.m/I3Units.s) ) #if gen != "exprm" else -1. # Unphysical experimental value 
		vars_primary["mclog10energy"] = np.log10( frame["MCPrimaryParticle"].energy / I3Units.GeV )                     #if gen != "exprm" else -1. # Unphysical experimental value 
		vars_primary["mccentrality"]  =           frame["Centrality_MCPrimaryParticle"]["length"]                       #if gen != "exprm" else -1. # Unphysical experimental value 
		vars_primary["mcgeomlength"]  =           frame["GeometricTrack_MCPrimaryParticle"]["length"]                   #if gen != "exprm" else -1. # Unphysical experimental value 
		vars_primary["mcgeomtime"]    =           frame["GeometricTrack_MCPrimaryParticle"]["time"]                     #if gen != "exprm" else -1. # Unphysical experimental value 
	vars_all.update(vars_primary)

	# Portia
	vars_portia = {}
	if lev in ["ehefilter","L2","L3","L4","preBDT","L5","L6"]:
		vars_portia["ptlog10npe"] = np.log10( max( 1e-20, frame["EHEPortiaEventSummarySRT"].GetTotalBestNPE() ) )
		vars_portia["ptnch"]      =                       frame["EHEPortiaEventSummarySRT"].GetTotalNch()
		vars_portia["ptrhope"]    =                       frame["EHEPortiaEventSummarySRT"].GetTotalBestNPE() / max( 1e-20, frame["EHEPortiaEventSummarySRT"].GetTotalNch() )
	vars_all.update(vars_portia)

	# Ophelia LineFit
	vars_ophelia = {}
	if lev in ["ehefilter","L2","L3","L4","preBDT","L5","L6"]:
		vars_ophelia["opcoszen"]     = np.cos( frame["EHEOpheliaParticleSRT_ImpLF"].dir.zenith )
		vars_ophelia["opazi"]        =         frame["EHEOpheliaParticleSRT_ImpLF"].dir.azimuth
		vars_ophelia["opbeta"]       =         frame["EHEOpheliaParticleSRT_ImpLF"].speed / ( spco.c * (I3Units.m/I3Units.s) ) 
		vars_ophelia["opfitquality"] =         frame["EHEOpheliaSRT_ImpLF"].fit_quality
	#	vars_ophelia["opcentrality"] =         frame["Centrality_EHEOpheliaParticleSRT_ImpLF"]["length"]
	#	vars_ophelia["opgeomlength"] =         frame["GeometricTrack_EHEOpheliaParticleSRT_ImpLF"]["length"]
	#	vars_ophelia["opgeomtime"]   =         frame["GeometricTrack_EHEOpheliaParticleSRT_ImpLF"]["time"]
	vars_all.update(vars_ophelia)

	# Ophelia LineFit
	vars_bdtsep = {}
	if lev in ["ehefilter","L2","L3","L4","preBDT","L5","L6"] and gen!="exprm":
		vars_bdtsep["bdtseparator"] = frame["BDTSeparator"].value
		vars_bdtsep["bdtistrain"]   = frame["BDTTrainTest"]["train"]
		vars_bdtsep["bdtistest"]    = frame["BDTTrainTest"]["test"]
	vars_all.update(vars_bdtsep)

	# BrightestMedian LineFit
	vars_brightestmedian = {}
	if lev in ["preBDT","L5","L6"]:
		vars_brightestmedian["bmcoszen"]     = np.cos( frame["BrightestMedianParticle"].dir.zenith )
		vars_brightestmedian["bmazi"]        =         frame["BrightestMedianParticle"].dir.azimuth
		vars_brightestmedian["bmbeta"]       =         frame["BrightestMedianParticle"].speed / ( spco.c * (I3Units.m/I3Units.s) ) 
		vars_brightestmedian["bmcentrality"] =         frame["Centrality_BrightestMedianParticle"]["length"]
		vars_brightestmedian["bmgeomlength"] =         frame["GeometricTrack_BrightestMedianParticle"]["length"]
		vars_brightestmedian["bmgeomtime"]   =         frame["GeometricTrack_BrightestMedianParticle"]["time"]
	vars_all.update(vars_brightestmedian)

	cvparticlename      = "BrightestMedianParticle"
	millipededict       = "Millipede_BrightestMedian_FitStats"
	cherenkovoffsetdict = "CherenkovOffset_BrightestMedianParticle_ClosestHitsIIPBMP"

	# CommonVariables
	vars_common = {}
	if lev in ["preBDT","L5","L6"]:
####		vars_common["cvdihdlength"]      = frame["CV_DirectHitsValues_{}D".format(cvparticlename)].dir_track_length                      if not np.isnan(frame["CV_DirectHitsValues_{}D".format(cvparticlename)].dir_track_length)                      else 0.0
####		vars_common["cvdihdsmoothness"]  = frame["CV_DirectHitsValues_{}D".format(cvparticlename)].dir_track_hit_distribution_smoothness if not np.isnan(frame["CV_DirectHitsValues_{}D".format(cvparticlename)].dir_track_hit_distribution_smoothness) else 1.0e100
####		vars_common["cvdihdqdirect"]     = frame["CV_DirectHitsValues_{}D".format(cvparticlename)].q_dir_pulses                          if not np.isnan(frame["CV_DirectHitsValues_{}D".format(cvparticlename)].q_dir_pulses)                          else 0.0
####		vars_common["cvdihdqearly"]      = frame["CV_DirectHitsValues_{}D".format(cvparticlename)].q_early_pulses                        if not np.isnan(frame["CV_DirectHitsValues_{}D".format(cvparticlename)].q_early_pulses)                        else 0.0
####		vars_common["cvdihdqlate"]       = frame["CV_DirectHitsValues_{}D".format(cvparticlename)].q_late_pulses                         if not np.isnan(frame["CV_DirectHitsValues_{}D".format(cvparticlename)].q_late_pulses)                         else 0.0
####		vars_common["cvdihalength"]      = frame["CV_DirectHitsValues_{}A".format(cvparticlename)].dir_track_length                      if not np.isnan(frame["CV_DirectHitsValues_{}A".format(cvparticlename)].dir_track_length)                      else 0.0
####		vars_common["cvdihasmoothness"]  = frame["CV_DirectHitsValues_{}A".format(cvparticlename)].dir_track_hit_distribution_smoothness if not np.isnan(frame["CV_DirectHitsValues_{}A".format(cvparticlename)].dir_track_hit_distribution_smoothness) else 1.0e100
####		vars_common["cvdihaqdirect"]     = frame["CV_DirectHitsValues_{}A".format(cvparticlename)].q_dir_pulses                          if not np.isnan(frame["CV_DirectHitsValues_{}A".format(cvparticlename)].q_dir_pulses)                          else 0.0
####		vars_common["cvdihaqearly"]      = frame["CV_DirectHitsValues_{}A".format(cvparticlename)].q_early_pulses                        if not np.isnan(frame["CV_DirectHitsValues_{}A".format(cvparticlename)].q_early_pulses)                        else 0.0
####		vars_common["cvdihaqlate"]       = frame["CV_DirectHitsValues_{}A".format(cvparticlename)].q_late_pulses                         if not np.isnan(frame["CV_DirectHitsValues_{}A".format(cvparticlename)].q_late_pulses)                         else 0.0
		vars_common["cvhiscog"]          = np.linalg.norm([ wcog for wcog in frame["CV_HitStatisticsValues"].cog ])
		vars_common["cvtictimefwhm"]     = frame["CV_TimeCharacteristicsValues_{}".format(cvparticlename)].timelength_fwhm
		vars_common["cvtictimetot"]      = frame["CV_TimeCharacteristicsValues_{}".format(cvparticlename)].timelength_last_first
		vars_common["cvtrclength"]       = frame["CV_TrackCharacteristicsValues_{}".format(cvparticlename)].track_hits_separation_length
		vars_common["cvtrcsmoothness"]   = frame["CV_TrackCharacteristicsValues_{}".format(cvparticlename)].track_hits_distribution_smoothness
		vars_common["cvtrcavgdistq"]     = frame["CV_TrackCharacteristicsValues_{}".format(cvparticlename)].avg_dom_dist_q_tot_dom
	# USING THE BMM BELOW
#		vars_common["cvdihabmmlength"]     = frame["CV_DirectHitsValues_{}_BMMA".format(cvparticlename)].dir_track_length                            if not np.isnan(frame["CV_DirectHitsValues_{}_BMMA".format(cvparticlename)].dir_track_length)                      else 0.0
#		vars_common["cvdihabmmsmoothness"] = frame["CV_DirectHitsValues_{}_BMMA".format(cvparticlename)].dir_track_hit_distribution_smoothness       if not np.isnan(frame["CV_DirectHitsValues_{}_BMMA".format(cvparticlename)].dir_track_hit_distribution_smoothness) else 1.0e100
#		vars_common["cvdihabmmqdirect"]    = frame["CV_DirectHitsValues_{}_BMMA".format(cvparticlename)].q_dir_pulses                                if not np.isnan(frame["CV_DirectHitsValues_{}_BMMA".format(cvparticlename)].q_dir_pulses)                          else 0.0
#		vars_common["cvdihabmmqearly"]     = frame["CV_DirectHitsValues_{}_BMMA".format(cvparticlename)].q_early_pulses                              if not np.isnan(frame["CV_DirectHitsValues_{}_BMMA".format(cvparticlename)].q_early_pulses)                        else 0.0
#		vars_common["cvdihabmmqlate"]      = frame["CV_DirectHitsValues_{}_BMMA".format(cvparticlename)].q_late_pulses                               if not np.isnan(frame["CV_DirectHitsValues_{}_BMMA".format(cvparticlename)].q_late_pulses)                         else 0.0
#		vars_common["cvdihdbmmlength"]     = frame["CV_DirectHitsValues_{}_BMMD".format(cvparticlename)].dir_track_length                            if not np.isnan(frame["CV_DirectHitsValues_{}_BMMD".format(cvparticlename)].dir_track_length)                      else 0.0
#		vars_common["cvdihdbmmsmoothness"] = frame["CV_DirectHitsValues_{}_BMMD".format(cvparticlename)].dir_track_hit_distribution_smoothness       if not np.isnan(frame["CV_DirectHitsValues_{}_BMMD".format(cvparticlename)].dir_track_hit_distribution_smoothness) else 1.0e100
#		vars_common["cvdihdbmmqdirect"]    = frame["CV_DirectHitsValues_{}_BMMD".format(cvparticlename)].q_dir_pulses                                if not np.isnan(frame["CV_DirectHitsValues_{}_BMMD".format(cvparticlename)].q_dir_pulses)                          else 0.0
#		vars_common["cvdihdbmmqearly"]     = frame["CV_DirectHitsValues_{}_BMMD".format(cvparticlename)].q_early_pulses                              if not np.isnan(frame["CV_DirectHitsValues_{}_BMMD".format(cvparticlename)].q_early_pulses)                        else 0.0
#		vars_common["cvdihdbmmqlate"]      = frame["CV_DirectHitsValues_{}_BMMD".format(cvparticlename)].q_late_pulses                               if not np.isnan(frame["CV_DirectHitsValues_{}_BMMD".format(cvparticlename)].q_late_pulses)                         else 0.0
#		vars_common["cvtrcbmmlength"]      = frame["CV_TrackCharacteristicsValues_{}_BMM".format(cvparticlename)].track_hits_separation_length
#		vars_common["cvtrcbmmsmoothness"]  = frame["CV_TrackCharacteristicsValues_{}_BMM".format(cvparticlename)].track_hits_distribution_smoothness
#		vars_common["cvtrcbmmavgdistq"]    = frame["CV_TrackCharacteristicsValues_{}_BMM".format(cvparticlename)].avg_dom_dist_q_tot_dom
#		vars_common["cvticbmmtimefwhm"]    = frame["CV_TimeCharacteristicsValues_{}_BMM".format(cvparticlename)].timelength_fwhm
#		vars_common["cvticbmmtimetot"]     = frame["CV_TimeCharacteristicsValues_{}_BMM".format(cvparticlename)].timelength_last_first
	vars_all.update(vars_common)

	# Millipede
	vars_millipede = {}
	if lev in ["preBDT","L5","L6"]:
		vars_millipede["mpavge"] = frame[millipededict]["avg_e"]
		vars_millipede["mpstde"] = frame[millipededict]["std_e"]
		vars_millipede["mprsde"] = frame[millipededict]["rsd_e"]
	vars_all.update(vars_millipede)


#	# Cherenkov Offset
#	vars_cherenkovoffs = {}
#	if lev in ["preBDT","L5","L6"]:
#		vars_cherenkovoffs["coavgx"] = frame[cherenkovoffsetdict]["x_avg"]
#		vars_cherenkovoffs["costdx"] = frame[cherenkovoffsetdict]["x_std"]
#		vars_cherenkovoffs["corsdx"] = frame[cherenkovoffsetdict]["x_rsd"]
#		vars_cherenkovoffs["coavgt"] = frame[cherenkovoffsetdict]["t_avg"]
#		vars_cherenkovoffs["costdt"] = frame[cherenkovoffsetdict]["t_std"]
#		vars_cherenkovoffs["corsdt"] = frame[cherenkovoffsetdict]["t_rsd"]
#	vars_all.update(vars_cherenkovoffs)
#
#	# Frank-Tamm Coefficient
#	vars_franktamm = {}
#	if lev in ["preBDT","L5","L6"]:
#		vars_franktamm["ftxanpe"]     = frame["FrankTammCoeff"]["XA_FT_npe"]
#		vars_franktamm["ftanpelgeom"] = frame["FrankTammCoeff"]["A_FT_npe_lgeom"]
#		vars_franktamm["ftanpeldihd"] = frame["FrankTammCoeff"]["A_FT_npe_ldihd"]
#		vars_franktamm["ftanpeldiha"] = frame["FrankTammCoeff"]["A_FT_npe_ldiha"]
#		vars_franktamm["ftanpeltrc"]  = frame["FrankTammCoeff"]["A_FT_npe_ltrc"]
#		vars_franktamm["ftxaqdihd"]     = frame["FrankTammCoeff"]["XA_FT_qdihd"]
#		vars_franktamm["ftaqdihdlgeom"] = frame["FrankTammCoeff"]["A_FT_qdihd_lgeom"]
#		vars_franktamm["ftaqdihdldihd"] = frame["FrankTammCoeff"]["A_FT_qdihd_ldihd"]
#		vars_franktamm["ftaqdihdldiha"] = frame["FrankTammCoeff"]["A_FT_qdihd_ldiha"]
#		vars_franktamm["ftaqdihdltrc"]  = frame["FrankTammCoeff"]["A_FT_qdihd_ltrc"]
#		vars_franktamm["ftxaqdiha"]     = frame["FrankTammCoeff"]["XA_FT_qdiha"]
#		vars_franktamm["ftaqdihalgeom"] = frame["FrankTammCoeff"]["A_FT_qdiha_lgeom"]
#		vars_franktamm["ftaqdihaldihd"] = frame["FrankTammCoeff"]["A_FT_qdiha_ldihd"]
#		vars_franktamm["ftaqdihaldiha"] = frame["FrankTammCoeff"]["A_FT_qdiha_ldiha"]
#		vars_franktamm["ftaqdihaltrc"]  = frame["FrankTammCoeff"]["A_FT_qdiha_ltrc"]
#	vars_all.update(vars_franktamm)

#####	# Hit Production Angle
#####	vars_hitprodangle = {}
#####	if lev in ["preBDT","L5","L6"]:
#####		vars_hitprodangle["pabmmiipavg"] = frame[hitprodangledict.format("BrightestMedianParticle","InIcePulsesSRTTW")]["theta_avg"]
#####		vars_hitprodangle["pabmmiipstd"] = frame[hitprodangledict.format("BrightestMedianParticle","InIcePulsesSRTTW")]["theta_std"]
#####		vars_hitprodangle["pabmmiiprsd"] = frame[hitprodangledict.format("BrightestMedianParticle","InIcePulsesSRTTW")]["theta_rsd"]
#####		vars_hitprodangle["pabmmbmmavg"] = frame[hitprodangledict.format("BrightestMedianParticle","BrightestMedianInIcePulsesSRTTW")]["theta_avg"]
#####		vars_hitprodangle["pabmmbmmstd"] = frame[hitprodangledict.format("BrightestMedianParticle","BrightestMedianInIcePulsesSRTTW")]["theta_std"]
#####		vars_hitprodangle["pabmmbmmrsd"] = frame[hitprodangledict.format("BrightestMedianParticle","BrightestMedianInIcePulsesSRTTW")]["theta_rsd"]
#####		vars_hitprodangle["pabmmclhavg"] = frame[hitprodangledict.format("BrightestMedianParticle","ClosestHitsIIPBMP")]["theta_avg"]
#####		vars_hitprodangle["pabmmclhstd"] = frame[hitprodangledict.format("BrightestMedianParticle","ClosestHitsIIPBMP")]["theta_std"]
#####		vars_hitprodangle["pabmmclhrsd"] = frame[hitprodangledict.format("BrightestMedianParticle","ClosestHitsIIPBMP")]["theta_rsd"]
#####	vars_all.update(vars_hitprodangle)

	# Combined Variables
	vars_combined = {}
	if lev in ["preBDT","L5","L6"] and gen!="exprm":
	# Beta
		vars_combined["mcopbetadiff"] = vars_primary["mcbeta"] - vars_ophelia["opbeta"]                      #if gen != "exprm" else 2. # Unphysical experimental value 
		vars_combined["mcbmbetadiff"] = vars_primary["mcbeta"] - vars_brightestmedian["bmbeta"]              #if gen != "exprm" else 2. # Unphysical experimental value 

	if lev in ["preBDT","L5","L6"]:
	# Non-length
#		vars_combined["bmcvdihdnonlength"]       =   vars_brightestmedian["bmgeomlength"] - vars_common["cvdihdlength"]
#		vars_combined["bmcvdihdnonlengthfrac"]   = ( vars_brightestmedian["bmgeomlength"] - vars_common["cvdihdlength"] ) / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.
####		vars_combined["bmcvdihdlengthfillratio"] =                                          vars_common["cvdihdlength"]   / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.
#		vars_combined["bmcvdihanonlength"]       =   vars_brightestmedian["bmgeomlength"] - vars_common["cvdihalength"]
#		vars_combined["bmcvdihanonlengthfrac"]   = ( vars_brightestmedian["bmgeomlength"] - vars_common["cvdihalength"] ) / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.
####		vars_combined["bmcvdihalengthfillratio"] =                                          vars_common["cvdihalength"]   / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.
#		vars_combined["bmcvtrcnonlength"]        =   vars_brightestmedian["bmgeomlength"] - vars_common["cvtrclength"]
#		vars_combined["bmcvtrcnonlengthfrac"]    = ( vars_brightestmedian["bmgeomlength"] - vars_common["cvtrclength"] ) / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.
		vars_combined["bmcvtrclengthfillratio"]  =                                          vars_common["cvtrclength"]   / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.

#	# Non-length BMM
#		vars_combined["bmcvdihdbmmnonlength"]       =   vars_brightestmedian["bmgeomlength"] - vars_common["cvdihdbmmlength"]
#		vars_combined["bmcvdihdbmmnonlengthfrac"]   = ( vars_brightestmedian["bmgeomlength"] - vars_common["cvdihdbmmlength"] ) / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.
#		vars_combined["bmcvdihdbmmlengthfillratio"] =                                          vars_common["cvdihdbmmlength"]   / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.
#		vars_combined["bmcvdihabmmnonlength"]       =   vars_brightestmedian["bmgeomlength"] - vars_common["cvdihabmmlength"]
#		vars_combined["bmcvdihabmmnonlengthfrac"]   = ( vars_brightestmedian["bmgeomlength"] - vars_common["cvdihabmmlength"] ) / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.
#		vars_combined["bmcvdihabmmlengthfillratio"] =                                          vars_common["cvdihabmmlength"]   / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.
#		vars_combined["bmcvtrcbmmnonlength"]        =   vars_brightestmedian["bmgeomlength"] - vars_common["cvtrcbmmlength"]
#		vars_combined["bmcvtrcbmmnonlengthfrac"]    = ( vars_brightestmedian["bmgeomlength"] - vars_common["cvtrcbmmlength"] ) / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.
#		vars_combined["bmcvtrcbmmlengthfillratio"]  =                                          vars_common["cvtrcbmmlength"]   / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.

	# Non-time
#		vars_combined["bmcvticnontimefwhm"]       =   vars_brightestmedian["bmgeomtime"] - vars_common["cvtictimefwhm"]
#		vars_combined["bmcvticnontimefwhmfrac"]   = ( vars_brightestmedian["bmgeomtime"] - vars_common["cvtictimefwhm"] ) / vars_brightestmedian["bmgeomtime"] if vars_brightestmedian["bmgeomtime"]!=0. else 0.
		vars_combined["bmcvtictimefwhmfillratio"] =                                        vars_common["cvtictimefwhm"]   / vars_brightestmedian["bmgeomtime"] if vars_brightestmedian["bmgeomtime"]!=0. else 0.
#		vars_combined["bmcvticnontimetot"]        =   vars_brightestmedian["bmgeomtime"] - vars_common["cvtictimetot"]
#		vars_combined["bmcvticnontimetotfrac"]    = ( vars_brightestmedian["bmgeomtime"] - vars_common["cvtictimetot"] ) / vars_brightestmedian["bmgeomtime"] if vars_brightestmedian["bmgeomtime"]!=0. else 0.
		vars_combined["bmcvtictimetotfillratio"]  =                                        vars_common["cvtictimetot"]   / vars_brightestmedian["bmgeomtime"] if vars_brightestmedian["bmgeomtime"]!=0. else 0.

#	# Non-time BMM
#		vars_combined["bmcvticbmmnontimefwhm"]       =   vars_brightestmedian["bmgeomtime"] - vars_common["cvticbmmtimefwhm"]
#		vars_combined["bmcvticbmmnontimefwhmfrac"]   = ( vars_brightestmedian["bmgeomtime"] - vars_common["cvticbmmtimefwhm"] ) / vars_brightestmedian["bmgeomtime"] if vars_brightestmedian["bmgeomtime"]!=0. else 0.
#		vars_combined["bmcvticbmmtimefwhmfillratio"] =                                        vars_common["cvticbmmtimefwhm"]   / vars_brightestmedian["bmgeomtime"] if vars_brightestmedian["bmgeomtime"]!=0. else 0.
#		vars_combined["bmcvticbmmnontimetot"]        =   vars_brightestmedian["bmgeomtime"] - vars_common["cvticbmmtimetot"]
#		vars_combined["bmcvticbmmnontimetotfrac"]    = ( vars_brightestmedian["bmgeomtime"] - vars_common["cvticbmmtimetot"] ) / vars_brightestmedian["bmgeomtime"] if vars_brightestmedian["bmgeomtime"]!=0. else 0.
#		vars_combined["bmcvticbmmtimetotfillratio"]  =                                        vars_common["cvticbmmtimetot"]   / vars_brightestmedian["bmgeomtime"] if vars_brightestmedian["bmgeomtime"]!=0. else 0.

	# COG Offset
#		vars_combined["bmcvhiscogoffset"]         =   np.linalg.norm([ wcog-wcen for wcog, wcen in zip(frame["CV_HitStatisticsValues"].cog, [ frame["Centrality_BrightestMedianParticle"][w] for w in ["x","y","z"] ]) ])
		vars_combined["bmcvhisrelativecogoffset"] = ( np.linalg.norm([ wcog-wcen for wcog, wcen in zip(frame["CV_HitStatisticsValues"].cog, [ frame["Centrality_BrightestMedianParticle"][w] for w in ["x","y","z"] ]) ]) ) / vars_brightestmedian["bmgeomlength"] if vars_brightestmedian["bmgeomlength"]!=0. else 0.
	vars_all.update(vars_combined)

#	# BDT Scores
#	vars_bdt = {}
#	if lev in ["L5","L6"]:
#		vars_bdt["bdtascore"] = frame["BDTAScore"].value
#		vars_bdt["bdtbscore"] = frame["BDTBScore"].value
#		vars_bdt["bdtcscore"] = frame["BDTCScore"].value
#		vars_bdt["bdtdscore"] = frame["BDTDScore"].value
#		vars_bdt["bdtescore"] = frame["BDTEScore"].value
#	vars_all.update(vars_bdt)

	# Weights
	vars_weight = {}
	if lev in ["trigger","ehefilter","L2","L3","L4","preBDT","L5","L6"] and gen!="exprm":
		vars_weight["wtcount"]                                              = frame["CountingWeightFactor"].value
	if lev in ["trigger","ehefilter","L2","L3","L4","preBDT","L5","L6"] and gen!="exprm":
		vars_weight["wtonenumudif2017central"]                              = frame["OneWeightDict"]["oneweight_reduced_numudif2017_central"]
		vars_weight["wtonenumudif2017plussigma"]                            = frame["OneWeightDict"]["oneweight_reduced_numudif2017_plussigma"]
		vars_weight["wtonenumudif2017minussigma"]                           = frame["OneWeightDict"]["oneweight_reduced_numudif2017_minussigma"]
		vars_weight["wtoverlapnumudif2017central_nancymedium_nancyhigh"]    = frame["OneWeightDict"]["overlap_weight_numudif2017_central__nancy_medium__nancy_high"]
		vars_weight["wtoverlapnumudif2017plussigma_nancymedium_nancyhigh"]  = frame["OneWeightDict"]["overlap_weight_numudif2017_plussigma__nancy_medium__nancy_high"]
		vars_weight["wtoverlapnumudif2017minussigma_nancymedium_nancyhigh"] = frame["OneWeightDict"]["overlap_weight_numudif2017_minussigma__nancy_medium__nancy_high"]
		vars_weight["wtoverlapnumudif2017central_nancyhigh_iceprodhigh"]    = frame["OneWeightDict"]["overlap_weight_numudif2017_central__nancy_high__iceprod_high"]
		vars_weight["wtoverlapnumudif2017plussigma_nancyhigh_iceprodhigh"]  = frame["OneWeightDict"]["overlap_weight_numudif2017_plussigma__nancy_high__iceprod_high"]
		vars_weight["wtoverlapnumudif2017minussigma_nancyhigh_iceprodhigh"] = frame["OneWeightDict"]["overlap_weight_numudif2017_minussigma__nancy_high__iceprod_high"]
		vars_weight["wtonenumudif2019central"]                              = frame["OneWeightDict"]["oneweight_reduced_numudif2019_central"]
		vars_weight["wtonenumudif2019plussigma"]                            = frame["OneWeightDict"]["oneweight_reduced_numudif2019_plussigma"]
		vars_weight["wtonenumudif2019minussigma"]                           = frame["OneWeightDict"]["oneweight_reduced_numudif2019_minussigma"]
		vars_weight["wtoverlapnumudif2019central_nancymedium_nancyhigh"]    = frame["OneWeightDict"]["overlap_weight_numudif2019_central__nancy_medium__nancy_high"]
		vars_weight["wtoverlapnumudif2019plussigma_nancymedium_nancyhigh"]  = frame["OneWeightDict"]["overlap_weight_numudif2019_plussigma__nancy_medium__nancy_high"]
		vars_weight["wtoverlapnumudif2019minussigma_nancymedium_nancyhigh"] = frame["OneWeightDict"]["overlap_weight_numudif2019_minussigma__nancy_medium__nancy_high"]
		vars_weight["wtoverlapnumudif2019central_nancyhigh_iceprodhigh"]    = frame["OneWeightDict"]["overlap_weight_numudif2019_central__nancy_high__iceprod_high"]
		vars_weight["wtoverlapnumudif2019plussigma_nancyhigh_iceprodhigh"]  = frame["OneWeightDict"]["overlap_weight_numudif2019_plussigma__nancy_high__iceprod_high"]
		vars_weight["wtoverlapnumudif2019minussigma_nancyhigh_iceprodhigh"] = frame["OneWeightDict"]["overlap_weight_numudif2019_minussigma__nancy_high__iceprod_high"]
		vars_weight["wtonehese2019central"]                                 = frame["OneWeightDict"]["oneweight_reduced_hese2019_central"]
		vars_weight["wtonehese2019plussigma"]                               = frame["OneWeightDict"]["oneweight_reduced_hese2019_plussigma"]
		vars_weight["wtonehese2019minussigma"]                              = frame["OneWeightDict"]["oneweight_reduced_hese2019_minussigma"]
		vars_weight["wtoverlaphese2019central_nancymedium_nancyhigh"]       = frame["OneWeightDict"]["overlap_weight_hese2019_central__nancy_medium__nancy_high"]
		vars_weight["wtoverlaphese2019plussigma_nancymedium_nancyhigh"]     = frame["OneWeightDict"]["overlap_weight_hese2019_plussigma__nancy_medium__nancy_high"]
		vars_weight["wtoverlaphese2019minussigma_nancymedium_nancyhigh"]    = frame["OneWeightDict"]["overlap_weight_hese2019_minussigma__nancy_medium__nancy_high"]
		vars_weight["wtoverlaphese2019central_nancyhigh_iceprodhigh"]       = frame["OneWeightDict"]["overlap_weight_hese2019_central__nancy_high__iceprod_high"]
		vars_weight["wtoverlaphese2019plussigma_nancyhigh_iceprodhigh"]     = frame["OneWeightDict"]["overlap_weight_hese2019_plussigma__nancy_high__iceprod_high"]
		vars_weight["wtoverlaphese2019minussigma_nancyhigh_iceprodhigh"]    = frame["OneWeightDict"]["overlap_weight_hese2019_minussigma__nancy_high__iceprod_high"]
	vars_all.update(vars_weight)

	# ABurgmanBookkeeping
	vars_bookkeeping = {}
	if lev in ["trigger","ehefilter","L2","L3","L4","preBDT","L5","L6"]:
		vars_bookkeeping["genmpsim"] = frame["ABurgmanGen"]["mpsim"]
		vars_bookkeeping["gennugen"] = frame["ABurgmanGen"]["nugen"]
		vars_bookkeeping["genexprm"] = frame["ABurgmanGen"]["exprm"]
		vars_bookkeeping["num00000"] = frame["ABurgmanNum"]["00000"]
		vars_bookkeeping["num00001"] = frame["ABurgmanNum"]["00001"]
		vars_bookkeeping["num00002"] = frame["ABurgmanNum"]["00002"]
		vars_bookkeeping["num11070"] = frame["ABurgmanNum"]["11070"]
		vars_bookkeeping["num11297"] = frame["ABurgmanNum"]["11297"]
		vars_bookkeeping["num86001"] = frame["ABurgmanNum"]["86001"]
		vars_bookkeeping["num86002"] = frame["ABurgmanNum"]["86002"]
		vars_bookkeeping["num86003"] = frame["ABurgmanNum"]["86003"]
		vars_bookkeeping["num86004"] = frame["ABurgmanNum"]["86004"]
		vars_bookkeeping["num86005"] = frame["ABurgmanNum"]["86005"]
		vars_bookkeeping["num86006"] = frame["ABurgmanNum"]["86006"]
		vars_bookkeeping["num86007"] = frame["ABurgmanNum"]["86007"]
		vars_bookkeeping["num86008"] = frame["ABurgmanNum"]["86008"]
		vars_bookkeeping["num86009"] = frame["ABurgmanNum"]["86009"]
		vars_bookkeeping["num86010"] = frame["ABurgmanNum"]["86010"]
		vars_bookkeeping["num86901"] = frame["ABurgmanNum"]["86901"]
		vars_bookkeeping["num86902"] = frame["ABurgmanNum"]["86902"]
		vars_bookkeeping["num86903"] = frame["ABurgmanNum"]["86903"]
		vars_bookkeeping["num86904"] = frame["ABurgmanNum"]["86904"]
		vars_bookkeeping["num86905"] = frame["ABurgmanNum"]["86905"]
		vars_bookkeeping["num86906"] = frame["ABurgmanNum"]["86906"]
		vars_bookkeeping["num86907"] = frame["ABurgmanNum"]["86907"]
		vars_bookkeeping["num86908"] = frame["ABurgmanNum"]["86908"]
		vars_bookkeeping["num86909"] = frame["ABurgmanNum"]["86909"]
		vars_bookkeeping["num86910"] = frame["ABurgmanNum"]["86910"]
		# Event time below
		vars_bookkeeping["utcstartyear"]       = -1. if gen!="exprm" else frame["I3EventHeader"].start_time.utc_year
		vars_bookkeeping["utcstartmonth"]      = -1. if gen!="exprm" else frame["I3EventHeader"].start_time.utc_month.numerator
		vars_bookkeeping["utcstartdayofmonth"] = -1. if gen!="exprm" else frame["I3EventHeader"].start_time.utc_day_of_month
		vars_bookkeeping["utcstartsecond"]     = -1. if gen!="exprm" else frame["I3EventHeader"].start_time.utc_sec
		vars_bookkeeping["utcstartnanosecond"] = -1. if gen!="exprm" else frame["I3EventHeader"].start_time.utc_nano_sec
		vars_bookkeeping["utcendyear"]         = -1. if gen!="exprm" else frame["I3EventHeader"].end_time.utc_year
		vars_bookkeeping["utcendmonth"]        = -1. if gen!="exprm" else frame["I3EventHeader"].end_time.utc_month.numerator
		vars_bookkeeping["utcenddayofmonth"]   = -1. if gen!="exprm" else frame["I3EventHeader"].end_time.utc_day_of_month
		vars_bookkeeping["utcendsecond"]       = -1. if gen!="exprm" else frame["I3EventHeader"].end_time.utc_sec
		vars_bookkeeping["utcendnanosecond"]   = -1. if gen!="exprm" else frame["I3EventHeader"].end_time.utc_nano_sec
		# FrameHeader
		vars_bookkeeping["fhseason"]  = -1. if gen!="exprm" else int(read_ABurgmanGenNum(frame)["num"][-2:])
		vars_bookkeeping["fhrunid"]   = -1. if gen!="exprm" else frame["I3EventHeader"].run_id
		vars_bookkeeping["fheventid"] = -1. if gen!="exprm" else frame["I3EventHeader"].event_id
	vars_all.update(vars_bookkeeping)

	frame["ABurgmanVars"] = I3MapStringDouble(vars_all)
	frame["ABurgmanKeys"] = I3String(",".join(sorted(vars_all.keys())))

#def export_aburgman_variables_L0(frame):
#	export_aburgman_variables(frame,"L0")
#def export_aburgman_variables_L1(frame):
#	export_aburgman_variables(frame,"L1")
#def export_aburgman_variables_L2(frame):
#	export_aburgman_variables(frame,"L2")
#def export_aburgman_variables_L3(frame):
#	export_aburgman_variables(frame,"L3")
#def export_aburgman_variables_L4(frame):
#	export_aburgman_variables(frame,"L4")
#def export_aburgman_variables_preBDT(frame):
#	export_aburgman_variables(frame,"preBDT")
#def export_aburgman_variables_L5(frame):
#	export_aburgman_variables(frame,"L5")
#def export_aburgman_variables_L6(frame):
#	export_aburgman_variables(frame,"L6")






