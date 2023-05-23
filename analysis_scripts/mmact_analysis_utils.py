from icecube import dataclasses, icetray
from icecube.icetray import I3Units
from icecube.dataclasses import I3MCTree, I3Particle
import numpy as np







use_exprm_yrs = np.linspace(1,8,8)

levs         = ["gen","trigg","ehefilt","L2","L3","L4","L5","L6"]
levs_stepii  = ["L5","L6"]
levs_prevlev = { Lhi: Llo for Lhi,Llo in zip(levs[1:],levs[:-1]) }

use_gennum  = [ "mpsim_00002", "nugen_00001", "nugen_00002", "nugen_11070", "nugen_11297", ]
use_gennum += [ "exprm_860{:02}".format(int(yr)) for yr in use_exprm_yrs ]

gens = [ "mpsim", "nugen", "exprm", ]
nums = { gen: [ gn.split("_")[-1] for gn in use_gennum if gen in gn ] for gen in gens }

flavs = { "mpsim": { "00002": [ "monopole",             ], },   # ABurgman
	      "nugen": { "00001": [ "nue", "numu", "nutau", ],      # Nancy
                     "00002": [ "nue", "numu", "nutau", ],
                     "11070": [        "numu",          ],      # Central Production
                     "11297": [                "nutau", ], }, }
flavs["exprm"] =   { "860{:02}".format(int(yr)): [ "unknown", ] for yr in use_exprm_yrs } # Experimental

flavs_all = [ "monopole", "nue", "numu", "nutau", "unknown" ]
gennum_flavs = { "monopole": [("mpsim","00002"),],
                 "nue":      [("nugen","00001"),("nugen","00002"),],
                 "numu":     [("nugen","00001"),("nugen","00002"),("nugen","11070"),],
                 "nutau":    [("nugen","00001"),("nugen","00002"),("nugen","11297"),],
                 "unknown":  [("exprm","860{:02}".format(int(yr))) for yr in use_exprm_yrs], }

gennumflavs  = [("mpsim","00002","monopole"                     ),
	            ("nugen","00001",           "nue"               ),
	            ("nugen","00001",                 "numu"        ),
	            ("nugen","00001",                        "nutau"),
                ("nugen","00002",           "nue"               ),
                ("nugen","00002",                 "numu"        ),
                ("nugen","00002",                        "nutau"),
                ("nugen","11070",                 "numu"        ),
                ("nugen","11297",                        "nutau"),]
gennumflavs += [("exprm","860{:02}".format(int(yr)),"unknown") for yr in use_exprm_yrs ]



default_settings = { #"n_events": 1000,
                     #"icemodel": "$I3_BUILD/ppc/resources/ice/",
                     "gcd":      "/data/sim/sim-new/downloads/GCD/GeoCalibDetectorStatus_2016.57531_V0.i3.gz", }


# DATA SAMPLE DETAILS

gcdfile = { "mpsim": { "00002": default_settings["gcd"], },
            "nugen": { "00001": "/data/sim/sim-new/downloads/GCD/GeoCalibDetectorStatus_2016.57531_V0.i3.gz",
                       "00002": "/data/sim/sim-new/downloads/GCD/GeoCalibDetectorStatus_2016.57531_V0.i3.gz",
                       "11070": "/data/sim/sim-new/downloads/GCD/GeoCalibDetectorStatus_2012.56063_V1.i3.gz",
                       "11297": "/data/sim/sim-new/downloads/GCD/GeoCalibDetectorStatus_2012.56063_V1.i3.gz", }, }
gcdfile["exprm"] =   { "860{:02}".format(int(yr)): "" for yr in use_exprm_yrs }

mmactdir = "/data/user/hhamdaoui/MC_nuclearites/"

physicsstream = { "mpsim": { "00002": "SLOPSplit", }, #InIceSplit
                  "nugen": { "00001": "InIceSplit",
                             "00002": "InIceSplit",
                             "11070": "InIceSplit",
                             "11297": "InIceSplit", },
                  "exprm": { "86{}{:02}".format(str(physburn),int(yr)): "SLOPSplit" for yr in np.linspace(1,10,10) for physburn in [0,9] }, }

datadir = { "mpsim": { "00002": mmactdir, },
            "nugen": { "00001": "/data/ana/Cscd/StartingEvents/NuGen_new/",
                       "00002": "/data/ana/Cscd/StartingEvents/NuGen_new/",
                       "11070": "/data/sim/IceCube/2012/filtered/level2/neutrino-generator/11070/",
                       "11297": "/data/sim/IceCube/2012/filtered/level2/neutrino-generator/11297/",           }, }

outsubdir = { "gen":     "/ANA0_gen/",
              "trigg":   "/ANA1_L0_trigg/",
              "ehefilt": "/ANA2_L2_ehefilt/",
              "L2":      "/ANA3_L2_anacut/",
              "L3":      "/ANA4_L3_atmnucut/",
              "L4":      "/ANA5_L4_atmmucut/",
              "L5":      "/ANA6_L5_itveto/",
              "L6":      "/ANA7_L6_astnucut/", }

mergedfilesdir = mmactdir + "/00_merged_files_analysis/"

bdtdir    =             mmactdir + "/BDT_stuff/BDTE/"
bdtsubdir = { "data":   bdtdir   + "/data/",
              "output": bdtdir   + "/output/", }
bdtefrozen191113 = bdtdir + "/../BDTE_frozen_191113.bdt"
bdtefrozen191113_cutval = 0.037
bdtefrozen191218 = bdtdir + "/../BDTE_frozen_191218.bdt"
bdtefrozen191218_cutval = 0.047

outdatadir        = { lev: mmactdir + "/{}".format(subd) for lev,subd in outsubdir.items() }
outdatadir_lunger = { lev: "/data/user/lunger/aburgman_TEMP_{}/".format(osd.replace("/","").split("_")[0]) for lev,osd in outsubdir.items() }

plotdir = { "syssanchk": mmactdir + "/mmact_plots_systematics_sanity_check/",
            "syshist1d": mmactdir + "/mmact_plots_systematics_hist1d/",
            "syshist2d": mmactdir + "/mmact_plots_systematics_hist2d/",
            "sysmisc":   mmactdir + "/mmact_plots_systematics_misc/",
            "hist1d":    mmactdir + "/mmact_plots_analysis_hist1d/",
            "hist2d":    mmactdir + "/mmact_plots_analysis_hist2d/",
            "misc":      mmactdir + "/mmact_plots_analysis_misc/",
            "thesis":    mmactdir + "/mmact_plots_thesis/", }

outputdir = {   "misc": mmactdir + "/mmact_output_analysis_misc/",
              "thesis": mmactdir + "/mmact_output_thesis/", }

photosplines = {
	"i3data": "$I3_DATA/photon-tables/splines/",
	"dir":    "/cvmfs/icecube.opensciencegrid.org/py2-v2/../data/photon-tables/splines/",
	"files": {
		"cascade": {
			"abs":  "/cvmfs/icecube.opensciencegrid.org/py2-v2/../data/photon-tables/splines/cascades_clsim_mie_z20_a10.abs.fits",
			"prob": "/cvmfs/icecube.opensciencegrid.org/py2-v2/../data/photon-tables/splines/cascades_clsim_mie_z20_a10.prob.fits"
		},
		"muon": {
			"abs":  "/cvmfs/icecube.opensciencegrid.org/py2-v2/../data/photon-tables/splines/InfBareMu_mie_abs_z20a10_V2.fits",
			"prob": "/cvmfs/icecube.opensciencegrid.org/py2-v2/../data/photon-tables/splines/InfBareMu_mie_prob_z20a10_V2.fits"
		},
	},
}


# SYSTEMATICS SETTINGS

supported_systematics = [
  "baseline"            ,
  "domeff_plus"         , "domeff_minus"        ,
  "scat_plus_abs_plus"  , "scat_plus_abs_minus" , "scat_minus_abs_plus" , "scat_minus_abs_minus",
  "angsens_set05"       , "angsens_set09"       , "angsens_set10"       , "angsens_set14"       ,
                                                  "p1_0.20_p2_0"        ,
  "p1_0.25_p2_-3"       , "p1_0.25_p2_-1"       , "p1_0.25_p2_0"        , "p1_0.25_p2_+1"       ,
  "p1_0.30_p2_-3"       , "p1_0.30_p2_-1"       , "p1_0.30_p2_0"        , "p1_0.30_p2_+1"       ,
                                                  "p1_0.35_p2_0"        ,
  ]

