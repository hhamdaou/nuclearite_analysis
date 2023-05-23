# functions to calculate number of triplets and tuples, ration of # of triplets to # of HLC,
# inverse velocity, linefit chi2, linefit velocity, triplet inner angle, new cylinder variables

from icecube import dataclasses, sim_services,trigger_sim,dataio,icetray
from icecube import simclasses

from icecube.phys_services import Cylinder
from icecube.KalmanFilter.KalmanAlgorithm import *
from scipy.stats import kurtosis
from scipy.stats import skew
#from scipy.stats import mode

class SlowMPHit:
  def __init__(self, OMKey, time, info):
     self.omkey = OMKey
     self.time = time
     self.info = info

def hitfilter(frame, inputMapName):
    ignoreDC=False
    hitlist = []
    
    if type(frame[inputMapName]) == dataclasses.I3RecoPulseSeriesMapMask:
        inputMap = frame[inputMapName].apply(frame)
    else:
        inputMap = frame[inputMapName]

    
    for omkey, recoPulseVector in inputMap:
        if ignoreDC and omkey.string > 78:
            continue
        else:
            hitlist.extend([SlowMPHit(omkey, pulse.time, pulse) for pulse in recoPulseVector])
    
    hitlist.sort(key=lambda h: h.time)
    
    return hitlist

def Chi2CallKalman(X,T,Particle):
    if len(T) > 2:
        chi2 = 0.
        v = np.array([Particle.dir.x, Particle.dir.y, Particle.dir.z]) * Particle.speed
        chi2 = np.sum(np.linalg.norm(X - (Particle.pos + v * np.array(T)[:, np.newaxis]) ) ** 2)
        return chi2/(3.*len(T)-6.)
    
    else:
       return float('nan')


