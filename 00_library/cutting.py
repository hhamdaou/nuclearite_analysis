#import numpy as np
#import scipy.constants as sc

from icecube import icetray
import numpy as np
from icecube import portia
#from icecube import dataclasses, dataio, tableio, common_variables, improvedLinefit, portia#, recclasses, sim_services, phys_services
#from icecube.icetray import I3Units
#from icecube.dataclasses import I3MCTree, I3Particle, I3RecoPulseSeriesMap, I3RecoPulse, I3MapStringDouble
#from icecube.tableio import I3TableWriter
#from icecube.hdfwriter import I3HDFTableService
#from I3Tray import *



class OrphanStreamDrop(icetray.I3PacketModule):
    """ Drop everything, the complete FramePackage, if this stream is orphaned """
    def __init__(self, ctx):
        icetray.I3PacketModule.__init__(self, ctx, icetray.I3Frame.DAQ)
        self.AddParameter("OrphanStream", "Drop everything if this stream is orphaned", '')
        self.AddOutBox("OutBox")
    def Configure(self):
        icetray.I3PacketModule.Configure(self)
        self.orphan_stream =self.GetParameter("OrphanStream")
        if self.orphan_stream == '':
            log_fatal('Configure "OrphanStream"')
    def FramePacket(self,frames):
        counter = 0
        for frame in frames:
            if frame.Has("I3EventHeader"):
                if frame["I3EventHeader"].sub_event_stream == self.orphan_stream:
                    counter+=1
        if counter!=0:
            for frame in frames:
                self.PushFrame(frame)
        return


def cut_filter_EHE(frame):
	passed_cut = False
	if frame.Has("QFilterMask"):
		filterkey="NO_KEY_DETECTED"
		if "EHEFilter_11" in frame["QFilterMask"].keys():
			filterkey="EHEFilter_11"
		if "EHEFilter_12" in frame["QFilterMask"].keys():
			filterkey="EHEFilter_12"
		if "EHEFilter_13" in frame["QFilterMask"].keys():
			filterkey="EHEFilter_13"
		if frame["QFilterMask"][filterkey].condition_passed and frame["QFilterMask"][filterkey].prescale_passed:
			passed_cut = True
	elif frame.Has("PoleEHESummaryPulseInfo"):
		if frame["PoleEHESummaryPulseInfo"].GetTotalBestNPE()>=1000:
			passed_cut = True
	elif frame.Has("EHESummaryPulseInfo"):
		if frame["EHESummaryPulseInfo"].GetTotalBestNPE()>=1000:
			passed_cut = True
	return passed_cut

def cut_filter_EHEAlert(frame):
	passed_cut = False
	if frame.Has("QFilterMask"):
		filterkey="NO_KEY_DETECTED"
		if "EHEAlertFilter_15" in frame["QFilterMask"].keys():
			filterkey="EHEAlertFilter_15"
		if frame["QFilterMask"][filterkey].condition_passed and frame["QFilterMask"][filterkey].prescale_passed:
			passed_cut = True
	return passed_cut


def cut_npe_at_value(frame, value):
	passed_cut = False
	if frame.Has("PoleEHESummaryPulseInfo"):
		if frame["PoleEHESummaryPulseInfo"].GetTotalBestNPE()>=value:
			passed_cut = True
	return passed_cut

def cut_npe_at_25000(frame):
	return cut_npe_at_value(frame,25000.)


def cut_nch_at_value(frame, value):
	passed_cut = False
	if frame.Has("PoleEHESummaryPulseInfo"):
		if frame["PoleEHESummaryPulseInfo"].GetTotalNch()>=value:
			passed_cut = True
	return passed_cut

def cut_nch_at_100(frame):
	return cut_nch_at_value(frame,100.)


def cut_log_npe_at_value(frame, value):
	passed_cut = False
	if frame.Has("PoleEHESummaryPulseInfo"):
		if np.log10(frame["PoleEHESummaryPulseInfo"].GetTotalBestNPE())>=value:
			passed_cut = True
	return passed_cut