supp_syst_gen = { "mpsim": [sk for sk in supported_systematics if "p1" not in sk], "nugen": ["baseline"], "exprm": ["baseline"] }

def exprm_lev_exists(l,n):
	if l in ["ehefilt","L2","L3","L4"]:
		return True
	elif n[-2:] in ["04","06","08"] and l in ["L5","L6"]:
		return True
	return False

datafilenames = { gen: { num: { lev: { flav: { syst:
	mergedfilesdir+"mmact_data__{}_{}__{}_{}__{}.hd5".format(gen,num,flav,lev,syst)
	for syst in supp_syst_gen[gen] } for flav in flavs[gen][num] } for lev in outsubdir.keys() } for num in nums[gen] } for gen in gens if gen!="exprm" }
datafilenames["exprm"] = { num: { lev: { flav: { "baseline": mergedfilesdir+"mmact_data__exprm_{}__{}_{}__phys.hd5".format(num,flav,lev) } for flav in flavs["exprm"][num] } for lev in outsubdir.keys() if exprm_lev_exists(lev,num) } for num in nums["exprm"] }


# __nutau__medium_energy__ <-- nancy's

syst_labels = {
	"baseline"            : "Baseline"              ,
	"domeff_plus"         : "DOM Efficiency +10 %"  ,
	"domeff_minus"        : "DOM Efficiency -10 %"  ,
	"scat_plus_abs_plus"  : "Scat. +5 %, Abs. +5 %" ,
	"scat_plus_abs_minus" : "Scat. +5 %, Abs. -5 %" ,
	"scat_minus_abs_plus" : "Scat. -5 %, Abs. +5 %" ,
	"scat_minus_abs_minus": "Scat. -5 %, Abs. -5 %" ,
	"angsens_set05"       : "Ang. Sens. set 5"      ,
	"angsens_set09"       : "Ang. Sens. set 9"      ,
	"angsens_set10"       : "Ang. Sens. set 10"     ,
	"angsens_set14"       : "Ang. Sens. set 14"     ,
	"p1_0.20_p2_0"        : "$p_1=0.20$, $p_2=0$"   ,
	"p1_0.25_p2_-3"       : "$p_1=0.25$, $p_2=-3$"  ,
	"p1_0.25_p2_-1"       : "$p_1=0.25$, $p_2=-1$"  ,
	"p1_0.25_p2_0"        : "$p_1=0.25$, $p_2=0$"   ,
	"p1_0.25_p2_+1"       : "$p_1=0.25$, $p_2=1$"   ,
	"p1_0.30_p2_-3"       : "$p_1=0.30$, $p_2=-3$"  ,
	"p1_0.30_p2_-1"       : "$p_1=0.30$, $p_2=-1$"  ,
	"p1_0.30_p2_0"        : "$p_1=0.30$, $p_2=0$"   ,
	"p1_0.30_p2_+1"       : "$p_1=0.30$, $p_2=1$"   ,
	"p1_0.35_p2_0"        : "$p_1=0.35$, $p_2=0$"   ,
	}

syst_colors = {
	"baseline"            : "black"         ,
	"domeff_plus"         : "orchid"        ,
	"domeff_minus"        : "orange"        ,
	"scat_plus_abs_plus"  : "orchid"        ,
	"scat_plus_abs_minus" : "darkturquoise" ,
	"scat_minus_abs_plus" : "green"         ,
	"scat_minus_abs_minus": "orange"        ,
	"angsens_set05"       : "orchid"        ,
	"angsens_set09"       : "darkturquoise" ,
	"angsens_set10"       : "green"         ,
	"angsens_set14"       : "orange"        ,
	"p1_0.20_p2_0"        : "orange"        ,
	"p1_0.25_p2_-3"       : "firebrick"     ,
	"p1_0.25_p2_-1"       : "crimson"       ,
	"p1_0.25_p2_0"        : "orchid"        ,
	"p1_0.25_p2_+1"       : "mediumpurple"  ,
	"p1_0.30_p2_-3"       : "blue"          ,
	"p1_0.30_p2_-1"       : "darkturquoise" ,
	"p1_0.30_p2_0"        : "mediumseagreen",
	"p1_0.30_p2_+1"       : "green"         ,
	"p1_0.35_p2_0"        : "olivedrab"     ,
	}

syst_order = {
	"baseline"            : "syst_z" ,
	"domeff_plus"         : "syst_a" ,
	"domeff_minus"        : "syst_b" ,
	"scat_plus_abs_plus"  : "syst_e" ,
	"scat_plus_abs_minus" : "syst_f" ,
	"scat_minus_abs_plus" : "syst_g" ,
	"scat_minus_abs_minus": "syst_h" ,
	"angsens_set05"       : "syst_i" ,
	"angsens_set09"       : "syst_j" ,
	"angsens_set10"       : "syst_k" ,
	"angsens_set14"       : "syst_l" ,
	"p1_0.20_p2_0"        : "syst_m" ,
	"p1_0.25_p2_-3"       : "syst_n" ,
	"p1_0.25_p2_-1"       : "syst_o" ,
	"p1_0.25_p2_0"        : "syst_p" ,
	"p1_0.25_p2_+1"       : "syst_q" ,
	"p1_0.30_p2_-3"       : "syst_r" ,
	"p1_0.30_p2_-1"       : "syst_s" ,
	"p1_0.30_p2_0"        : "syst_t" ,
	"p1_0.30_p2_+1"       : "syst_u" ,
	"p1_0.35_p2_0"        : "syst_v" ,
	}


# SANITY CHECK SETTINGS

syst_cat_key = { "domeff":  "domeff_", "scatabs": "scat_", "holeice": "p1_", "angsens": "angsens_", }

syst_categories = { sc: [ "baseline" ] + [ sk for sk in supported_systematics if sck in sk ] for sc,sck in syst_cat_key.items() }

syst_cols_cats = {
	"domeff":  [ "black", "orchid", "orange", ],
	"scatabs": [ "black", "orchid", "darkturquoise", "green", "orange", ],
	"angsens": [ "black", "orchid", "darkturquoise", "green", "orange", ],
	"holeice": [ "black", "orange", "firebrick", "crimson", "orchid", "mediumpurple", "blue", "darkturquoise", "mediumseagreen", "green", "olivedrab", ],
	}

icwip_pos  = { "log10qtot": "ul", "log10npe": "ul", "log10nch": "ul", "fitqual": "ur", "coszen": "ul", "mcbetatrigger": "ur", "mcbetafilter": "ur", "mcbeta": "ur", }
data_title = { "log10qtot": "$\\mathrm{log}_{10}(q_{tot})$", "log10npe": "$\\mathrm{log}_{10}(n_{pe})$", "log10nch": "$\\mathrm{log}_{10}(n_{ch})$", "fitqual": "$\\chi^2_{\\mathrm{LF}}$", "coszen": "$\\mathrm{cos}(zen)$", "mcbetatrigger": "$\\beta_{\\mathrm{MC},triggered}$", "mcbetafilter": "$\\beta_{\\mathrm{MC},EHE-filtered}$", "mcbeta": "$\\beta_{\\mathrm{MC}}$", }

sanchk_range_x = { "log10qtot": [2.,6.], "log10npe": [2.,6.], "log10nch": [1.,4.], "fitqual": [0.,300.], "coszen": [-1.,1.], "mcbeta": [0.75,1.], }
sanchk_nbin = 40