def AddVariables(frame):
    #print ("Adding variables")

    # commented out by Timo
    # if frame.Has('SLOPTuples_X'):
    #     X = frame['SLOPTuples_X']
    #     Y = frame['SLOPTuples_Y']
    #     Z = frame['SLOPTuples_Z']
    #
    #     Triplets = np.zeros((len(X)/4,3))
    #     i=0
    #     for j in range(len(X)):
    #         Number = j%4
    #         if Number == 0:
    #             R = np.zeros((3,3))
    #         elif Number == 3:
    #             Triplets[i,:] = R[0,:] - R[2,:]
    #             i+=1
    #         if Number<3:
    #             R[Number,:] = np.array([X[j],Y[j],Z[j]])
    #     Mean_Vector = Triplets.mean(axis=0)
    #     Psi = np.arccos((Mean_Vector[np.newaxis,:]*Triplets).sum(axis=1)/np.sqrt((Mean_Vector**2).sum()*(Triplets**2).sum(axis=1)))
    #     frame['BDT_MeanAngle'] = dataclasses.I3Double(Psi.mean())
    #     frame['BDT_VarAngle']  = dataclasses.I3Double(Psi.std())
    #     print('after angle')
    if frame.Has('MeanAngle') and frame.Has('VarAngle'):
        frame['BDT_MeanAngle'] = frame['MeanAngle']#dataclasses.I3Double(Psi.mean())
        frame['BDT_VarAngle']  = frame['VarAngle']#dataclasses.I3Double(Psi.std())

    ## NTuple
    if frame.Has("SLOPTuples_RelV_Launches") and frame.Has("SLOPLaunchMapTuples"):
        N_Triplet = len(frame["SLOPTuples_RelV_Launches"])
        #print('N_Triplet',N_Triplet)
        NTuple = 0.
        for omkey, pulse_list in frame["SLOPLaunchMapTuples"]:
            for pulses in pulse_list:
                NTuple += 1.
        frame["BDT_NTuple"] = dataclasses.I3Double(NTuple)
        frame["BDT_NTriplet"] = dataclasses.I3Double(N_Triplet)
        frame["BDT_Triplet_HLC"] = dataclasses.I3Double(N_Triplet/float(NTuple))
    ## NHITS
    if frame.Has("SLOPKalman_NHits"):
        frame["BDT_NHits"] = frame["SLOPKalman_NHits"]

    ## P
    if frame.Has("SLOPKalman_P"):
        frame["BDT_P"] = dataclasses.I3Double(frame["SLOPKalman_P"][-1])

    ## Chi2Pred
    if frame.Has("SLOPLineFit_Chi2"):
        frame["BDT_Chi2Pred"] = frame["SLOPLineFit_Chi2"]
    elif frame.Has('I3Geometry') and frame.Has("SLOPLaunchMapTuples"):
        geo = frame['I3Geometry']
        hitlist = hitfilter(frame, "SLOPLaunchMapTuples") 
        x, y, z, t = [], [], [], []
        for hit in hitlist:
            pos = geo.omgeo[hit.omkey].position
            x += [np.array(pos)]
            t += [hit.time]
        particle = frame['SLOPTuples_LineFit']
        if particle.fit_status == dataclasses.I3Particle.FitStatus.OK:
            frame['BDT_Chi2Pred']= dataclasses.I3Double(Chi2CallKalman(x,t,particle))
    #else:
        #print('chi2 not added')

    ## Velocity
    if frame.Has("SLOPTuples_LineFit"):
        frame["BDT_Velocity"] = dataclasses.I3Double(frame["SLOPTuples_LineFit"].speed)

    ## Triggerlength
    if frame.Has("I3TriggerHierarchy"):
        for trigger in frame['I3TriggerHierarchy']:
            #if trigger.key.config_id == 22005:
             trigger_length = trigger.length
        frame["BDT_TriggerLength"] = dataclasses.I3Double(trigger_length)
    ## Invvel
    if frame.Has("SLOPTuples_RelV_Launches"):
        frame["BDT_Invvel_mean"] = dataclasses.I3Double(np.mean(frame["SLOPTuples_RelV_Launches"]))

    if frame.Has("SLOPTuples_RelV_Launches"):
        frame["BDT_Invvel_max"] = dataclasses.I3Double(np.max(frame["SLOPTuples_RelV_Launches"]))

    if frame.Has("SLOPTuples_RelV_Launches"):
        frame["BDT_Invvel_min"] = dataclasses.I3Double(np.min(frame["SLOPTuples_RelV_Launches"]))

    if frame.Has("SLOPTuples_RelV_Launches"):
        frame["BDT_Invvel_var"] = dataclasses.I3Double(np.var(frame["SLOPTuples_RelV_Launches"]))

    if frame.Has("SLOPTuples_RelV_Launches"): # new!!!
        frame["BDT_Invvel_90per"] = dataclasses.I3Double(np.percentile(frame["SLOPTuples_RelV_Launches"],90))

    if frame.Has("SLOPTuples_RelV_Launches"): # new!!!
        frame["BDT_Invvel_10per"] = dataclasses.I3Double(np.percentile(frame["SLOPTuples_RelV_Launches"],10))

    if frame.Has("SLOPTuples_RelV_Launches"): # new!!!
        frame["BDT_Invvel_75per"] = dataclasses.I3Double(np.percentile(frame["SLOPTuples_RelV_Launches"],75))

    if frame.Has("SLOPTuples_RelV_Launches"): # new!!!
        frame["BDT_Invvel_25per"] = dataclasses.I3Double(np.percentile(frame["SLOPTuples_RelV_Launches"],25))

    if frame.Has("SLOPTuples_RelV_Launches"): # new!!!
        frame["BDT_Invvel_median"] = dataclasses.I3Double(np.median(frame["SLOPTuples_RelV_Launches"]))
    
    if frame.Has("SLOPTuples_RelV_Launches"): # new!!!
        frame["BDT_Invvel_skewness"] = dataclasses.I3Double(skew(frame["SLOPTuples_RelV_Launches"]))
    
    if frame.Has("SLOPTuples_RelV_Launches"): # new!!!
        frame["BDT_Invvel_kurtosis"] = dataclasses.I3Double(kurtosis(frame["SLOPTuples_RelV_Launches"]))
    #innerangle
    if frame.Has("SLOPTuples_CosAlpha_Launches"):
        frame["BDT_Innerangle_mean"] = dataclasses.I3Double(np.mean(frame["SLOPTuples_CosAlpha_Launches"]))

    if frame.Has("SLOPTuples_CosAlpha_Launches"):
        frame["BDT_Innerangle_min"] = dataclasses.I3Double(np.min(frame["SLOPTuples_CosAlpha_Launches"]))

    if frame.Has("SLOPTuples_CosAlpha_Launches"):
        frame["BDT_Innerangle_max"] = dataclasses.I3Double(np.max(frame["SLOPTuples_CosAlpha_Launches"]))

    if frame.Has("SLOPTuples_CosAlpha_Launches"):
        frame["BDT_Innerangle_var"] = dataclasses.I3Double(np.var(frame["SLOPTuples_CosAlpha_Launches"]))

    if frame.Has("SLOPTuples_CosAlpha_Launches"): # new!!!
        frame["BDT_Innerangle_90per"] = dataclasses.I3Double(np.percentile(frame["SLOPTuples_CosAlpha_Launches"],90))

    if frame.Has("SLOPTuples_CosAlpha_Launches"): # new!!!
        frame["BDT_Innerangle_10per"] = dataclasses.I3Double(np.percentile(frame["SLOPTuples_CosAlpha_Launches"],10))

    if frame.Has("SLOPTuples_CosAlpha_Launches"): # new!!!
        frame["BDT_Innerangle_75per"] = dataclasses.I3Double(np.percentile(frame["SLOPTuples_CosAlpha_Launches"],75))

    if frame.Has("SLOPTuples_CosAlpha_Launches"): # new!!!
        frame["BDT_Innerangle_25per"] = dataclasses.I3Double(np.percentile(frame["SLOPTuples_CosAlpha_Launches"],25))

    if frame.Has("SLOPTuples_CosAlpha_Launches"): # new!!!
        frame["BDT_Innerangle_median"] = dataclasses.I3Double(np.median(frame["SLOPTuples_CosAlpha_Launches"]))
    
    if frame.Has("SLOPTuples_CosAlpha_Launches"): # new!!!
        frame["BDT_Innerangle_skewness"] = dataclasses.I3Double(skew(frame["SLOPTuples_CosAlpha_Launches"]))
    
    if frame.Has("SLOPTuples_CosAlpha_Launches"): # new!!!
        frame["BDT_Innerangle_kurtosis"] = dataclasses.I3Double(kurtosis(frame["SLOPTuples_CosAlpha_Launches"]))
    ## Q_tot
    # frame["All_Q_frames"] = dataclasses.I3Double(len(all1))
    if frame.Has("SLOPPulseMask"):
        Map = frame["SLOPPulseMask"].apply(frame)
        Q_tot = 0.
        for OMKey, PulseVector in Map:
            for Pulse in PulseVector:
                Q_tot += Pulse.charge
        frame["BDT_Qtot"] = dataclasses.I3Double(Q_tot)


    ## NChannel
    if frame.Has("SLOPKalman_Map"):

        Map = frame["SLOPKalman_Map"].apply(frame)
        frame["BDT_NChannel"] = dataclasses.I3Double(len(Map))

    if frame.Has("I3MCTree"):
        tree = frame["I3MCTree"]
        primary = tree.get_primaries()[0]
        primary_position = primary.pos
        primary_direction = primary.dir
        dist = ((primary.pos).cross(primary.dir)).magnitude
        Intersect = Cylinder(1000.0, 550, dataclasses.I3Position(0,0,0)).intersection(primary_position,primary_direction)
        frame["CylinderIntersection"] = dataclasses.I3VectorDouble([Intersect.first, Intersect.second])
        frame["DistToCenter"] = dataclasses.I3Double(dist)

    if frame.Has("I3MCPESeriesMap"):
        n_doms = len(frame["I3MCPESeriesMap"])
        n_strings = len(np.unique([omkey.string for omkey, _ in frame["I3MCPESeriesMap"]]))
        npe = sum([pulse.npe for _, pulselist in frame["I3MCPESeriesMap"] for pulse in pulselist])
        frame["Number_PE"] = dataclasses.I3Double(npe)
        frame["Number_doms"] = dataclasses.I3Double(n_doms)
