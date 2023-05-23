#import numpy as np
#import scipy.constants as sc

from icecube import dataclasses#, icetray, dataio, tableio, common_variables, improvedLinefit, portia#, recclasses, sim_services, phys_services
#from icecube.icetray import I3Units
from icecube.dataclasses import I3MCTree, I3Particle, I3RecoPulseSeriesMap, I3RecoPulse#, I3MapStringDouble
#from icecube.tableio import I3TableWriter
#from icecube.hdfwriter import I3HDFTableService
#from I3Tray import *


def add_MCPrimaryParticle(frame):
	if "I3MCTree" in frame and "MCPrimaryParticle" not in frame:
		accepted_primaries = ["monopole","nue","nuebar","numu","numubar","nutau","nutaubar"]
		try:
			primaries = [ p for p in frame["I3MCTree"].get_primaries() if str(p.type).lower() in accepted_primaries ]
		except AttributeError:
			primaries = [ p for p in [ frame["I3MCTree"][0] ] if str(p.type).lower() in accepted_primaries ]
#			temp_primary = frame["I3MCTree"][0]
#			if str(temp_primary.type).lower() in accepted_primaries:
#				primaries = [ temp_primaries ]
#			else:
#				primaries = []
		if len(primaries)!=1:
			exit("Event nr {} has {} primary particles (neutrinos and monopoles counted) in it's MCTree! Deal with this case!".format(frame["I3EventHeader"].event_id,len(primaries)))
		primary = primaries[0]
		frame["MCPrimaryParticle"] = primary

def add_I3EventHeader(frame):
    eh = dataclasses.I3EventHeader()
    eh.run_id = 1
    eh.event_id = add_I3EventHeader.event_id
    add_I3EventHeader.event_id += 1
    frame['I3EventHeader'] = eh


def delete_I3EventHeader(frame):
	del frame["I3EventHeader"]
	# tray.Add("Delete", Keys=["I3EventHeader"])

# Make some module that adds in useful cut information, e.g. centrality of the track.
# Look at what exists in CommonVariables!

####def add_InIcePulsesMap(frame):
####	if not frame.Has("InIcePulsesMap"):
####		frame["InIcePulsesMap"]=I3RecoPulseSeriesMap.from_frame(frame, "InIcePulses")

def add_InIcePulsesMap(frame):
	from icecube import dataclasses
	from icecube.dataclasses import I3RecoPulseSeriesMap
	print(list(frame.keys()))
	frame["InIcePulsesMap"]=I3RecoPulseSeriesMap.from_frame(frame, "InIcePulses")

def add_InIcePulsesInfo(frame):
	import numpy as np
	from icecube import dataclasses
	from icecube.dataclasses import I3RecoPulseSeriesMap, I3RecoPulse, I3Double
	from icecube.dataclasses import I3MCTree, I3Particle, I3RecoPulseSeriesMap, I3RecoPulse, I3MapStringDouble
	if "InIcePulsesMap" not in frame:
		add_InIcePulsesMap(frame)
	pulsemap=frame["InIcePulsesMap"]
	totcharge=0.
	ndom=0.
	chargedensity=np.nan
	maxcharge=0.
	for omkey in list(pulsemap.keys()):
		for pulse in pulsemap[omkey]:
			totcharge+=pulse.charge
			maxcharge=max(maxcharge,pulse.charge)
		ndom+=1
	chargedensity=totcharge/ndom
	frame["InIcePulsesTotalCharge"]   = I3Double(totcharge)
	frame["InIcePulsesNDOM"]          = I3Double(ndom)
	frame["InIcePulsesChargeDensity"] = I3Double(chargedensity)
	frame["InIcePulsesMaxChargePulse"] = I3Double(maxcharge)

def add_MCPEinfo(frame):
	if "I3MCPESeriesMap" not in frame:
		return
	nmcpe=0
#	for _, mcpes in frame["I3MCPESeriesMap"]:
#		nmcpe += sum([ mcpe.npe for mcpe in mcpes ])
	nmcpe=float( sum([ sum([ mcpe.npe for mcpe in mcpes ]) for mcpe in list(frame["I3MCPESeriesMap"].values()) ]) )
	frame["MCPEn"]=I3Double(nmcpe)
	if "I3MCTree" not in frame:
		return
	ltot=0
	ltot=float( sum([ mcp.length for mcp in frame["I3MCTree"] if str(mcp.type)=="Monopole" ]) )
	frame["MCPEl"]=I3Double(ltot)
	frame["MCPEnperl"]=I3Double(nmcpe/ltot)