datakeys = {}
datakeys["gen"] = []
datakeys["trigg"] = [dk for dk in datakeys["gen"]] + [
	"mccoszen"     , "mcazi"        , "mcbeta"       , "mclog10energy", 
	"mccentrality" , "mcgeomlength" , "mcgeomtime"   , 
	"wtcount",
	"wtonenumudif2017central"                          , "wtonenumudif2017plussigma"                          , "wtonenumudif2017minussigma"                          ,
	"wtoverlapnumudif2017central_nancymedium_nancyhigh", "wtoverlapnumudif2017plussigma_nancymedium_nancyhigh", "wtoverlapnumudif2017minussigma_nancymedium_nancyhigh",
	"wtoverlapnumudif2017central_nancyhigh_iceprodhigh", "wtoverlapnumudif2017plussigma_nancyhigh_iceprodhigh", "wtoverlapnumudif2017minussigma_nancyhigh_iceprodhigh",
	"wtonenumudif2019central"                          , "wtonenumudif2019plussigma"                          , "wtonenumudif2019minussigma"                          ,
	"wtoverlapnumudif2019central_nancymedium_nancyhigh", "wtoverlapnumudif2019plussigma_nancymedium_nancyhigh", "wtoverlapnumudif2019minussigma_nancymedium_nancyhigh",
	"wtoverlapnumudif2019central_nancyhigh_iceprodhigh", "wtoverlapnumudif2019plussigma_nancyhigh_iceprodhigh", "wtoverlapnumudif2019minussigma_nancyhigh_iceprodhigh",
	"wtonehese2019central"                             , "wtonehese2019plussigma"                             , "wtonehese2019minussigma"                             ,
	"wtoverlaphese2019central_nancymedium_nancyhigh"   , "wtoverlaphese2019plussigma_nancymedium_nancyhigh"   , "wtoverlaphese2019minussigma_nancymedium_nancyhigh"   ,
	"wtoverlaphese2019central_nancyhigh_iceprodhigh"   , "wtoverlaphese2019plussigma_nancyhigh_iceprodhigh"   , "wtoverlaphese2019minussigma_nancyhigh_iceprodhigh"   ,
	"genmpsim", "gennugen", "genexprm",
	"num00000", "num00001", "num00002", "num11070", "num11297",
	]
datakeys["ehefilt"] = [dk for dk in datakeys["trigg"]] + [
	"ptlog10npe"  , "ptnch"       , "ptrhope"     , 
	"opcoszen"    , "opazi"       , "opbeta"      , 
	"opfitquality", "opcentrality", "Slop passedopgeomlength", "opgeomtime"  , 
	"bdtseparator", "bdtistrain"  , "bdtistest"   , 
	]
datakeys["L2"] = [dk for dk in datakeys["ehefilt"]]
datakeys["L3"] = [dk for dk in datakeys["L2"]]
datakeys["L4"] = [dk for dk in datakeys["L3"]]
datakeys["L5"] = [dk for dk in datakeys["L4"]] + [
	"bmcoszen"                , "bmazi"                   , "bmbeta"                  ,
	"bmcentrality"            , "bmgeomlength"            , "bmgeomtime"              ,
	"cvhiscog"                , "cvtictimefwhm"           , "cvtictimetot"            ,
	"cvtrclength"             , "cvtrcsmoothness"         , "cvtrcavgdistq"           ,
	"mpavge"                  , "mpstde"                  , "mprsde"                  ,
	"mcopbetadiff"            , "mcbmbetadiff"            ,
	"bmcvtrclengthfillratio"  , "bmcvtictimefwhmfillratio",
	"bmcvtictimetotfillratio" , "bmcvhisrelativecogoffset",
	"bdtescore",
	]
datakeys["L6"] = [dk for dk in datakeys["L5"]]

datakeys_exprm = {}
datakeys_exprm["mpsim"] = [  ]
datakeys_exprm["nugen"] = [  ]
datakeys_exprm["exprm"] = [
	"utcstartyear"      , "utcstartmonth"     , "utcstartdayofmonth", "utcstartsecond"    , "utcstartnanosecond",
	"utcendyear"        , "utcendmonth"       , "utcenddayofmonth"  , "utcendsecond"      , "utcendnanosecond"  ,
	"fhseason"          , "fhrunid"           , "fheventid"         ,
	]

keys_L6={}
# Splitting the long strings below with the "," delimiter
keys_L6["baseline"] = "bdtistest,bdtistrain,bdtseparator,bmazi,bmbeta,bmcentrality,bmcoszen,bmcvhisrelativecogoffset,bmcvtictimefwhmfillratio,bmcvtictimetotfillratio,bmcvtrclengthfillratio,bmgeomlength,bmgeomtime,cvhiscog,cvtictimefwhm,cvtictimetot,cvtrcavgdistq,cvtrclength,cvtrcsmoothness,genexprm,genmpsim,gennugen,mcazi,mcbeta,mcbmbetadiff,mccentrality,mccoszen,mcgeomlength,mcgeomtime,mclog10energy,mcopbetadiff,mpavge,mprsde,mpstde,num00000,num00001,num00002,num11070,num11297,opazi,opbeta,opcentrality,opcoszen,opfitquality,opgeomlength,opgeomtime,ptlog10npe,ptnch,ptrhope,wtcount,wtonehese2019central,wtonehese2019minussigma,wtonehese2019plussigma,wtonenumudif2017central,wtonenumudif2017minussigma,wtonenumudif2017plussigma,wtonenumudif2019central,wtonenumudif2019minussigma,wtonenumudif2019plussigma,wtoverlaphese2019central_nancyhigh_iceprodhigh,wtoverlaphese2019central_nancymedium_nancyhigh,wtoverlaphese2019minussigma_nancyhigh_iceprodhigh,wtoverlaphese2019minussigma_nancymedium_nancyhigh,wtoverlaphese2019plussigma_nancyhigh_iceprodhigh,wtoverlaphese2019plussigma_nancymedium_nancyhigh,wtoverlapnumudif2017central_nancyhigh_iceprodhigh,wtoverlapnumudif2017central_nancymedium_nancyhigh,wtoverlapnumudif2017minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017minussigma_nancymedium_nancyhigh,wtoverlapnumudif2017plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017plussigma_nancymedium_nancyhigh,wtoverlapnumudif2019central_nancyhigh_iceprodhigh,wtoverlapnumudif2019central_nancymedium_nancyhigh,wtoverlapnumudif2019minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019minussigma_nancymedium_nancyhigh,wtoverlapnumudif2019plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019plussigma_nancymedium_nancyhigh".split(",")
keys_L6["domeff"]   = "bdtistest,bdtistrain,bdtseparator,bmazi,bmbeta,bmcentrality,bmcoszen,bmcvhisrelativecogoffset,bmcvtictimefwhmfillratio,bmcvtictimetotfillratio,bmcvtrclengthfillratio,bmgeomlength,bmgeomtime,cvhiscog,cvtictimefwhm,cvtictimetot,cvtrcavgdistq,cvtrclength,cvtrcsmoothness,genexprm,genmpsim,gennugen,mcazi,mcbeta,mcbmbetadiff,mccentrality,mccoszen,mcgeomlength,mcgeomtime,mclog10energy,mcopbetadiff,mpavge,mprsde,mpstde,num00000,num00001,num00002,num11070,num11297,opazi,opbeta,opcentrality,opcoszen,opfitquality,opgeomlength,opgeomtime,ptlog10npe,ptnch,ptrhope,wtcount,wtonehese2019central,wtonehese2019minussigma,wtonehese2019plussigma,wtonenumudif2017central,wtonenumudif2017minussigma,wtonenumudif2017plussigma,wtonenumudif2019central,wtonenumudif2019minussigma,wtonenumudif2019plussigma,wtoverlaphese2019central_nancyhigh_iceprodhigh,wtoverlaphese2019central_nancymedium_nancyhigh,wtoverlaphese2019minussigma_nancyhigh_iceprodhigh,wtoverlaphese2019minussigma_nancymedium_nancyhigh,wtoverlaphese2019plussigma_nancyhigh_iceprodhigh,wtoverlaphese2019plussigma_nancymedium_nancyhigh,wtoverlapnumudif2017central_nancyhigh_iceprodhigh,wtoverlapnumudif2017central_nancymedium_nancyhigh,wtoverlapnumudif2017minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017minussigma_nancymedium_nancyhigh,wtoverlapnumudif2017plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017plussigma_nancymedium_nancyhigh,wtoverlapnumudif2019central_nancyhigh_iceprodhigh,wtoverlapnumudif2019central_nancymedium_nancyhigh,wtoverlapnumudif2019minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019minussigma_nancymedium_nancyhigh,wtoverlapnumudif2019plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019plussigma_nancymedium_nancyhigh".split(",")
keys_L6["scatabs"]  = "bdtistest,bdtistrain,bdtseparator,bmazi,bmbeta,bmcentrality,bmcoszen,bmcvhisrelativecogoffset,bmcvtictimefwhmfillratio,bmcvtictimetotfillratio,bmcvtrclengthfillratio,bmgeomlength,bmgeomtime,cvhiscog,cvtictimefwhm,cvtictimetot,cvtrcavgdistq,cvtrclength,cvtrcsmoothness,genexprm,genmpsim,gennugen,mcazi,mcbeta,mcbmbetadiff,mccentrality,mccoszen,mcgeomlength,mcgeomtime,mclog10energy,mcopbetadiff,mpavge,mprsde,mpstde,num00000,num00001,num00002,num11070,num11297,opazi,opbeta,opcentrality,opcoszen,opfitquality,opgeomlength,opgeomtime,ptlog10npe,ptnch,ptrhope,wtcount,wtonehese2019central,wtonehese2019minussigma,wtonehese2019plussigma,wtonenumudif2017central,wtonenumudif2017minussigma,wtonenumudif2017plussigma,wtonenumudif2019central,wtonenumudif2019minussigma,wtonenumudif2019plussigma,wtoverlaphese2019central_nancyhigh_iceprodhigh,wtoverlaphese2019central_nancymedium_nancyhigh,wtoverlaphese2019minussigma_nancyhigh_iceprodhigh,wtoverlaphese2019minussigma_nancymedium_nancyhigh,wtoverlaphese2019plussigma_nancyhigh_iceprodhigh,wtoverlaphese2019plussigma_nancymedium_nancyhigh,wtoverlapnumudif2017central_nancyhigh_iceprodhigh,wtoverlapnumudif2017central_nancymedium_nancyhigh,wtoverlapnumudif2017minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017minussigma_nancymedium_nancyhigh,wtoverlapnumudif2017plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017plussigma_nancymedium_nancyhigh,wtoverlapnumudif2019central_nancyhigh_iceprodhigh,wtoverlapnumudif2019central_nancymedium_nancyhigh,wtoverlapnumudif2019minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019minussigma_nancymedium_nancyhigh,wtoverlapnumudif2019plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019plussigma_nancymedium_nancyhigh".split(",")
keys_L6["angsens"]  = "bdtistest,bdtistrain,bdtseparator,bmazi,bmbeta,bmcentrality,bmcoszen,bmcvhisrelativecogoffset,bmcvtictimefwhmfillratio,bmcvtictimetotfillratio,bmcvtrclengthfillratio,bmgeomlength,bmgeomtime,cvhiscog,cvtictimefwhm,cvtictimetot,cvtrcavgdistq,cvtrclength,cvtrcsmoothness,fheventid,fhrunid,fhseason,genexprm,genmpsim,gennugen,mcazi,mcbeta,mcbmbetadiff,mccentrality,mccoszen,mcgeomlength,mcgeomtime,mclog10energy,mcopbetadiff,mpavge,mprsde,mpstde,num00000,num00001,num00002,num11070,num11297,num86001,num86002,num86003,num86004,num86005,num86006,num86007,num86008,num86009,num86010,num86901,num86902,num86903,num86904,num86905,num86906,num86907,num86908,num86909,num86910,opazi,opbeta,opcoszen,opfitquality,ptlog10npe,ptnch,ptrhope,utcenddayofmonth,utcendmonth,utcendnanosecond,utcendsecond,utcendyear,utcstartdayofmonth,utcstartmonth,utcstartnanosecond,utcstartsecond,utcstartyear,wtcount,wtonehese2019central,wtonehese2019minussigma,wtonehese2019plussigma,wtonenumudif2017central,wtonenumudif2017minussigma,wtonenumudif2017plussigma,wtonenumudif2019central,wtonenumudif2019minussigma,wtonenumudif2019plussigma,wtoverlaphese2019central_nancyhigh_iceprodhigh,wtoverlaphese2019central_nancymedium_nancyhigh,wtoverlaphese2019minussigma_nancyhigh_iceprodhigh,wtoverlaphese2019minussigma_nancymedium_nancyhigh,wtoverlaphese2019plussigma_nancyhigh_iceprodhigh,wtoverlaphese2019plussigma_nancymedium_nancyhigh,wtoverlapnumudif2017central_nancyhigh_iceprodhigh,wtoverlapnumudif2017central_nancymedium_nancyhigh,wtoverlapnumudif2017minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017minussigma_nancymedium_nancyhigh,wtoverlapnumudif2017plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017plussigma_nancymedium_nancyhigh,wtoverlapnumudif2019central_nancyhigh_iceprodhigh,wtoverlapnumudif2019central_nancymedium_nancyhigh,wtoverlapnumudif2019minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019minussigma_nancymedium_nancyhigh,wtoverlapnumudif2019plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019plussigma_nancymedium_nancyhigh".split(",")
datakeysexcluded_syst = { "baseline"            : [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["baseline"] ],
                         "domeff_plus"         : [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["domeff"]   ],
                         "domeff_minus"        : [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["domeff"]   ],
                         "scat_plus_abs_plus"  : [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["scatabs"]  ],
                         "scat_plus_abs_minus" : [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["scatabs"]  ],
                         "scat_minus_abs_plus" : [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["scatabs"]  ],
                         "scat_minus_abs_minus": [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["scatabs"]  ],
                         "angsens_set05"       : [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["angsens"]  ],
                         "angsens_set09"       : [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["angsens"]  ],
                         "angsens_set10"       : [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["angsens"]  ],
                         "angsens_set14"       : [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["angsens"]  ], }
keys_L6["mpsim"] = "bdtistest,bdtistrain,bdtseparator,bmazi,bmbeta,bmcentrality,bmcoszen,bmcvhisrelativecogoffset,bmcvtictimefwhmfillratio,bmcvtictimetotfillratio,bmcvtrclengthfillratio,bmgeomlength,bmgeomtime,cvhiscog,cvtictimefwhm,cvtictimetot,cvtrcavgdistq,cvtrclength,cvtrcsmoothness,genexprm,genmpsim,gennugen,mcazi,mcbeta,mcbmbetadiff,mccentrality,mccoszen,mcgeomlength,mcgeomtime,mclog10energy,mcopbetadiff,mpavge,mprsde,mpstde,num00000,num00001,num00002,num11070,num11297,opazi,opbeta,opcentrality,opcoszen,opfitquality,opgeomlength,opgeomtime,ptlog10npe,ptnch,ptrhope,wtcount,wtonehese2019central,wtonehese2019minussigma,wtonehese2019plussigma,wtonenumudif2017central,wtonenumudif2017minussigma,wtonenumudif2017plussigma,wtonenumudif2019central,wtonenumudif2019minussigma,wtonenumudif2019plussigma,wtoverlaphese2019central_nancyhigh_iceprodhigh,wtoverlaphese2019central_nancymedium_nancyhigh,wtoverlaphese2019minussigma_nancyhigh_iceprodhigh,wtoverlaphese2019minussigma_nancymedium_nancyhigh,wtoverlaphese2019plussigma_nancyhigh_iceprodhigh,wtoverlaphese2019plussigma_nancymedium_nancyhigh,wtoverlapnumudif2017central_nancyhigh_iceprodhigh,wtoverlapnumudif2017central_nancymedium_nancyhigh,wtoverlapnumudif2017minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017minussigma_nancymedium_nancyhigh,wtoverlapnumudif2017plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017plussigma_nancymedium_nancyhigh,wtoverlapnumudif2019central_nancyhigh_iceprodhigh,wtoverlapnumudif2019central_nancymedium_nancyhigh,wtoverlapnumudif2019minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019minussigma_nancymedium_nancyhigh,wtoverlapnumudif2019plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019plussigma_nancymedium_nancyhigh".split(",")
keys_L6["nugen"] = "bdtistest,bdtistrain,bdtseparator,bmazi,bmbeta,bmcentrality,bmcoszen,bmcvhisrelativecogoffset,bmcvtictimefwhmfillratio,bmcvtictimetotfillratio,bmcvtrclengthfillratio,bmgeomlength,bmgeomtime,cvhiscog,cvtictimefwhm,cvtictimetot,cvtrcavgdistq,cvtrclength,cvtrcsmoothness,genexprm,genmpsim,gennugen,mcazi,mcbeta,mcbmbetadiff,mccentrality,mccoszen,mcgeomlength,mcgeomtime,mclog10energy,mcopbetadiff,mpavge,mprsde,mpstde,num00000,num00001,num00002,num11070,num11297,opazi,opbeta,opcentrality,opcoszen,opfitquality,opgeomlength,opgeomtime,ptlog10npe,ptnch,ptrhope,wtcount,wtonehese2019central,wtonehese2019minussigma,wtonehese2019plussigma,wtonenumudif2017central,wtonenumudif2017minussigma,wtonenumudif2017plussigma,wtonenumudif2019central,wtonenumudif2019minussigma,wtonenumudif2019plussigma,wtoverlaphese2019central_nancyhigh_iceprodhigh,wtoverlaphese2019central_nancymedium_nancyhigh,wtoverlaphese2019minussigma_nancyhigh_iceprodhigh,wtoverlaphese2019minussigma_nancymedium_nancyhigh,wtoverlaphese2019plussigma_nancyhigh_iceprodhigh,wtoverlaphese2019plussigma_nancymedium_nancyhigh,wtoverlapnumudif2017central_nancyhigh_iceprodhigh,wtoverlapnumudif2017central_nancymedium_nancyhigh,wtoverlapnumudif2017minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017minussigma_nancymedium_nancyhigh,wtoverlapnumudif2017plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2017plussigma_nancymedium_nancyhigh,wtoverlapnumudif2019central_nancyhigh_iceprodhigh,wtoverlapnumudif2019central_nancymedium_nancyhigh,wtoverlapnumudif2019minussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019minussigma_nancymedium_nancyhigh,wtoverlapnumudif2019plussigma_nancyhigh_iceprodhigh,wtoverlapnumudif2019plussigma_nancymedium_nancyhigh".split(",")
keys_L6["exprm"] = "bmazi,bmbeta,bmcentrality,bmcoszen,bmcvhisrelativecogoffset,bmcvtictimefwhmfillratio,bmcvtictimetotfillratio,bmcvtrclengthfillratio,bmgeomlength,bmgeomtime,cvhiscog,cvtictimefwhm,cvtictimetot,cvtrcavgdistq,cvtrclength,cvtrcsmoothness,fheventid,fhrunid,fhseason,genexprm,genmpsim,gennugen,mpavge,mprsde,mpstde,num00000,num00001,num00002,num11070,num11297,num86001,num86002,num86003,num86004,num86005,num86006,num86007,num86008,num86009,num86010,num86901,num86902,num86903,num86904,num86905,num86906,num86907,num86908,num86909,num86910,opazi,opbeta,opcoszen,opfitquality,ptlog10npe,ptnch,ptrhope,utcenddayofmonth,utcendmonth,utcendnanosecond,utcendsecond,utcendyear,utcstartdayofmonth,utcstartmonth,utcstartnanosecond,utcstartsecond,utcstartyear".split(",")
datakeysexcluded_gen = { "mpsim": [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["mpsim"] ],
                         "nugen": [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["nugen"] ],
                         "exprm": [ dk for dk in keys_L6["baseline"] if dk not in keys_L6["exprm"] ], } # FIX

#
#plotkeys       = [ dk for dk in datakeys["L6"] if not dk[:2]=="wt" ]



weightkeys_spectra = {
	"numudif2017_central"   : [ "wtcount", "wtistest", "wtonenumudif2017central"   , "wtoverlapnumudif2017central_nancymedium_nancyhigh"   , "wtoverlapnumudif2017central_nancyhigh_iceprodhigh"   , ],
	"numudif2017_plussigma" : [ "wtcount", "wtistest", "wtonenumudif2017plussigma" , "wtoverlapnumudif2017plussigma_nancymedium_nancyhigh" , "wtoverlapnumudif2017plussigma_nancyhigh_iceprodhigh" , ],
	"numudif2017_minussigma": [ "wtcount", "wtistest", "wtonenumudif2017minussigma", "wtoverlapnumudif2017minussigma_nancymedium_nancyhigh", "wtoverlapnumudif2017minussigma_nancyhigh_iceprodhigh", ],
	"numudif2019_central"   : [ "wtcount", "wtistest", "wtonenumudif2019central"   , "wtoverlapnumudif2019central_nancymedium_nancyhigh"   , "wtoverlapnumudif2019central_nancyhigh_iceprodhigh"   , ],
	"numudif2019_plussigma" : [ "wtcount", "wtistest", "wtonenumudif2019plussigma" , "wtoverlapnumudif2019plussigma_nancymedium_nancyhigh" , "wtoverlapnumudif2019plussigma_nancyhigh_iceprodhigh" , ],
	"numudif2019_minussigma": [ "wtcount", "wtistest", "wtonenumudif2019minussigma", "wtoverlapnumudif2019minussigma_nancymedium_nancyhigh", "wtoverlapnumudif2019minussigma_nancyhigh_iceprodhigh", ],
	"hese2019_central"      : [ "wtcount", "wtistest", "wtonehese2019central"      , "wtoverlaphese2019central_nancymedium_nancyhigh"      , "wtoverlaphese2019central_nancyhigh_iceprodhigh"      , ],
	"hese2019_plussigma"    : [ "wtcount", "wtistest", "wtonehese2019plussigma"    , "wtoverlaphese2019plussigma_nancymedium_nancyhigh"    , "wtoverlaphese2019plussigma_nancyhigh_iceprodhigh"    , ],
	"hese2019_minussigma"   : [ "wtcount", "wtistest", "wtonehese2019minussigma"   , "wtoverlaphese2019minussigma_nancymedium_nancyhigh"   , "wtoverlaphese2019minussigma_nancyhigh_iceprodhigh"   , ],
	}


weightkeys_baseline = [ wk for wk in weightkeys_spectra["numudif2017_central"] ]


spectra_gen = { "mpsim": ["numudif2017_central"], "nugen": sorted([sk for sk in weightkeys_spectra.keys()]) }


angsens_params = {
"set0"  : { "p0": -0.065  , "p1" : -0.11    , },
"set1"  : { "p0": -0.48   , "p1" : -0.017   , },
"set2"  : { "p0":  0.28   , "p1" : -0.075   , },
"set3"  : { "p0":  0.11   , "p1" :  0.0035  , },
"set4"  : { "p0": -0.05   , "p1" : -0.054   , },
"set5"  : { "p0": -0.37   , "p1" :  0.035   , },
"set6"  : { "p0":  0.3    , "p1" : -0.036   , },
"set7"  : { "p0":  0.12   , "p1" : -0.11    , },
"set8"  : { "p0": -0.036  , "p1" : -0.019   , },
"set9"  : { "p0": -0.31   , "p1" : -0.077   , },
"set10" : { "p0":  0.31   , "p1" :  0.0017  , },
"set11" : { "p0":  0.14   , "p1" : -0.056   , },
"set12" : { "p0": -0.022  , "p1" :  0.031   , },
"set13" : { "p0": -0.27   , "p1" : -0.038   , },
"set14" : { "p0":  0.33   , "p1" : -0.12    , },
"set15" : { "p0":  0.15   , "p1" : -0.02    , },
"set16" : { "p0": -0.008  , "p1" : -0.079   , },
"set17" : { "p0": -0.24   , "p1" : -0.00015 , },
"set18" : { "p0":  0.35   , "p1" : -0.057   , },
"set19" : { "p0":  0.16   , "p1" :  0.028   , },
"set20" : { "p0":  0.0053 , "p1" : -0.039   , },
"set21" : { "p0": -0.21   , "p1" : -0.12    , },
"set22" : { "p0":  0.37   , "p1" : -0.022   , },
"set23" : { "p0":  0.17   , "p1" : -0.082   , },
"set24" : { "p0":  0.018  , "p1" : -0.0019  , },
"set25" : { "p0": -0.19   , "p1" : -0.059   , },
"set26" : { "p0":  0.4    , "p1" :  0.025   , },
"set27" : { "p0":  0.19   , "p1" : -0.041   , },
"set28" : { "p0":  0.031  , "p1" : -0.13    , },
"set29" : { "p0": -0.16   , "p1" : -0.023   , },
"set30" : { "p0":  0.42   , "p1" : -0.084   , },
"set31" : { "p0":  0.2    , "p1" : -0.0036  , },
"set32" : { "p0":  0.044  , "p1" : -0.061   , },
"set33" : { "p0": -0.14   , "p1" :  0.022   , },
"set34" : { "p0":  0.45   , "p1" : -0.042   , },
"set35" : { "p0":  0.21   , "p1" : -0.14    , },
"set36" : { "p0":  0.056  , "p1" : -0.024   , },
"set37" : { "p0": -0.12   , "p1" : -0.086   , },
"set38" : { "p0":  0.49   , "p1" : -0.0053  , },
"set39" : { "p0":  0.23   , "p1" : -0.062   , },
"set40" : { "p0":  0.069  , "p1" :  0.02    , },
"set41" : { "p0": -0.11   , "p1" : -0.043   , },
"set42" : { "p0":  0.54   , "p1" : -0.17    , },
"set43" : { "p0":  0.24   , "p1" : -0.026   , },
"set44" : { "p0":  0.081  , "p1" : -0.088   , },
"set45" : { "p0": -0.089  , "p1" : -0.0069  , },
"set46" : { "p0":  0.61   , "p1" : -0.064   , },
"set47" : { "p0":  0.26   , "p1" :  0.017   , },
"set48" : { "p0":  0.093  , "p1" : -0.045   , },
"set49" : { "p0": -0.073  , "p1" :  0.085   , },
}
angsens_baseline = { "p0": 0.101569, "p1": -0.049344, }
angsens_use = [ "set5", "set9", "set10", "set14", ]
#angsens_range = { "p0": [-2.,1], "p1": [-0.2,0.2], }
angsens_range = { "p0": [-0.5,0.7], "p1": [-0.2,0.1], }



#
#import random, os, sys, json
#
#with open("config.json") as json_config_file:
#	configs = json.load(json_config_file)
#sys.path.insert(0, "/home/aburgman/icecube/00_library/")
#
#from funcs_custom import add_to_list_uniquely
##from funcs_custom import get_filenames_in_dir
#from statistics import *
#from plotting   import *
#from misc       import *
#
#
#dataset_flavors = { "mpsim_00000": ["monopole"],           "mpsim_00001": ["monopole"],           "juliet_12497": ["mu","tau","nue","numu","nutau"],
#                    "nugen_00000": ["nue","numu","nutau"], "nugen_00001": ["nue","numu","nutau"], "nugen_00002":  ["nue","numu","nutau"],          
#                                                           "nugen_11070": [      "numu"        ], "nugen_11297":  [             "nutau"],            }
#
#use_gennum = [ "mpsim_00001", "nugen_00001", "nugen_00002", "nugen_11070", "nugen_11297" ]
#
#conf_fn = configs["filename"]
#
#cats  = [ cat                                                                                                                                                                                                                                    for cat in conf_fn.keys() if "exp" not in cat ]
#gens  = { cat:                      [  gen for  gen in sorted( conf_fn[cat].keys()           ) if gen         in [ gn.split("_")[0] for gn in use_gennum ] ]                                                                                     for cat in cats                               }
#nums  = { cat: { gen:               [  num for  num in sorted( conf_fn[cat][gen].keys()      ) if gen+"_"+num in use_gennum                                ]                                                              for gen in gens[cat] } for cat in cats                               }
#levs  = { cat: { gen: { num:        [  lev for  lev in sorted( conf_fn[cat][gen][num].keys() )                                                             ]                                  for num in nums[cat][gen] } for gen in gens[cat] } for cat in cats                               }
#flavs = { cat: { gen: { num: { lev: [ flav for flav in sorted( dataset_flavors[gen+"_"+num]  )                                                             ] for lev in levs[cat][gen][num] } for num in nums[cat][gen] } for gen in gens[cat] } for cat in cats                               }
#
#stepi_levels    = [ "L0", "L1", "L2", "L3", "L4", "L5" ]
#stepii_cut_lev  = [ "L5" ]
#stepii_levels   = [ "L5", "L6" ]
#
#all_levs, all_flavs = [], []
#for cat in cats:
#	for gen in gens[cat]:
#		for num in nums[cat][gen]:
#			all_levs = add_to_list_uniquely( all_levs, levs[cat][gen][num] )
#			for lev in levs[cat][gen][num]:
#				all_flavs = add_to_list_uniquely( all_flavs, flavs[cat][gen][num][lev] )
#
#gennumflavs = [ ( gennum.split("_")[0], gennum.split("_")[1], flav ) for gennum in sorted(dataset_flavors.keys()) for flav in dataset_flavors[gennum] if gennum in use_gennum ]
#
#flavgennums = {}
#for flav in all_flavs:
#	flavgennums[flav] = []
#	for gennum in use_gennum:
#		this_gen, this_num = gennum.split("_")
#		if flav in flavs["montecarlo_data"][this_gen][this_num]["L5"]:
#			flavgennums[flav] += [ ( this_gen, this_num ) ]
#flavlevs = {}
#for flav in all_flavs:
#	flavlevs[flav] = []
#	for cat in cats:
#		for gen in gens[cat]:
#			for num in nums[cat][gen]:
#				for lev in levs[cat][gen][num]:
#					if flav in flavs[cat][gen][num][lev]:
#						flavlevs[flav] = add_to_list_uniquely(flavlevs[flav],[lev])
#
#
#
#
#datafile_list = get_filenames_in_dir( configs["path"]["dir"]["mergedfiles"], "HDF" )
#datafiles = {
#	cat: { gen: { num: { lev: { flav:
#		""
#	  for flav in flavs[cat][gen][num][lev] } for lev in levs[cat][gen][num] } for num in nums[cat][gen] } for gen in gens[cat] } for cat in cats
#	}
#for datafile in datafile_list:
#	filename = datafile.split("/")[-1]
#	filegen  = filename.split("_")[0]
#	filenum  = filename.split("_")[1]
#	filecat  = str(configs["data_category"][filegen][filenum])
#	filelev  = filename.split("_")[-1].split(".")[0]
#	fileflav = filename.split("_")[2]
#	datafiles[filecat][filegen][filenum][filelev][fileflav] = datafile
#
#
#
#weightkeys_numudif = {
#	"numudif_central"    : [ "wtcount", "wtonecentral",    "wtoverlapcentral_nancymedium_nancyhigh",    "wtoverlapcentral_nancyhigh_iceprodhigh",    "wtistest" ],
#	"numudif_plussigma"  : [ "wtcount", "wtoneplussigma",  "wtoverlapplussigma_nancymedium_nancyhigh",  "wtoverlapplussigma_nancyhigh_iceprodhigh",  "wtistest" ],
#	"numudif_minussigma" : [ "wtcount", "wtoneminussigma", "wtoverlapminussigma_nancymedium_nancyhigh", "wtoverlapminussigma_nancyhigh_iceprodhigh", "wtistest" ],
#}
#
#weightkeys_use                = [ wtkey for wtkey in weightkeys_numudif["numudif_central"] ]
#
#
#





#  "path": {
#    "dir": {
#      "library":          "/home/aburgman/icecube/00_library/",
#      "datasets":         "/home/aburgman/icecube/03_datasets/",
#      "cube":             "/home/aburgman/icecube/181024_mmact/",
#      "data":        "/data/user/aburgman/icedata/181024_mmact/",
#      "filenames":   "/data/user/aburgman/icedata/181024_mmact/00_filenames/",
#      "mergedfiles": "/data/user/aburgman/icedata/181024_mmact/01_merged_files/",
#      "plots":       "/data/user/aburgman/icedata/181024_mmact/02_plots/",
#      "bdt":         "/data/user/aburgman/icedata/181024_mmact/03_bdt_stuff/"
#    },
#    "library": {
#      "cutting":                  "cutting.py",
#      "frameobject_manipulation": "frameobject_manipulation.py",
#      "misc":                     "misc.py",
#      "plotting":                 "plotting.py",
#      "statistics":               "statistics.py"
#    },
#    "misc": {
#      "funcs_custom":             "funcs_custom.py",
#    }
#  },
#  "bdt": {
#    "bdtx": {
#      "bdta": "/bdta/",
#      "bdtb": "/bdtb/",
#      "bdtc": "/bdtc/",
#      "bdtd": "/bdtd/",
#      "bdte": "/bdte/"
#    },
#    "subdir": {
#      "data":   "/data/",
#      "output": "/output/"
#    }
#  },
#  "data_category": {
#    "mpsim": {
#      "00000": "montecarlo_data",
#      "00001": "montecarlo_data"
#    },
#    "juliet": {
#      "12497": "montecarlo_data"
#    },
#    "nugen": {
#      "00000": "montecarlo_data",
#      "00001": "montecarlo_data",
#      "00002": "montecarlo_data",
#      "11070": "montecarlo_data",
#      "11297": "montecarlo_data"
#    },
#    "experimental": {
#      "00000": "experimental_data"
#    }
#  },
#  "interesting_frameobjects": [
#    "I3EventHeader",
#    "EHEPortiaEventSummary",
#    "EHEOpheliaSRT_ImpLF",
#    "EHEOpheliaParticleSRT_ImpLF",
#    "InIcePulses",
#    "InIceDSTOnlyPulses",
#    "InIceDSTPulses",
#    "EHEInIcePulsesSRT",
#    "EHETWCInIcePulsesSRT",
#    "EHEdebiased_BestPortiaPulseSRT_CleanDelay",
#    "CalibratedWaveformRange",
#    "Millipede*",
#    "PUT_IN_ALL_THE_ONES_WHICH_MAY_BE_CUT_ON",
#    "PUT_IN_COMMON_VARIABLES_STUFF",
#    "PUT_IN_MILLIPEDE",
#    "PUT_IN_MONOPOD",
#    "MCPrimaryParticle",
#    "PoleEHESummaryPulseInfo",
#    "PoleEHEOphelia_ImpLF",
#    "PoleEHEOpheliaParticle_ImpLF",
#    "CountingWeightFactor",
#    "RelativeSpectrumWeightFactor",
#    "QFilterMask",
#    "FilterMask",
#    "I3SuperDST",
#    "ReextractedInIcePulses",
#    "PropagationMatrix",
#    "JulietWeightDict",
#    "Homogenized_Qtot"
#  ],
#  "data_sample_details": {
#    "montecarlo_data": {
#      "mpsim": {
#        "00000": "/data/user/aburgman/icedata/01_mc__mpsim_monopole__170131/details.json",
#        "00001": "/data/ana/BSM/IC86_MagneticMonopoles_AboveCherenkovThreshold/details.json"
#      },
#      "juliet": {
#        "12497": "/home/aburgman/icecube/03_datasets/JULIeT_2012/IC86_2012_JULIeT_12497_SPICEMie_EHE__info/details.json"
#      },
#      "nugen": {
#        "00000": "/home/aburgman/icecube/03_datasets/NuGen_2016/nancy_samples/details_00000.json",
#        "00001": "/home/aburgman/icecube/03_datasets/NuGen_2016/nancy_samples/details_00001.json",
#        "00002": "/home/aburgman/icecube/03_datasets/NuGen_2016/nancy_samples/details_00002.json",
#        "11070": "/home/aburgman/icecube/03_datasets/NuGen_2012/details_11070.json",
#        "11297": "/home/aburgman/icecube/03_datasets/NuGen_2012/details_11297.json"
#      }
#    },
#    "experimental_data": {
#      "experimental": {
#        "00000": ""
#      }
#    }
#  },
#  "data_filename_template": {
#    "montecarlo_data": {
#      "mpsim": {
#        "00000": "mpsim_FLAVOR_00000__beta_0800_0995__000000_PROCESSNUMBER.EXTENSION",
#        "00001": "mpsim_FLAVOR__IC86_YEAR__beta_BETALOW_BETAHIGH__proc_PROCESSNUMBER.EXTENSION"
#      },
#      "juliet": {
#        "12497": "juliet_FLAVOR_12497__energy_1e5GeV_1e11GeV__000000_PROCESSNUMBER.EXTENSION"
#      },
#      "nugen": {
#        "00000": "nugen__FLAVOR__low_energy__IC86_flasher_p1_03_p2_00__l2__SETNUMBER__l2_PROCESSNUMBER.EXTENSION",
#        "00001": "nugen__FLAVOR__medium_energy__IC86_flasher_p1_03_p2_00__l2__SETNUMBER__l2_PROCESSNUMBER.EXTENSION",
#        "00002": "nugen__FLAVOR__high_energy__IC86_flasher_p1_03_p2_00__l2__SETNUMBER__l2_PROCESSNUMBER.EXTENSION",
#        "11070": "nugen__FLAVOR__IC86__YEAR__11070__PROCESSNUMBER.EXTENSION",
#        "11297": "nugen__FLAVOR__IC86__YEAR__11297__PROCESSNUMBER.EXTENSION"
#      }
#    },
#    "experimental_data": {
#      "experimental": {
#        "00000": ""
#      }
#    }
#  },
#  "data_keep_i3file": {
#    "montecarlo_data": {
#      "mpsim": {
#        "00000": [
#          "mpsim_monopole_00000__beta_0800_0995__000000_000000.i3.bz2"
#        ],
#        "00001": [
#          "mpsim_monopole__IC86_2016__beta_0750_0995__proc_0000.i3.gz"
#        ]
#      },
#      "juliet": {
#        "12497": [
#          "juliet_mu_12497__energy_1e5GeV_1e11GeV__000000_000000.i3.bz2",
#          "juliet_tau_12497__energy_1e5GeV_1e11GeV__000000_000190.i3.bz2",
#          "juliet_nue_12497__energy_1e5GeV_1e11GeV__000000_000050.i3.bz2",
#          "juliet_numu_12497__energy_1e5GeV_1e11GeV__000000_000000.i3.bz2",
#          "juliet_nutau_12497__energy_1e5GeV_1e11GeV__000000_000000.i3.bz2"
#        ]
#      },
#      "nugen": {
#        "00000": [
#          "NuE__low_energy__IC86_flasher_p1_03_p2_00__l2__0001__l2_00000001.i3.zst",
#          "NuMu__low_energy__IC86_flasher_p1_03_p2_00__l2__0001__l2_00000001.i3.zst",
#          "NuTau__low_energy__IC86_flasher_p1_03_p2_00__l2__0001__l2_00000001.i3.zst"
#        ],
#        "00001": [
#          "NuE__medium_energy__IC86_flasher_p1_03_p2_00__l2__0001__l2_00000001.i3.zst",
#          "NuMu__medium_energy__IC86_flasher_p1_03_p2_00__l2__0001__l2_00000001.i3.zst",
#          "NuTau__medium_energy__IC86_flasher_p1_03_p2_00__l2__0001__l2_00000001.i3.zst"
#        ],
#        "00002": [
#          "NuE__high_energy__IC86_flasher_p1_03_p2_00__l2__0001__l2_00000001.i3.zst",
#          "NuMu__high_energy__IC86_flasher_p1_03_p2_00__l2__0001__l2_00000001.i3.zst",
#          "NuTau__high_energy__IC86_flasher_p1_03_p2_00__l2__0001__l2_00000001.i3.zst"
#        ],
#        "11070": [
#          ""
#        ],
#        "11297": [
#          ""
#        ]
#      }
#    },
#    "experimental_data": {
#      "experimental": {
#        "00000": [
#          ""
#        ]
#      }
#    }
#  },
#  "filename": {
#    "montecarlo_data": {
#      "mpsim": {
#        "00000": {
#          "G0": "filenames_G0__mpsim_00000.txt",
#          "L0": "filenames_L0__mpsim_00000.txt",
#          "L1": "filenames_L1__mpsim_00000.txt",
#          "L2": "filenames_L2__mpsim_00000.txt",
#          "L3": "filenames_L3__mpsim_00000.txt",
#          "L4": "filenames_L4__mpsim_00000.txt",
#          "L5": "filenames_L5__mpsim_00000.txt",
#          "L6": "filenames_L6__mpsim_00000.txt"
#        },
#        "00001": {
#          "G0": "filenames_G0__mpsim_00001.txt",
#          "L0": "filenames_L0__mpsim_00001.txt",
#          "L1": "filenames_L1__mpsim_00001.txt",
#          "L2": "filenames_L2__mpsim_00001.txt",
#          "L3": "filenames_L3__mpsim_00001.txt",
#          "L4": "filenames_L4__mpsim_00001.txt",
#          "L5": "filenames_L5__mpsim_00001.txt",
#          "L6": "filenames_L6__mpsim_00001.txt"
#        }
#      },
#      "juliet": {
#        "12497": {
#          "L0": "filenames_L0__juliet_12497.txt",
#          "L1": "filenames_L1__juliet_12497.txt",
#          "L2": "filenames_L2__juliet_12497.txt",
#          "L3": "filenames_L3__juliet_12497.txt",
#          "L4": "filenames_L4__juliet_12497.txt",
#          "L5": "filenames_L5__juliet_12497.txt",
#          "L6": "filenames_L6__juliet_12497.txt"
#        }
#      },
#      "nugen": {
#        "00000": { "L0": "", "L1": "", "L2": "", "L3": "", "L4": "", "L5": "", "L6": "" },
#        "00001": { "L0": "", "L1": "", "L2": "", "L3": "", "L4": "", "L5": "", "L6": "" },
#        "00002": { "L0": "", "L1": "", "L2": "", "L3": "", "L4": "", "L5": "", "L6": "" },
#        "11070": { "L0": "", "L1": "", "L2": "", "L3": "", "L4": "", "L5": "", "L6": "" },
#        "11297": { "L0": "", "L1": "", "L2": "", "L3": "", "L4": "", "L5": "", "L6": "" }
#      }
#    },
#    "experimental_data": {
#      "experimental": {
#        "00000": {
#          "L0": "",
#          "L1": "",
#          "L2": "",
#          "L3": "",
#          "L4": "",
#          "L5": "",
#          "L6": "",
#          "LA": ""
#        }
#      }
#    }
#  },
#  "subdir": {
#    "montecarlo_data": {
#      "mpsim": {
#        "00000": {
#          "G0": "/mpsim_00000__G0_gen/",
#          "L0": "/mpsim_00000__L0_trigg/",
#          "L1": "/mpsim_00000__L1_ehefilt/",
#          "L2": "/mpsim_00000__L2_anacut/",
#          "L3": "/mpsim_00000__L3_atmnucut/",
#          "L4": "/mpsim_00000__L4_atmmucut/",
#          "L5": "/mpsim_00000__L5_itveto/",
#          "L6": "/mpsim_00000__L6_astnucut/",
#          "LA": "/mpsim_00000__LA_fakedir/"
#        },
#        "00001": {
#          "G0": "/mpsim_00001__G0_gen/",
#          "L0": "/mpsim_00001__L0_trigg/",
#          "L1": "/mpsim_00001__L1_ehefilt/",
#          "L2": "/mpsim_00001__L2_anacut/",
#          "L3": "/mpsim_00001__L3_atmnucut/",
#          "L4": "/mpsim_00001__L4_atmmucut/",
#          "L5": "/mpsim_00001__L5_itveto/",
#          "L6": "/mpsim_00001__L6_astnucut/",
#          "LA": "/mpsim_00001__LA_fakedir/"
#        }
#      },
#      "juliet": {
#        "12497": {
#          "L0": "/juliet_12497__L0_trigg/",
#          "L1": "/juliet_12497__L1_ehefilt/",
#          "L2": "/juliet_12497__L2_anacut/",
#          "L3": "/juliet_12497__L3_atmnucut/",
#          "L4": "/juliet_12497__L4_atmmucut/",
#          "L5": "/juliet_12497__L5_itveto/",
#          "L6": "/juliet_12497__L6_astnucut/",
#          "LA": "/juliet_12497__LA_fakedir/"
#        }
#      },
#      "nugen": {
#        "00000": {
#          "L0": "/nugen_00000__L0_trigg/",
#          "L1": "/nugen_00000__L1_ehefilt/",
#          "L2": "/nugen_00000__L2_anacut/",
#          "L3": "/nugen_00000__L3_atmnucut/",
#          "L4": "/nugen_00000__L4_atmmucut/",
#          "L5": "/nugen_00000__L5_itveto/",
#          "L6": "/nugen_00000__L6_astnucut/",
#          "LA": "/nugen_00000__LA_fakedir/"
#        },
#        "00001": {
#          "L0": "/nugen_00001__L0_trigg/",
#          "L1": "/nugen_00001__L1_ehefilt/",
#          "L2": "/nugen_00001__L2_anacut/",
#          "L3": "/nugen_00001__L3_atmnucut/",
#          "L4": "/nugen_00001__L4_atmmucut/",
#          "L5": "/nugen_00001__L5_itveto/",
#          "L6": "/nugen_00001__L6_astnucut/",
#          "LA": "/nugen_00001__LA_fakedir/"
#        },
#        "00002": {
#          "L0": "/nugen_00002__L0_trigg/",
#          "L1": "/nugen_00002__L1_ehefilt/",
#          "L2": "/nugen_00002__L2_anacut/",
#          "L3": "/nugen_00002__L3_atmnucut/",
#          "L4": "/nugen_00002__L4_atmmucut/",
#          "L5": "/nugen_00002__L5_itveto/",
#          "L6": "/nugen_00002__L6_astnucut/",
#          "LA": "/nugen_00002__LA_fakedir/"
#        },
#        "11070": {
#          "L0": "/nugen_11070__L0_trigg/",
#          "L1": "/nugen_11070__L1_ehefilt/",
#          "L2": "/nugen_11070__L2_anacut/",
#          "L3": "/nugen_11070__L3_atmnucut/",
#          "L4": "/nugen_11070__L4_atmmucut/",
#          "L5": "/nugen_11070__L5_itveto/",
#          "L6": "/nugen_11070__L6_astnucut/",
#          "LA": "/nugen_11070__LA_fakedir/"
#        },
#        "11297": {
#          "L0": "/nugen_11297__L0_trigg/",
#          "L1": "/nugen_11297__L1_ehefilt/",
#          "L2": "/nugen_11297__L2_anacut/",
#          "L3": "/nugen_11297__L3_atmnucut/",
#          "L4": "/nugen_11297__L4_atmmucut/",
#          "L5": "/nugen_11297__L5_itveto/",
#          "L6": "/nugen_11297__L6_astnucut/",
#          "LA": "/nugen_11297__LA_fakedir/"
#        }
#      }
#    },
#    "experimental_data": {
#      "experimental": {
#        "00000": {
#          "L0": "",
#          "L1": "",
#          "L2": "",
#          "L3": "",
#          "L4": "",
#          "L5": "",
#          "L6": "",
#          "LA": ""
#        }
#      }
#    }
#  },
#  "EHE_analysis_spec": {
#    "highest_EHE_analysis_level": "L5",
#    "L5_decrease_factor": 0.894,
#    "Phi_0": 3.46e-18,
#    "Omega_div_by_4pi_radians": 1.0,
#    "n_ob_L5": {
#      "IC40":     0.0,
#      "IC59":     0.0,
#      "IC79":     0.0,
#      "IC86-I":   0.0,
#      "IC86-II":  0.0,
#      "IC86-III": 0.0,
#      "IC86-IV":  1.0,
#      "IC86-V":   0.0,
#      "IC86-VI":  1.0
#    },
#    "n_bg_L5": {
#      "IC40":     0.0,
#      "IC59":     0.0,
#      "IC79":     0.0,
#      "IC86-I":   0.0,
#      "IC86-II":  0.0,
#      "IC86-III": 0.0,
#      "IC86-IV":  0.0,
#      "IC86-V":   0.0,
#      "IC86-VI":  0.0
#    },
#    "n_bg_L5_alt": {
#      "perlivetime":       7.92,
#      "perlivetime_alta":  3.62,
#      "perlivetime_altb":  7.92,
#      "perlivetime_altc": 16.61
#    },
#    "n_bg_L6": {
#      "IC40":     0.0,
#      "IC59":     0.0,
#      "IC79":     0.0,
#      "IC86-I":   0.0,
#      "IC86-II":  0.0,
#      "IC86-III": 0.0,
#      "IC86-IV":  0.0,
#      "IC86-V":   0.0,
#      "IC86-VI":  0.0
#    },
#    "t_live": {
#      "IC40":     373.08,
#      "IC59":     342.76,
#      "IC79":     312.52,
#      "IC86-I":   341.77,
#      "IC86-II":  329.65,
#      "IC86-III": 360.34,
#      "IC86-IV":  365.91,
#      "IC86-V":   359.30,
#      "IC86-VI":  357.18
#    },
#    "t_burn": {
#      "IC40":     35.32,
#      "IC59":     33.04,
#      "IC79":     33.23,
#      "IC86-I":   33.56,
#      "IC86-II":  34.70,
#      "IC86-III": 33.98,
#      "IC86-IV":  34.71,
#      "IC86-V":   37.17,
#      "IC86-VI":   0.0
#    }
#  },
#  "exclude_files": {
#    "montecarlo_data": {
#      "mpsim": {
#        "00000": [
#        ]
#      },
#      "juliet": {
#        "12497": [
#        ]
#      },
#      "nugen": {
#        "00000": [
#        ]
#      }
#    },
#    "experimental_data": {
#      "experimental": {
#        "00000": [
#        ]
#      }
#    }
#  }




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



