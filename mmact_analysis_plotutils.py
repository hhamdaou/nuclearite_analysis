import numpy as np
import scipy as sp
import scipy.constants as spco

from icecube import icetray
from icecube.icetray import I3Units

#ev_rate_label = "Event Rate  [$t_{live,\mathrm{IC86}"+u"\u2010"+"\mathrm{I}"+u"\u2013"+"\mathrm{VIII}}^{-1}$]"
ev_rate_label       = "Event Rate  [$t_{\mathrm{IC86, 8 yr}}^{-1}$]"
ev_rate_label_pers  = "Event Rate  [$\mathrm{s}^{-1}$]"
ev_rate_label_peryr = "Event Rate  [$\mathrm{yr}^{-1}$]"
au_label = "[a.u.]"
# Hyphen:  u"\u2010"
# En-dash: u"\u2013"
# Em-dash: u"\u2014"

#:--
# UNITS
#:--

unit_label = {
	""              : r"",
	"rad"           : r"$\mathrm{rad}$",
	"m"             : r"$\mathrm{m}$",
	"ns"            : r"$\mathrm{ns}$",
	"mus"           : r"$\mathrm{\mu s}$",
	"GeV"           : r"$\mathrm{GeV}$",
	"m2"            : r"$\mathrm{m^{2}}$",
	"km2"           : r"$\mathrm{km^{2}}$",
	"cm-2 s-1 sr-1" : r"$\mathrm{cm^{-2}s^{-1}sr^{-1}}$",
	"e"             : r"$e$",
	}
unit_value = {
	""              : 1.,
	"rad"           : I3Units.rad,
	"m"             : I3Units.m,
	"ns"            : I3Units.ns,
	"mus"           : I3Units.microsecond,
	"GeV"           : I3Units.GeV,
	"m2"            : I3Units.m2,
	"km2"           : I3Units.km2,
	"cm-2 s-1 sr-1" : 1./(I3Units.cm2*I3Units.s*I3Units.steradian),
	"e"             : I3Units.eplus,
	}


#:--
# HISTOGRAMMING
#:--

nbin = {
	"mccoszen"            : 40,
	"mcazi"               : 36,
	"mcbeta"              : 50,
	"mclog10energy"       : 50,
	"mccentrality"        : 50,
	"mcgeomlength"        : 40,
	"mcgeomtime"          : 40,
	"bdtseparator"        : 50,
	"bdtistest"           : 50,
	"ptlog10npe"          : 50,
	"ptnch"               : 40,
	"ptrhope"             : 40,
	"opcoszen"            : 40,
	"opazi"               : 36,
	"opbeta"              : 45,
	"opfitquality"        : 50,
	"opcentrality"        : 50,
	"opgeomlength"        : 40,
	"opgeomtime"          : 40,
	"bmcoszen"            : 40,
	"bmazi"               : 36,
	"bmbeta"              : 45,
	"bmcentrality"        : 50,
	"bmgeomlength"        : 40,
	"bmgeomtime"          : 40,
	"cvdihdlength"        : 50,
	"cvdihdsmoothness"    : 50,
	"cvdihdqdirect"       : 50,
	"cvdihdqearly"        : 50,
	"cvdihdqlate"         : 50,
	"cvdihalength"        : 50,
	"cvdihasmoothness"    : 50,
	"cvdihaqdirect"       : 50,
	"cvdihaqearly"        : 50,
	"cvdihaqlate"         : 50,
	"cvhiscog"            : 50,
	"cvtictimefwhm"       : 50,
	"cvtictimetot"        : 50,
	"cvtrclength"         : 50,
	"cvtrcsmoothness"     : 50,
	"cvtrcavgdistq"       : 50,
	"cvdihabmmlength"     : 50,
	"cvdihabmmsmoothness" : 50,
	"cvdihabmmqdirect"       : 50,
	"cvdihabmmqearly"        : 50,
	"cvdihabmmqlate"         : 50,
	"cvdihdbmmlength"     : 50,
	"cvdihdbmmsmoothness" : 50,
	"cvdihdbmmqdirect"       : 50,
	"cvdihdbmmqearly"        : 50,
	"cvdihdbmmqlate"         : 50,
	"cvtrcbmmlength"      : 50,
	"cvtrcbmmsmoothness"  : 50,
	"cvtrcbmmavgdistq"    : 50,
	"cvticbmmtimefwhm"    : 50,
	"cvticbmmtimetot"     : 50,
	"mpavge"              : 50,
	"mpstde"              : 50,
	"mprsde"              : 50,
	"coavgx"              : 50,
	"costdx"              : 50,
	"corsdx"              : 50,
	"coavgt"              : 50,
	"costdt"              : 50,
	"corsdt"              : 50,
	"ftxanpe"             : 50,
	"ftanpelgeom"         : 50,
	"ftanpeldihd"         : 50,
	"ftanpeldiha"         : 50,
	"ftanpeltrc"          : 50,
	"ftxaqdihd"           : 50,
	"ftaqdihdlgeom"       : 50,
	"ftaqdihdldihd"       : 50,
	"ftaqdihdldiha"       : 50,
	"ftaqdihdltrc"        : 50,
	"ftxaqdiha"           : 50,
	"ftaqdihalgeom"       : 50,
	"ftaqdihaldihd"       : 50,
	"ftaqdihaldiha"       : 50,
	"ftaqdihaltrc"        : 50,
	"mcopbetadiff"        : 60,
	"mcbmbetadiff"        : 60,
	"bmcvdihdnonlength"   : 50,
	"bmcvdihanonlength"   : 50,
	"bmcvtrcnonlength"    : 50,
	"bmcvticnontimefwhm"  : 50,
	"bmcvticnontimetot"   : 50,
	"bmcvhiscogoffset"    : 50,
	"bmcvdihdbmmnonlength"    : 50,
	"bmcvdihabmmnonlength"    : 50,
	"bmcvtrcbmmnonlength"     : 50,
	"bmcvticbmmnontimefwhm"   : 50,
	"bmcvticbmmnontimetot"    : 50,
	"bmcvdihdnonlengthfrac"   : 50,
	"bmcvdihanonlengthfrac"   : 50,
	"bmcvtrcnonlengthfrac"    : 50,
	"bmcvticnontimefwhmfrac"  : 50,
	"bmcvticnontimetotfrac"   : 50,
	"bmcvdihdbmmnonlengthfrac"    : 50,
	"bmcvdihabmmnonlengthfrac"    : 50,
	"bmcvtrcbmmnonlengthfrac"     : 50,
	"bmcvticbmmnontimefwhmfrac"   : 50,
	"bmcvticbmmnontimetotfrac"    : 50,
	"bmcvhisrelativecogoffset"    : 50,
	"bmcvdihdlengthfillratio"     : 50,
	"bmcvdihalengthfillratio"     : 50,
	"bmcvtrclengthfillratio"      : 50,
	"bmcvtictimefwhmfillratio"    : 50,
	"bmcvtictimetotfillratio"     : 50,
	"bmcvdihdbmmlengthfillratio"  : 50,
	"bmcvdihabmmlengthfillratio"  : 50,
	"bmcvtrcbmmlengthfillratio"   : 50,
	"bmcvticbmmtimefwhmfillratio" : 50,
	"bmcvticbmmtimetotfillratio"  : 50,
	"bdtascore"           : 40,
	"bdtbscore"           : 40,
	"bdtcscore"           : 40,
	"bdtdscore"           : 40,
	"bdtescore"           : 40,
	}

range_x = {
	"mccoszen"            : [        -1.0    ,              1.0            ],
	"mcazi"               : [         0.0    ,              2.0 * np.pi    ],
	"mcbeta"              : [         0.75   ,              1.0            ],
	"mclog10energy"       : [         4.5    ,              9.5            ],
	"mccentrality"        : [         0.0    ,           1000.0            ],
	"mcgeomlength"        : [         0.0    ,           2000.0            ],
	"mcgeomtime"          : [         0.0    ,          16000.0            ],
	"bdtseparator"        : [         0.0    ,              1.0            ],
	"bdtistest"           : [         0.0    ,              1.0            ],
	"ptlog10npe"          : [         2.5    ,              7.5            ],
	"ptnch"               : [         0.0    ,           1500.0            ],
	"ptrhope"             : [         0.0    ,           1000.0            ],
	"opcoszen"            : [        -1.0    ,              1.0            ],
	"opazi"               : [         0.0    ,              2.0 * np.pi    ],
	"opbeta"              : [         0.0    ,              1.5            ],
	"opfitquality"        : [         0.0    ,            250.0            ],
	"opcentrality"        : [         0.0    ,           1000.0            ],
	"opgeomlength"        : [         0.0    ,           2000.0            ],
	"opgeomtime"          : [         0.0    ,          16000.0            ],
	"bmcoszen"            : [        -1.0    ,              1.0            ],
	"bmazi"               : [         0.0    ,              2.0 * np.pi    ],
	"bmbeta"              : [         0.0    ,              1.5            ],
	"bmcentrality"        : [         0.0    ,           1000.0            ],
	"bmgeomlength"        : [         0.0    ,           2000.0            ],
	"bmgeomtime"          : [         0.0    ,          16000.0            ],
	"cvdihdlength"        : [         0.0    ,           1600.0            ],
	"cvdihdsmoothness"    : [        -1.0    ,              1.0            ],
	"cvdihdqdirect"       : [         0.0    ,          60000.0            ],
	"cvdihdqearly"        : [         0.0    ,         200000.0            ],
	"cvdihdqlate"         : [         0.0    ,         200000.0            ],
	"cvdihalength"        : [         0.0    ,           1600.0            ],
	"cvdihasmoothness"    : [        -1.0    ,              1.0            ],
	"cvdihaqdirect"       : [         0.0    ,          20000.0            ],
	"cvdihaqearly"        : [         0.0    ,         200000.0            ],
	"cvdihaqlate"         : [         0.0    ,         200000.0            ],
	"cvhiscog"            : [         0.0    ,            800.0            ],
	"cvtictimefwhm"       : [      1000.0    ,           4000.0            ],
	"cvtictimetot"        : [      3500.0    ,           6500.0            ],
	"cvtrclength"         : [         0.0    ,           1200.0            ],
	"cvtrcsmoothness"     : [        -1.0    ,              1.0            ],
	"cvtrcavgdistq"       : [         0.0    ,             80.0            ],
	"cvdihabmmlength"     : [         0.0    ,           1600.0            ],
	"cvdihabmmsmoothness" : [        -1.0    ,              1.0            ],
	"cvdihabmmqdirect"       : [         0.0    ,         1000.0            ],
	"cvdihabmmqearly"        : [         0.0    ,         4000.0            ],
	"cvdihabmmqlate"         : [         0.0    ,         2000.0            ],
	"cvdihdbmmlength"     : [         0.0    ,           1600.0            ],
	"cvdihdbmmsmoothness" : [        -1.0    ,              1.0            ],
	"cvdihdbmmqdirect"       : [         0.0    ,         1000.0            ],
	"cvdihdbmmqearly"        : [         0.0    ,         4000.0            ],
	"cvdihdbmmqlate"         : [         0.0    ,         2000.0            ],
	"cvtrcbmmlength"      : [         0.0    ,           1600.0            ],
	"cvtrcbmmsmoothness"  : [        -1.0    ,              1.0            ],
	"cvtrcbmmavgdistq"    : [         0.0    ,             80.0            ],
	"cvticbmmtimefwhm"    : [         0.0    ,           5000.0            ],
	"cvticbmmtimetot"     : [         0.0    ,           5000.0            ],
	"mpavge"              : [         0.0    ,          50000.0            ],
	"mpstde"              : [         0.0    ,         150000.0            ],
	"mprsde"              : [         0.0    ,             15.0            ],
	"coavgx"              : [      -250.0    ,            250.0            ],
	"costdx"              : [         0.0    ,            800.0            ],
	"corsdx"              : [       -50.0    ,             50.0            ],
	"coavgt"              : [         0.0    ,           4000.0            ],
	"costdt"              : [         0.0    ,           2000.0            ],
	"corsdt"              : [         0.0    ,              2.5            ],
	"ftxanpe"             : [         0.0    ,        2000000.0            ],
	"ftanpelgeom"         : [         0.0    ,           2000.0            ],
	"ftanpeldihd"         : [         0.0    ,           2000.0            ],
	"ftanpeldiha"         : [         0.0    ,           2000.0            ],
	"ftanpeltrc"          : [         0.0    ,           2000.0            ],
	"ftxaqdihd"           : [         0.0    ,         200000.0            ],
	"ftaqdihdlgeom"       : [         0.0    ,            200.0            ],
	"ftaqdihdldihd"       : [         0.0    ,            200.0            ],
	"ftaqdihdldiha"       : [         0.0    ,            200.0            ],
	"ftaqdihdltrc"        : [         0.0    ,            200.0            ],
	"ftxaqdiha"           : [         0.0    ,          50000.0            ],
	"ftaqdihalgeom"       : [         0.0    ,             50.0            ],
	"ftaqdihaldihd"       : [         0.0    ,             50.0            ],
	"ftaqdihaldiha"       : [         0.0    ,             50.0            ],
	"ftaqdihaltrc"        : [         0.0    ,             50.0            ],
	"mcopbetadiff"        : [        -0.5    ,              1.0            ],
	"mcbmbetadiff"        : [        -0.5    ,              1.0            ],
	"bmcvdihdnonlength"   : [      -500.0    ,           1300.0            ],
	"bmcvdihanonlength"   : [      -500.0    ,           1300.0            ],
	"bmcvtrcnonlength"    : [         0.0    ,           1800.0            ],
	"bmcvticnontimefwhm"  : [     -2000.0    ,           6000.0            ],
	"bmcvticnontimetot"   : [     -5000.0    ,           5000.0            ],
	"bmcvhiscogoffset"    : [         0.0    ,            800.0            ],
	"bmcvdihdbmmnonlength"        : [      -500.0    ,           1300.0            ],
	"bmcvdihabmmnonlength"        : [      -500.0    ,           1300.0            ],
	"bmcvtrcbmmnonlength"         : [         0.0    ,           1800.0            ],
	"bmcvticbmmnontimefwhm"       : [     -2000.0    ,           6000.0            ],
	"bmcvticbmmnontimetot"        : [     -5000.0    ,           5000.0            ],
	"bmcvdihdnonlengthfrac"       : [        -0.5    ,              1.0            ],
	"bmcvdihanonlengthfrac"       : [        -0.5    ,              1.0            ],
	"bmcvtrcnonlengthfrac"        : [         0.0    ,              1.0            ],
	"bmcvticnontimefwhmfrac"      : [        -0.5    ,              1.0            ],
	"bmcvticnontimetotfrac"       : [        -0.5    ,              0.5            ],
	"bmcvdihdbmmnonlengthfrac"    : [        -0.5    ,              1.0            ],
	"bmcvdihabmmnonlengthfrac"    : [        -0.5    ,              1.0            ],
	"bmcvtrcbmmnonlengthfrac"     : [         0.0    ,              1.0            ],
	"bmcvticbmmnontimefwhmfrac"   : [        -0.5    ,              1.0            ],
	"bmcvticbmmnontimetotfrac"    : [        -0.5    ,              0.5            ],
	"bmcvhisrelativecogoffset"    : [         0.0    ,              0.6            ],
	"bmcvdihdlengthfillratio"     : [         0.0    ,              2.0            ],
	"bmcvdihalengthfillratio"     : [        -2.0    ,              2.0            ],
	"bmcvtrclengthfillratio"      : [         0.0    ,              1.0            ],
	"bmcvtictimefwhmfillratio"    : [         0.0    ,              2.0            ],
	"bmcvtictimetotfillratio"     : [         0.0    ,              4.0            ],
	"bmcvdihdbmmlengthfillratio"  : [         0.0    ,              2.0            ],
	"bmcvdihabmmlengthfillratio"  : [         0.0    ,              2.0            ],
	"bmcvtrcbmmlengthfillratio"   : [         0.0    ,              1.0            ],
	"bmcvticbmmtimefwhmfillratio" : [         0.0    ,              2.0            ],
	"bmcvticbmmtimetotfillratio"  : [         0.0    ,              4.0            ],
	"bdtascore"           : [-1.0,1.0],
	"bdtbscore"           : [-1.0,1.0],
	"bdtcscore"           : [-1.0,1.0],
	"bdtdscore"           : [-1.0,1.0],
	"bdtescore"           : [-1.0,1.0],
	}

WIP_position_lin = {
	"mccoszen"            : "ur",
	"mcazi"               : "cc",
	"mcbeta"              : "ul",
	"mclog10energy"       : "ur",
	"mccentrality"        : "ur",
	"mcgeomlength"        : "ur",
	"mcgeomtime"          : "ur",
	"bdtseparator"        : "uc",
	"bdtistest"           : "uc",
	"ptlog10npe"          : "ur",
	"ptnch"               : "ur",
	"ptrhope"             : "ur",
	"opcoszen"            : "ur",
	"opazi"               : "cc",
	"opbeta"              : "ul",
	"opfitquality"        : "ur",
	"opcentrality"        : "ur",
	"opgeomlength"        : "ur",
	"opgeomtime"          : "ur",
	"bmcoszen"            : "ur",
	"bmazi"               : "cc",
	"bmbeta"              : "ul",
	"bmcentrality"        : "ur",
	"bmgeomlength"        : "ur",
	"bmgeomtime"          : "ur",
	"cvdihdlength"        : "ul",
	"cvdihdsmoothness"    : "ur",
	"cvdihdqdirect"       : "ur",
	"cvdihdqearly"        : "ur",
	"cvdihdqlate"         : "ur",
	"cvdihalength"        : "ul",
	"cvdihasmoothness"    : "ur",
	"cvdihaqdirect"       : "ur",
	"cvdihaqearly"        : "ur",
	"cvdihaqlate"         : "ur",
	"cvhiscog"            : "ul",
	"cvtictimefwhm"       : "ur",
	"cvtictimetot"        : "ur",
	"cvtrclength"         : "ul",
	"cvtrcsmoothness"     : "ur",
	"cvtrcavgdistq"       : "ur",
	"cvdihabmmlength"     : "ul",
	"cvdihabmmsmoothness" : "ur",
	"cvdihabmmqdirect"       : "ur",
	"cvdihabmmqearly"        : "ur",
	"cvdihabmmqlate"         : "ur",
	"cvdihdbmmlength"     : "ul",
	"cvdihdbmmsmoothness" : "ur",
	"cvdihdbmmqdirect"       : "ur",
	"cvdihdbmmqearly"        : "ur",
	"cvdihdbmmqlate"         : "ur",
	"cvtrcbmmlength"      : "ul",
	"cvtrcbmmsmoothness"  : "ur",
	"cvtrcbmmavgdistq"    : "ur",
	"cvticbmmtimefwhm"    : "ur",
	"cvticbmmtimetot"     : "ur",
	"mpavge"              : "ul",
	"mpstde"              : "ur",
	"mprsde"              : "ur",
	"coavgx"              : "ul",
	"costdx"              : "ur",
	"corsdx"              : "ur",
	"coavgt"              : "ul",
	"costdt"              : "ur",
	"corsdt"              : "ur",
	"ftxanpe"             : "ur",
	"ftanpelgeom"         : "ur",
	"ftanpeldihd"         : "ur",
	"ftanpeldiha"         : "ur",
	"ftanpeltrc"          : "ur",
	"ftxaqdihd"           : "ur",
	"ftaqdihdlgeom"       : "ur",
	"ftaqdihdldihd"       : "ur",
	"ftaqdihdldiha"       : "ur",
	"ftaqdihdltrc"        : "ur",
	"ftxaqdiha"           : "ur",
	"ftaqdihalgeom"       : "ur",
	"ftaqdihaldihd"       : "ur",
	"ftaqdihaldiha"       : "ur",
	"ftaqdihaltrc"        : "ur",
	"mcopbetadiff"        : "ur",
	"mcbmbetadiff"        : "ur",
	"bmcvdihdnonlength"   : "ur",
	"bmcvdihanonlength"   : "ur",
	"bmcvtrcnonlength"    : "ur",
	"bmcvticnontimefwhm"  : "ur",
	"bmcvticnontimetot"   : "ur",
	"bmcvhiscogoffset"    : "ur",
	"bmcvdihdbmmnonlength"    : "ur",
	"bmcvdihabmmnonlength"    : "ur",
	"bmcvtrcbmmnonlength"     : "ur",
	"bmcvticbmmnontimefwhm"   : "ur",
	"bmcvticbmmnontimetot"    : "ur",
	"bmcvdihdnonlengthfrac"   : "ur",
	"bmcvdihanonlengthfrac"   : "ur",
	"bmcvtrcnonlengthfrac"    : "ur",
	"bmcvticnontimefwhmfrac"  : "ur",
	"bmcvticnontimetotfrac"   : "ur",
	"bmcvdihdbmmnonlengthfrac"    : "ur",
	"bmcvdihabmmnonlengthfrac"    : "ur",
	"bmcvtrcbmmnonlengthfrac"     : "ur",
	"bmcvticbmmnontimefwhmfrac"   : "ur",
	"bmcvticbmmnontimetotfrac"    : "ur",
	"bmcvhisrelativecogoffset"    : "ur",
	"bmcvdihdlengthfillratio"     : "ul",
	"bmcvdihalengthfillratio"     : "ul",
	"bmcvtrclengthfillratio"      : "ul",
	"bmcvtictimefwhmfillratio"    : "ul",
	"bmcvtictimetotfillratio"     : "ul",
	"bmcvdihdbmmlengthfillratio"  : "ul",
	"bmcvdihabmmlengthfillratio"  : "ul",
	"bmcvtrcbmmlengthfillratio"   : "ul",
	"bmcvticbmmtimefwhmfillratio" : "ul",
	"bmcvticbmmtimetotfillratio"  : "ul",
	"bdtascore"           : "ul",
	"bdtbscore"           : "ul",
	"bdtcscore"           : "ul",
	"bdtdscore"           : "ul",
	"bdtescore"           : "ul",
	}

WIP_position_log = { pk: pos for pk,pos in WIP_position_lin.items() }


label = {
	"mccoszen"            : "$\\cos(\\theta_{zen,\\mathrm{MC}})$",
	"mcazi"               : "$\\phi_{azi,\\mathrm{MC}}$",
	"mcbeta"              : "$\\beta_{\\mathrm{MC}}$",
	"mclog10energy"       : "$\\log_{10}(E_{\\mathrm{MC}}/1 \\mathrm{GeV})$",
	"mccentrality"        : "$d_{C,\\mathrm{MC}}$",
	"mcgeomlength"        : "$l_{geom,\\mathrm{MC}}$",
	"mcgeomtime"          : "$t_{geom,\\mathrm{MC}}$",
	"bdtseparator"        : "$sep_{\mathrm{BDT}}$",
	"bdtistest"           : "$istest_{\mathrm{BDT}}$",
	"ptlog10npe"          : "$\\log_{10}(n_{PE})$",
	"ptnch"               : "$n_{CH}$",
	"ptrhope"             : "$\\rho_{PE}$",
	"opcoszen"            : "$\mathrm{cos}(\\theta_{zen,\mathrm{EHE}})$",
	"opazi"               : "$azi_{\\mathrm{Ophelia}}$",
	"opbeta"              : "$\\beta_{\\mathrm{Ophelia}}$",
	"opfitquality"        : "$\\chi^2_{red,\mathrm{EHE}}$",
	"opcentrality"        : "$d_{C,\\mathrm{Ophelia}}$",
	"opgeomlength"        : "$l_{geom,\\mathrm{Ophelia}}$",
	"opgeomtime"          : "$t_{geom,\\mathrm{Ophelia}}$",
	"bmcoszen"            : "$\\cos(\\theta_{zen,\\mathrm{BM}})$",
	"bmazi"               : "$azi_{\\mathrm{BM}}$",
	"bmbeta"              : "$\\beta_{\\mathrm{BM}}$",
	"bmcentrality"        : "$d_{C,\\mathrm{BM}}$",
	"bmgeomlength"        : "$l_{geom,\\mathrm{BM}}$",
	"bmgeomtime"          : "$t_{geom,\\mathrm{BM}}$",
	"cvdihdlength"        : "$l_{\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"cvdihdsmoothness"    : "$smoothness_{\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"cvdihdqdirect"       : "$Q_{direct,\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"cvdihdqearly"        : "$Q_{early,\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"cvdihdqlate"         : "$Q_{late,\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"cvdihalength"        : "$l_{\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvdihasmoothness"    : "$smoothness_{\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvdihaqdirect"       : "$Q_{direct,\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvdihaqearly"        : "$Q_{early,\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvdihaqlate"         : "$Q_{late,\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvhiscog"            : "$r_{CoG,\\mathrm{CV"+u"\u2010"+"HitStats}}$",
	"cvtictimefwhm"       : "$t_{FWHM,\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"cvtictimetot"        : "$t_{tot,\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"cvtrclength"         : "$l_{\\mathrm{CV"+u"\u2010"+"TrackChar}}$",
	"cvtrcsmoothness"     : "$smoothness_{\\mathrm{CV"+u"\u2010"+"TrackChar}}$",
	"cvtrcavgdistq"       : "$\mathrm{avg}(d_{\\mathrm{DOM},Q})_\\mathrm{CV"+u"\u2010"+"TrackChar}$",
	"cvdihabmmlength"     : "$l_{\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvdihabmmsmoothness" : "$smoothness_{\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvdihabmmqdirect"       : "$Q_{direct,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvdihabmmqearly"        : "$Q_{early,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvdihabmmqlate"         : "$Q_{late,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvdihdbmmlength"     : "$l_{\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"cvdihdbmmsmoothness" : "$smoothness_{\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"cvdihdbmmqdirect"       : "$Q_{direct,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvdihdbmmqearly"        : "$Q_{early,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvdihdbmmqlate"         : "$Q_{late,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"cvtrcbmmlength"      : "$l_{\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TrachChar}}$",
	"cvtrcbmmsmoothness"  : "$smoothness_{\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TrachChar}}$",
	"cvtrcbmmavgdistq"    : "$\mathrm{avg}(d_{\\mathrm{DOM},Q})_{\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TrackChar}}$",
	"cvticbmmtimefwhm"    : "$t_{FWHM,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"cvticbmmtimetot"     : "$t_{tot,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"mpavge"              : "$\\mathrm{avg}(E_{\\mathrm{MIL}})$",
	"mpstde"              : "$\\mathrm{std}(E_{\\mathrm{MIL}})$",
	"mprsde"              : "$\\mathrm{rsd}(E_{\\mathrm{MIL}})$",
	"coavgx"              : "$\\mathrm{avg}(x_{\\mathrm{Cherenkov-offset}})$",
	"costdx"              : "$\\mathrm{std}(x_{\\mathrm{Cherenkov-offset}})$",
	"corsdx"              : "$\\mathrm{rsd}(x_{\\mathrm{Cherenkov-offset}})$",
	"coavgt"              : "$\\mathrm{avg}(t_{\\mathrm{Cherenkov-offset}})$",
	"costdt"              : "$\\mathrm{std}(t_{\\mathrm{Cherenkov-offset}})$",
	"corsdt"              : "$\\mathrm{rsd}(t_{\\mathrm{Cherenkov-offset}})$",
	"ftxanpe"             : "$l\\times A_{n_{pe},\\mathrm{Frank-Tamm}}$",
	"ftanpelgeom"         : "$A_{geom,n_{pe},\\mathrm{Frank-Tamm}}$",
	"ftanpeldihd"         : "$A_{geom,n_{pe},\\mathrm{Frank-Tamm}}$",
	"ftanpeldiha"         : "$A_{geom,n_{pe},\\mathrm{Frank-Tamm}}$",
	"ftanpeltrc"          : "$A_{geom,n_{pe},\\mathrm{Frank-Tamm}}$",
	"ftxaqdihd"           : "$l\\times A_{Q_{\\mathrm{DirHitsD}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihdlgeom"       : "$A_{geom,Q_{\\mathrm{DirHitsD}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihdldihd"       : "$A_{CV-DiH-D,Q_{\\mathrm{DirHitsD}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihdldiha"       : "$A_{CV-DiH-A,Q_{\\mathrm{DirHitsD}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihdltrc"        : "$A_{CV-TrC,Q_{\\mathrm{DirHitsD}},\\mathrm{Frank-Tamm}}$",
	"ftxaqdiha"           : "$l\\times A_{Q_{\\mathrm{DirHitsA}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihalgeom"       : "$A_{geom,Q_{\\mathrm{DirHitsA}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihaldihd"       : "$A_{CV-DiH-D,Q_{\\mathrm{DirHitsA}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihaldiha"       : "$A_{CV-DiH-A,Q_{\\mathrm{DirHitsA}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihaltrc"        : "$A_{CV-TrC,Q_{\\mathrm{DirHitsA}},\\mathrm{Frank-Tamm}}$",
	"mcopbetadiff"        : "$\\beta_{\\mathrm{MC}}-\\beta_{\\mathrm{Ophelia}}$",
	"mcbmbetadiff"        : "$\\beta_{\\mathrm{MC}}-\\beta_{\\mathrm{BM}}$",
	"bmcvdihdnonlength"   : "$l_{non,\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"bmcvdihanonlength"   : "$l_{non,\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"bmcvtrcnonlength"    : "$l_{non,\\mathrm{CV"+u"\u2010"+"TrackChar}}$",
	"bmcvticnontimefwhm"  : "$t_{non,FWHM,\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"bmcvticnontimetot"   : "$t_{non,tot,\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"bmcvhiscogoffset"    : "$d_{CoG"+u"\u2010"+"offset,\\mathrm{CV"+u"\u2010"+"HitStats}}$",
	"bmcvdihdbmmnonlength"    : "$l_{non,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"bmcvdihabmmnonlength"    : "$l_{non,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"bmcvtrcbmmnonlength"     : "$l_{non,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TrackChar}}$",
	"bmcvticbmmnontimefwhm"   : "$t_{non,FWHM,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"bmcvticbmmnontimetot"    : "$t_{non,tot,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"bmcvdihdnonlengthfrac"   : "$l_{frac,non,\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"bmcvdihanonlengthfrac"   : "$l_{frac,non,\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"bmcvtrcnonlengthfrac"    : "$l_{frac,non,\\mathrm{CV"+u"\u2010"+"TrackChar}}$",
	"bmcvticnontimefwhmfrac"  : "$t_{frac,non,FWHM,\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"bmcvticnontimetotfrac"   : "$t_{frac,non,tot,\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"bmcvdihdbmmnonlengthfrac"    : "$l_{frac,non,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"bmcvdihabmmnonlengthfrac"    : "$l_{frac,non,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"bmcvtrcbmmnonlengthfrac"     : "$l_{frac,non,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TrackChar}}$",
	"bmcvticbmmnontimefwhmfrac"   : "$t_{frac,non,FWHM,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"bmcvticbmmnontimetotfrac"    : "$t_{frac,non,tot,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
#	"bmcvhisrelativecogoffset"    : "$d_{rel.CoG"+u"\u2010"+"offset,\\mathrm{CV"+u"\u2010"+"HitStats}}$",
	"bmcvhisrelativecogoffset"    : "$RCO_{\\mathrm{CV"+u"\u2010"+"HitStats}}$",
	"bmcvdihdlengthfillratio"     : "$LFR_{\\mathrm{CV"+u"\u2010"+"DirHitsD}}$",
	"bmcvdihalengthfillratio"     : "$LFR_{\\mathrm{CV"+u"\u2010"+"DirHitsA}}$",
	"bmcvtrclengthfillratio"      : "$LFR_{\\mathrm{CV"+u"\u2010"+"TrackChar}}$",
	"bmcvtictimefwhmfillratio"    : "$TFR_{FWHM,\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"bmcvtictimetotfillratio"     : "$TFR_{tot,\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"bmcvdihdbmmlengthfillratio"  : "$LFR_{\\mathrm{BMMap},\\mathrm{CV-DirHitsD}}$",
	"bmcvdihabmmlengthfillratio"  : "$LFR_{\\mathrm{BMMap},\\mathrm{CV-DirHitsA}}$",
	"bmcvtrcbmmlengthfillratio"   : "$LFR_{\\mathrm{BMMap},\\mathrm{CV-TrackChar}}$",
	"bmcvticbmmtimefwhmfillratio" : "$TFR_{FWHM,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"bmcvticbmmtimetotfillratio"  : "$TFR_{tot,\\mathrm{BMMap},\\mathrm{CV"+u"\u2010"+"TimeChar}}$",
	"bdtascore"           : "BDT-score (BDT A)",
	"bdtbscore"           : "BDT-score (BDT B)",
	"bdtcscore"           : "BDT-score (BDT C)",
	"bdtdscore"           : "BDT-score (BDT D)",
#	"bdtescore"           : "BDT-score (BDT E)",
	"bdtescore"           : "BDT score",
	"aeff"        : "$A_{eff}$",
	"Phi90"       : "$\Phi_{90}$",
	"Phi90sens"   : "$\Phi_{90,sens.}$",
	"Phi90sensmc" : "$\Phi_{90,sens.,BG"+u"\u2010"+"from"+u"\u2010"+"MC}$",
	}






label_nonIC = {
	"mccoszen"            : "NOPE $\\cos(zen_{\\mathrm{MC}})$",
	"mcazi"               : "NOPE $azi_{\\mathrm{MC}}$",
	"mcbeta"              : "NOPE $\\beta_{\\mathrm{MC}}$",
	"mclog10energy"       : "NOPE $\\log_{10}(E_{\\mathrm{MC}}/1 \\mathrm{GeV})$",
	"mccentrality"        : "NOPE $d_{C,\\mathrm{MC}}$",
	"mcgeomlength"        : "NOPE $l_{geom,\\mathrm{MC}}$",
	"mcgeomtime"          : "NOPE $t_{geom,\\mathrm{MC}}$",
	"bdtseparator"        : "NOPE $sep_{\mathrm{BDT}}$",
	"bdtistest"           : "NOPE $istest_{\mathrm{BDT}}$",
	"ptlog10npe"          : "$\\log_{10}(n_{photo-electrons})$",
	"ptnch"               : "$n_{channels}$",
	"ptrhope"             : "$\\rho_{photo-electrons}$",
	"opcoszen"            : "NOPE $\\cos(zen_{\\mathrm{Ophelia}})$",
	"opazi"               : "NOPE $azi_{\\mathrm{Ophelia}}$",
	"opbeta"              : "NOPE $\\beta_{\\mathrm{Ophelia}}$",
	"opfitquality"        : "NOPE $\\chi^2_{red,\\mathrm{Ophelia}}$",
	"opcentrality"        : "NOPE $d_{C,\\mathrm{Ophelia}}$",
	"opgeomlength"        : "NOPE $l_{geom,\\mathrm{Ophelia}}$",
	"opgeomtime"          : "NOPE $t_{geom,\\mathrm{Ophelia}}$",
	"bmcoszen"            : "NOPE $\\cos(zen_{\\mathrm{BM}})$",
	"bmazi"               : "NOPE $azi_{\\mathrm{BM}}$",
	"bmbeta"              : "NOPE $\\beta_{\\mathrm{BM}}$",
	"bmcentrality"        : "NOPE $d_{C,\\mathrm{BM}}$",
	"bmgeomlength"        : "NOPE $l_{geom,\\mathrm{BM}}$",
	"bmgeomtime"          : "NOPE $t_{geom,\\mathrm{BM}}$",
	"cvdihdlength"        : "NOPE $l_{\\mathrm{CV-DirHitsD}}$",
	"cvdihdsmoothness"    : "NOPE $smoothness_{\\mathrm{CV-DirHitsD}}$",
	"cvdihdqdirect"       : "NOPE $Q_{direct,\\mathrm{CV-DirHitsD}}$",
	"cvdihdqearly"        : "NOPE $Q_{early,\\mathrm{CV-DirHitsD}}$",
	"cvdihdqlate"         : "NOPE $Q_{late,\\mathrm{CV-DirHitsD}}$",
	"cvdihalength"        : "NOPE $l_{\\mathrm{CV-DirHitsA}}$",
	"cvdihasmoothness"    : "NOPE $smoothness_{\\mathrm{CV-DirHitsA}}$",
	"cvdihaqdirect"       : "NOPE $Q_{direct,\\mathrm{CV-DirHitsA}}$",
	"cvdihaqearly"        : "NOPE $Q_{early,\\mathrm{CV-DirHitsA}}$",
	"cvdihaqlate"         : "NOPE $Q_{late,\\mathrm{CV-DirHitsA}}$",
	"cvhiscog"            : "NOPE $r_{CoG,\\mathrm{CV-HitStats}}$",
	"cvtictimefwhm"       : "NOPE $t_{FWHM,\\mathrm{CV-TimeChar}}$",
	"cvtictimetot"        : "NOPE $t_{tot,\\mathrm{CV-TimeChar}}$",
	"cvtrclength"         : "NOPE $l_{\\mathrm{CV-TrackChar}}$",
	"cvtrcsmoothness"     : "NOPE $smoothness_{\\mathrm{CV-TrackChar}}$",
	"cvtrcavgdistq"       : "NOPE $\mathrm{avg}(d_{\\mathrm{DOM},Q})_\\mathrm{CV-TrackChar}$",
	"cvdihabmmlength"     : "NOPE $l_{\\mathrm{BMMap},\\mathrm{CV-DirHitsA}}$",
	"cvdihabmmsmoothness" : "NOPE $smoothness_{\\mathrm{BMMap},\\mathrm{CV-DirHitsA}}$",
	"cvdihabmmqdirect"    : "NOPE $Q_{direct,\\mathrm{BMMap},\\mathrm{CV-DirHitsA}}$",
	"cvdihabmmqearly"     : "NOPE $Q_{early,\\mathrm{BMMap},\\mathrm{CV-DirHitsA}}$",
	"cvdihabmmqlate"      : "NOPE $Q_{late,\\mathrm{BMMap},\\mathrm{CV-DirHitsA}}$",
	"cvdihdbmmlength"     : "NOPE $l_{\\mathrm{BMMap},\\mathrm{CV-DirHitsD}}$",
	"cvdihdbmmsmoothness" : "NOPE $smoothness_{\\mathrm{BMMap},\\mathrm{CV-DirHitsD}}$",
	"cvdihdbmmqdirect"    : "NOPE $Q_{direct,\\mathrm{BMMap},\\mathrm{CV-DirHitsA}}$",
	"cvdihdbmmqearly"     : "NOPE $Q_{early,\\mathrm{BMMap},\\mathrm{CV-DirHitsA}}$",
	"cvdihdbmmqlate"      : "NOPE $Q_{late,\\mathrm{BMMap},\\mathrm{CV-DirHitsA}}$",
	"cvtrcbmmlength"      : "NOPE $l_{\\mathrm{BMMap},\\mathrm{CV-TrachChar}}$",
	"cvtrcbmmsmoothness"  : "NOPE $smoothness_{\\mathrm{BMMap},\\mathrm{CV-TrachChar}}$",
	"cvtrcbmmavgdistq"    : "NOPE $\mathrm{avg}(d_{\\mathrm{DOM},Q})_{\\mathrm{BMMap},\\mathrm{CV-TrackChar}}$",
	"cvticbmmtimefwhm"    : "NOPE $t_{FWHM,\\mathrm{BMMap},\\mathrm{CV-TimeChar}}$",
	"cvticbmmtimetot"     : "NOPE $t_{tot,\\mathrm{BMMap},\\mathrm{CV-TimeChar}}$",
	"mpavge"              : "NOPE $\\mathrm{avg}(E_{\\mathrm{MIL}})$",
	"mpstde"              : "NOPE $\\mathrm{std}(E_{\\mathrm{MIL}})$",
	"mprsde"              : "NOPE $\\mathrm{rsd}(E_{\\mathrm{MIL}})$",
	"coavgx"              : "NOPE $\\mathrm{avg}(x_{\\mathrm{Cherenkov-offset}})$",
	"costdx"              : "NOPE $\\mathrm{std}(x_{\\mathrm{Cherenkov-offset}})$",
	"corsdx"              : "NOPE $\\mathrm{rsd}(x_{\\mathrm{Cherenkov-offset}})$",
	"coavgt"              : "NOPE $\\mathrm{avg}(t_{\\mathrm{Cherenkov-offset}})$",
	"costdt"              : "NOPE $\\mathrm{std}(t_{\\mathrm{Cherenkov-offset}})$",
	"corsdt"              : "NOPE $\\mathrm{rsd}(t_{\\mathrm{Cherenkov-offset}})$",
	"ftxanpe"             : "NOPE $l\\times A_{n_{pe},\\mathrm{Frank-Tamm}}$",
	"ftanpelgeom"         : "NOPE $A_{geom,n_{pe},\\mathrm{Frank-Tamm}}$",
	"ftanpeldihd"         : "NOPE $A_{geom,n_{pe},\\mathrm{Frank-Tamm}}$",
	"ftanpeldiha"         : "NOPE $A_{geom,n_{pe},\\mathrm{Frank-Tamm}}$",
	"ftanpeltrc"          : "NOPE $A_{geom,n_{pe},\\mathrm{Frank-Tamm}}$",
	"ftxaqdihd"           : "NOPE $l\\times A_{Q_{\\mathrm{DirHitsD}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihdlgeom"       : "NOPE $A_{geom,Q_{\\mathrm{DirHitsD}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihdldihd"       : "NOPE $A_{CV-DiH-D,Q_{\\mathrm{DirHitsD}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihdldiha"       : "NOPE $A_{CV-DiH-A,Q_{\\mathrm{DirHitsD}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihdltrc"        : "NOPE $A_{CV-TrC,Q_{\\mathrm{DirHitsD}},\\mathrm{Frank-Tamm}}$",
	"ftxaqdiha"           : "NOPE $l\\times A_{Q_{\\mathrm{DirHitsA}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihalgeom"       : "NOPE $A_{geom,Q_{\\mathrm{DirHitsA}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihaldihd"       : "NOPE $A_{CV-DiH-D,Q_{\\mathrm{DirHitsA}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihaldiha"       : "NOPE $A_{CV-DiH-A,Q_{\\mathrm{DirHitsA}},\\mathrm{Frank-Tamm}}$",
	"ftaqdihaltrc"        : "NOPE $A_{CV-TrC,Q_{\\mathrm{DirHitsA}},\\mathrm{Frank-Tamm}}$",
	"mcopbetadiff"        : "NOPE $\\beta_{\\mathrm{MC}}-\\beta_{\\mathrm{Ophelia}}$",
	"mcbmbetadiff"        : "NOPE $\\beta_{\\mathrm{MC}}-\\beta_{\\mathrm{BM}}$",
	"bmcvdihdnonlength"   : "NOPE $l_{non,\\mathrm{CV-DirHitsD}}$",
	"bmcvdihanonlength"   : "NOPE $l_{non,\\mathrm{CV-DirHitsA}}$",
	"bmcvtrcnonlength"    : "NOPE $l_{non,\\mathrm{CV-TrackChar}}$",
	"bmcvticnontimefwhm"  : "NOPE $t_{non,FWHM,\\mathrm{CV-TimeChar}}$",
	"bmcvticnontimetot"   : "NOPE $t_{non,tot,\\mathrm{CV-TimeChar}}$",
	"bmcvhiscogoffset"    : "NOPE $d_{CoG-offset,\\mathrm{CV-HitStats}}$",
	"bmcvdihdbmmnonlength"    : "NOPE $l_{non,\\mathrm{BMMap},\\mathrm{CV-DirHitsD}}$",
	"bmcvdihabmmnonlength"    : "NOPE $l_{non,\\mathrm{BMMap},\\mathrm{CV-DirHitsA}}$",
	"bmcvtrcbmmnonlength"     : "NOPE $l_{non,\\mathrm{BMMap},\\mathrm{CV-TrackChar}}$",
	"bmcvticbmmnontimefwhm"   : "NOPE $t_{non,FWHM,\\mathrm{BMMap},\\mathrm{CV-TimeChar}}$",
	"bmcvticbmmnontimetot"    : "NOPE $t_{non,tot,\\mathrm{BMMap},\\mathrm{CV-TimeChar}}$",
	"bmcvdihdnonlengthfrac"   : "NOPE $l_{frac,non,\\mathrm{CV-DirHitsD}}$",
	"bmcvdihanonlengthfrac"   : "NOPE $l_{frac,non,\\mathrm{CV-DirHitsA}}$",
	"bmcvtrcnonlengthfrac"    : "NOPE $l_{frac,non,\\mathrm{CV-TrackChar}}$",
	"bmcvticnontimefwhmfrac"  : "NOPE $t_{frac,non,FWHM,\\mathrm{CV-TimeChar}}$",
	"bmcvticnontimetotfrac"   : "NOPE $t_{frac,non,tot,\\mathrm{CV-TimeChar}}$",
	"bmcvdihdbmmnonlengthfrac"    : "NOPE $l_{frac,non,\\mathrm{BMMap},\\mathrm{CV-DirHitsD}}$",
	"bmcvdihabmmnonlengthfrac"    : "NOPE $l_{frac,non,\\mathrm{BMMap},\\mathrm{CV-DirHitsA}}$",
	"bmcvtrcbmmnonlengthfrac"     : "NOPE $l_{frac,non,\\mathrm{BMMap},\\mathrm{CV-TrackChar}}$",
	"bmcvticbmmnontimefwhmfrac"   : "NOPE $t_{frac,non,FWHM,\\mathrm{BMMap},\\mathrm{CV-TimeChar}}$",
	"bmcvticbmmnontimetotfrac"    : "NOPE $t_{frac,non,tot,\\mathrm{BMMap},\\mathrm{CV-TimeChar}}$",
	"bmcvhisrelativecogoffset"    : "Relative hit-CoG Offset",
	"bmcvdihdlengthfillratio"     : "Length-Fill-Ratio",
	"bmcvdihalengthfillratio"     : "Length-Fill-Ratio",
	"bmcvtrclengthfillratio"      : "Length-Fill-Ratio",
	"bmcvtictimefwhmfillratio"    : "Time-Fill-Ratio",
	"bmcvtictimetotfillratio"     : "Time-Fill-Ratio",
	"bmcvdihdbmmlengthfillratio"  : "Length-Fill-Ratio",
	"bmcvdihabmmlengthfillratio"  : "Length-Fill-Ratio",
	"bmcvtrcbmmlengthfillratio"   : "Length-Fill-Ratio",
	"bmcvticbmmtimefwhmfillratio" : "Time-Fill-Ratio",
	"bmcvticbmmtimetotfillratio"  : "Time-Fill-Ratio",
	"bdtascore"                   : "BDT-score (BDT A)",
	"bdtbscore"                   : "BDT-score (BDT B)",
	"bdtcscore"                   : "BDT-score (BDT C)",
	"bdtdscore"                   : "BDT-score (BDT D)",
#	"bdtescore"                   : "BDT-score (BDT E)",
	"bdtescore"                   : "BDT score",
	"aeff"                        : "Effective Area",
	"Phi90"                       : "$\Phi_{90}$",
	"Phi90sens"                   : "$\Phi_{90,sens.}$",
	"Phi90sensres"                 : "$\Phi_{90,sens.,BG=0}$",
	}





unit = {
	"mccoszen"            : "",
	"mcazi"               : "rad",
	"mcbeta"              : "",
	"mclog10energy"       : "",
	"mccentrality"        : "m",
	"mcgeomlength"        : "m",
	"mcgeomtime"          : "ns",
	"bdtseparator"        : "",
	"bdtistest"           : "",
	"ptlog10npe"          : "",
	"ptnch"               : "",
	"ptrhope"             : "",
	"opcoszen"            : "",
	"opazi"               : "rad",
	"opbeta"              : "",
	"opfitquality"        : "",
	"opcentrality"        : "m",
	"opgeomlength"        : "m",
	"opgeomtime"          : "ns",
	"bmcoszen"            : "",
	"bmazi"               : "rad",
	"bmbeta"              : "",
	"bmcentrality"        : "m",
	"bmgeomlength"        : "m",
	"bmgeomtime"          : "ns",
	"cvdihdlength"        : "m",
	"cvdihdsmoothness"    : "",
	"cvdihdqdirect"       : "e",
	"cvdihdqearly"        : "e",
	"cvdihdqlate"         : "e",
	"cvdihalength"        : "m",
	"cvdihasmoothness"    : "",
	"cvdihaqdirect"       : "e",
	"cvdihaqearly"        : "e",
	"cvdihaqlate"         : "e",
	"cvhiscog"            : "m",
	"cvtictimefwhm"       : "ns",
	"cvtictimetot"        : "ns",
	"cvtrclength"         : "m",
	"cvtrcsmoothness"     : "",
	"cvtrcavgdistq"       : "m",
	"cvdihabmmlength"     : "m",
	"cvdihabmmsmoothness" : "",
	"cvdihabmmqdirect"       : "e",
	"cvdihabmmqearly"        : "e",
	"cvdihabmmqlate"         : "e",
	"cvdihdbmmlength"     : "m",
	"cvdihdbmmsmoothness" : "",
	"cvdihdbmmqdirect"       : "e",
	"cvdihdbmmqearly"        : "e",
	"cvdihdbmmqlate"         : "e",
	"cvtrcbmmlength"      : "m",
	"cvtrcbmmsmoothness"  : "",
	"cvtrcbmmavgdistq"    : "m",
	"cvticbmmtimefwhm"    : "ns",
	"cvticbmmtimetot"     : "ns",
	"mpavge"              : "GeV",
	"mpstde"              : "GeV",
	"mprsde"              : "",
	"coavgx"              : "m",
	"costdx"              : "m",
	"corsdx"              : "",
	"coavgt"              : "ns",
	"costdt"              : "ns",
	"corsdt"              : "",
	"ftxanpe"             : "m",
	"ftanpelgeom"         : "",
	"ftanpeldihd"         : "",
	"ftanpeldiha"         : "",
	"ftanpeltrc"          : "",
	"ftxaqdihd"           : "m",
	"ftaqdihdlgeom"       : "",
	"ftaqdihdldihd"       : "",
	"ftaqdihdldiha"       : "",
	"ftaqdihdltrc"        : "",
	"ftxaqdiha"           : "m",
	"ftaqdihalgeom"       : "",
	"ftaqdihaldihd"       : "",
	"ftaqdihaldiha"       : "",
	"ftaqdihaltrc"        : "",
	"mcopbetadiff"        : "",
	"mcbmbetadiff"        : "",
	"bmcvdihdnonlength"   : "m",
	"bmcvdihanonlength"   : "m",
	"bmcvtrcnonlength"    : "m",
	"bmcvticnontimefwhm"  : "ns",
	"bmcvticnontimetot"   : "ns",
	"bmcvhiscogoffset"    : "m",
	"bmcvdihdbmmnonlength"    : "m",
	"bmcvdihabmmnonlength"    : "m",
	"bmcvtrcbmmnonlength"     : "m",
	"bmcvticbmmnontimefwhm"   : "ns",
	"bmcvticbmmnontimetot"    : "ns",
	"bmcvdihdnonlengthfrac"   : "",
	"bmcvdihanonlengthfrac"   : "",
	"bmcvtrcnonlengthfrac"    : "",
	"bmcvticnontimefwhmfrac"  : "",
	"bmcvticnontimetotfrac"   : "",
	"bmcvdihdbmmnonlengthfrac"    : "",
	"bmcvdihabmmnonlengthfrac"    : "",
	"bmcvtrcbmmnonlengthfrac"     : "",
	"bmcvticbmmnontimefwhmfrac"   : "",
	"bmcvticbmmnontimetotfrac"    : "",
	"bmcvhisrelativecogoffset"    : "",
	"bmcvdihdlengthfillratio"     : "",
	"bmcvdihalengthfillratio"     : "",
	"bmcvtrclengthfillratio"      : "",
	"bmcvtictimefwhmfillratio"    : "",
	"bmcvtictimetotfillratio"     : "",
	"bmcvdihdbmmlengthfillratio"  : "",
	"bmcvdihabmmlengthfillratio"  : "",
	"bmcvtrcbmmlengthfillratio"   : "",
	"bmcvticbmmtimefwhmfillratio" : "",
	"bmcvticbmmtimetotfillratio"  : "",
	"bdtascore"           : "",
	"bdtbscore"           : "",
	"bdtcscore"           : "",
	"bdtdscore"           : "",
	"bdtescore"           : "",
	"aeff"        : "km2",
	"Phi90"       : "cm-2 s-1 sr-1",
	"Phi90sens"   : "cm-2 s-1 sr-1",
	"Phi90sensmc" : "cm-2 s-1 sr-1",
	}



#flav = { the_key: { flav: "" for flav in all_flavs+["nutot"] } for the_key in [ "legend", "legend_short", "color", "key" ] }
flav_legend = {}
flav_legend["monopole"]       = "Magnetic Monopole"
flav_legend["nue"]            = "Electron Neutrino"
flav_legend["numu"]           = "Muon Neutrino"
flav_legend["nutau"]          = "Tauon Neutrino"
flav_legend["nutot"]          = "Neutrino Total"
flav_legend["unknown"]        = "Exprm. Data"
flav_legend_short = {}
flav_legend_short["monopole"] = "$MM$"
flav_legend_short["nue"]      = "$\\nu_{e}$"
flav_legend_short["numu"]     = "$\\nu_{\\mu}$"
flav_legend_short["nutau"]    = "$\\nu_{\\tau}$"
flav_legend_short["nutot"]    = "$\\nu_{tot}$"
flav_legend_short["unknown"]  = "$exprm$"
flav_color = {}
#flav_color["monopole"]        = "red"
#flav_color["nue"]             = "royalblue"
#flav_color["numu"]            = "c"
#flav_color["nutau"]           = "seagreen"
#flav_color["nutot"]           = "orange"
#flav_color["unknown"]         = "black"
flav_color["monopole"]        = "red"
flav_color["nue"]             = "orange"
flav_color["numu"]            = "c"
flav_color["nutau"]           = "orchid"
flav_color["nutot"]           = "royalblue"
flav_color["unknown"]         = "seagreen"
flav_linestyle = {}
flav_linestyle["monopole"]    = "solid"
flav_linestyle["nue"]         = "solid" # "dashed" # "dotted"
flav_linestyle["numu"]        = "solid" # "dashed" # "dashed"
flav_linestyle["nutau"]       = "solid" # "dashed" # "dashdot"
flav_linestyle["nutot"]       = "solid"
flav_linestyle["unknown"]     = "solid"
flav_linewidth = {}
flav_linewidth["monopole"]    = 1.5
flav_linewidth["nue"]         = 1.
flav_linewidth["numu"]        = 1.
flav_linewidth["nutau"]       = 1.
flav_linewidth["nutot"]       = 1.5
flav_linewidth["unknown"]     = 1.5
flav_key = {}
flav_key["monopole"]          = "flav_05"
flav_key["nue"]               = "flav_02"
flav_key["numu"]              = "flav_03"
flav_key["nutau"]             = "flav_04"
flav_key["nutot"]             = "flav_01"
flav_key["unknown"]           = "flav_06"
flav_legend_order = {}
flav_legend_order["monopole"] = 0
flav_legend_order["nue"]      = 2
flav_legend_order["numu"]     = 3
flav_legend_order["nutau"]    = 4
flav_legend_order["nutot"]    = 1
flav_legend_order["unknown"]  = 5





lev_legend = {}
lev_legend["gen"]     = "Generation"
lev_legend["trigg"]   = "Trigger"
lev_legend["ehefilt"] = "EHE filter"
lev_legend["L2"]      = "Step I (L2)"
lev_legend["L3"]      = "Step I (L3)"
lev_legend["L4"]      = "Step I (L4)"
lev_legend["L5"]      = "Step I (L5)"
lev_legend["L6"]      = "Step II (L6)"
lev_legend_short = {}
lev_legend_short["gen"]     = "Gen"
lev_legend_short["trigg"]   = "Trigg"
lev_legend_short["ehefilt"] = "EHE filt"
lev_legend_short["L2"]      = "L2"
lev_legend_short["L3"]      = "L3"
lev_legend_short["L4"]      = "L4"
lev_legend_short["L5"]      = "L5"
lev_legend_short["L6"]      = "L6"
lev_legend_nonIC = {}
lev_legend_nonIC["gen"]     = "Generated"
lev_legend_nonIC["trigg"]   = "Trigger"
lev_legend_nonIC["ehefilt"] = "EHE filter"
lev_legend_nonIC["L2"]      = "Step I L2"
lev_legend_nonIC["L3"]      = "Step I L3"
lev_legend_nonIC["L4"]      = "Step I L4"
lev_legend_nonIC["L5"]      = "Step I"
lev_legend_nonIC["L6"]      = "Step II"
lev_name = {}
lev_name["gen"]     = "G0_gen"
lev_name["trigg"]   = "L0_trigg"
lev_name["ehefilt"] = "L1_filt"
lev_name["L2"]      = "L2_ana"
lev_name["L3"]      = "L3_atmnu"
lev_name["L4"]      = "L4_atmmu"
lev_name["L5"]      = "L5_itveto"
lev_name["L6"]      = "L6_astnu"
lev_color = {}
#lev_color["gen"]     = "mediumseagreen"
#lev_color["trigg"]   = "mediumturquoise"
#lev_color["ehefilt"] = "royalblue"
#lev_color["L2"]      = "c"
#lev_color["L3"]      = "orchid"
#lev_color["L4"]      = "orange"
#lev_color["L5"]      = "red"
#lev_color["L6"]      = "seagreen"
lev_color["gen"]     = "orchid"
lev_color["trigg"]   = "royalblue"
lev_color["ehefilt"] = "c"
lev_color["L2"]      = "k"
lev_color["L3"]      = "k"
lev_color["L4"]      = "k"
lev_color["L5"]      = "orange"
lev_color["L6"]      = "seagreen"
lev_key = {}
lev_key["gen"]     = "lev_a"
lev_key["trigg"]   = "lev_b"
lev_key["ehefilt"] = "lev_c"
lev_key["L2"]      = "lev_d"
lev_key["L3"]      = "lev_e"
lev_key["L4"]      = "lev_f"
lev_key["L5"]      = "lev_g"
lev_key["L6"]      = "lev_h"


syst_legend = {}
syst_legend["baseline"]             = "Baseline"
syst_legend["domeff_plus"]          = "DOM Efficiency +10 %"
syst_legend["domeff_minus"]         = "DOM Efficiency -10 %"
syst_legend["scat_plus_abs_plus"]   = "Scat. +5 %, Abs. +5 %"
syst_legend["scat_plus_abs_minus"]  = "Scat. +5 %, Abs. -5 %"
syst_legend["scat_minus_abs_plus"]  = "Scat. -5 %, Abs. +5 %"
syst_legend["scat_minus_abs_minus"] = "Scat. -5 %, Abs. -5 %"
syst_legend["angsens_set05"]        = "Ang. Sens. set 5"
syst_legend["angsens_set09"]        = "Ang. Sens. set 9"
syst_legend["angsens_set10"]        = "Ang. Sens. set 10"
syst_legend["angsens_set14"]        = "Ang. Sens. set 14"
syst_legend["p1_0.20_p2_0"]         = "$p_1=0.20$, $p_2=0$"
syst_legend["p1_0.25_p2_-3"]        = "$p_1=0.25$, $p_2=-3$"
syst_legend["p1_0.25_p2_-1"]        = "$p_1=0.25$, $p_2=-1$"
syst_legend["p1_0.25_p2_0"]         = "$p_1=0.25$, $p_2=0$"
syst_legend["p1_0.25_p2_+1"]        = "$p_1=0.25$, $p_2=1$"
syst_legend["p1_0.30_p2_-3"]        = "$p_1=0.30$, $p_2=-3$"
syst_legend["p1_0.30_p2_-1"]        = "$p_1=0.30$, $p_2=-1$"
syst_legend["p1_0.30_p2_0"]         = "$p_1=0.30$, $p_2=0$"
syst_legend["p1_0.30_p2_+1"]        = "$p_1=0.30$, $p_2=1$"
syst_legend["p1_0.35_p2_0"]         = "$p_1=0.35$, $p_2=0$"
syst_color = {}
syst_color["baseline"]             = "black"
syst_color["domeff_plus"]          = "orchid"
syst_color["domeff_minus"]         = "orange"
syst_color["scat_plus_abs_plus"]   = "orchid"
syst_color["scat_plus_abs_minus"]  = "darkturquoise"
syst_color["scat_minus_abs_plus"]  = "green"
syst_color["scat_minus_abs_minus"] = "orange"
syst_color["angsens_set05"]        = "orchid"
syst_color["angsens_set09"]        = "darkturquoise"
syst_color["angsens_set10"]        = "green"
syst_color["angsens_set14"]        = "orange"
syst_color["p1_0.20_p2_0"]         = "orange"
syst_color["p1_0.25_p2_-3"]        = "firebrick"
syst_color["p1_0.25_p2_-1"]        = "crimson"
syst_color["p1_0.25_p2_0"]         = "orchid"
syst_color["p1_0.25_p2_+1"]        = "mediumpurple"
syst_color["p1_0.30_p2_-3"]        = "blue"
syst_color["p1_0.30_p2_-1"]        = "darkturquoise"
syst_color["p1_0.30_p2_0"]         = "mediumseagreen"
syst_color["p1_0.30_p2_+1"]        = "green"
syst_color["p1_0.35_p2_0"]         = "olivedrab"
syst_key = {}
syst_key["baseline"]             = "syst_z"
syst_key["domeff_plus"]          = "syst_a"
syst_key["domeff_minus"]         = "syst_b"
syst_key["scat_plus_abs_plus"]   = "syst_e"
syst_key["scat_plus_abs_minus"]  = "syst_f"
syst_key["scat_minus_abs_plus"]  = "syst_g"
syst_key["scat_minus_abs_minus"] = "syst_h"
syst_key["angsens_set05"]        = "syst_i"
syst_key["angsens_set09"]        = "syst_j"
syst_key["angsens_set10"]        = "syst_k"
syst_key["angsens_set14"]        = "syst_l"
syst_key["p1_0.20_p2_0"]         = "syst_m"
syst_key["p1_0.25_p2_-3"]        = "syst_n"
syst_key["p1_0.25_p2_-1"]        = "syst_o"
syst_key["p1_0.25_p2_0"]         = "syst_p"
syst_key["p1_0.25_p2_+1"]        = "syst_q"
syst_key["p1_0.30_p2_-3"]        = "syst_r"
syst_key["p1_0.30_p2_-1"]        = "syst_s"
syst_key["p1_0.30_p2_0"]         = "syst_t"
syst_key["p1_0.30_p2_+1"]        = "syst_u"
syst_key["p1_0.35_p2_0"]         = "syst_v"



spectr_legend = {}
spectr_legend["numudif2017_central"]    = "$\\Phi[\\nu_\\mu^{DIF},2017]$, nominal"
spectr_legend["numudif2017_plussigma"]  = "$\\Phi[\\nu_\\mu^{DIF},2017]$, $+1\\sigma$"
spectr_legend["numudif2017_minussigma"] = "$\\Phi[\\nu_\\mu^{DIF},2017]$, $-1\\sigma$"
spectr_legend["numudif2019_central"]    = "$\\Phi[\\nu_\\mu^{DIF},2019]$, nominal"
spectr_legend["numudif2019_plussigma"]  = "$\\Phi[\\nu_\\mu^{DIF},2019]$, $+1\\sigma$"
spectr_legend["numudif2019_minussigma"] = "$\\Phi[\\nu_\\mu^{DIF},2019]$, $-1\\sigma$"
spectr_legend["hese2019_central"]       = "$\\Phi[HESE,2019]$, nominal"
spectr_legend["hese2019_plussigma"]     = "$\\Phi[HESE,2019]$, $+1\\sigma$"
spectr_legend["hese2019_minussigma"]    = "$\\Phi[HESE,2019]$, $-1\\sigma$"
spectr_legend_short = {}
spectr_legend_short["numudif2017_central"]    = "$\\nu_\\mu^{DIF}$, 2017"
spectr_legend_short["numudif2017_plussigma"]  = "$\\nu_\\mu^{DIF}$, 2017"
spectr_legend_short["numudif2017_minussigma"] = "$\\nu_\\mu^{DIF}$, 2017"
spectr_legend_short["numudif2019_central"]    = "$\\nu_\\mu^{DIF}$, 2019"
spectr_legend_short["numudif2019_plussigma"]  = "$\\nu_\\mu^{DIF}$, 2019"
spectr_legend_short["numudif2019_minussigma"] = "$\\nu_\\mu^{DIF}$, 2019"
spectr_legend_short["hese2019_central"]       = "$HESE$, 2019"
spectr_legend_short["hese2019_plussigma"]     = "$HESE$, 2019"
spectr_legend_short["hese2019_minussigma"]    = "$HESE$, 2019"
spectr_color = {}
spectr_color["numudif2017_central"]    = "red"
spectr_color["numudif2017_plussigma"]  = "red"
spectr_color["numudif2017_minussigma"] = "red"
spectr_color["numudif2019_central"]    = "green"
spectr_color["numudif2019_plussigma"]  = "green"
spectr_color["numudif2019_minussigma"] = "green"
spectr_color["hese2019_central"]       = "orange"
spectr_color["hese2019_plussigma"]     = "orange"
spectr_color["hese2019_minussigma"]    = "orange"
spectr_key = {}
spectr_key["numudif2017_central"]    = "spectr_o"
spectr_key["numudif2017_plussigma"]  = "spectr_n"
spectr_key["numudif2017_minussigma"] = "spectr_m"
spectr_key["numudif2019_central"]    = "spectr_i"
spectr_key["numudif2019_plussigma"]  = "spectr_h"
spectr_key["numudif2019_minussigma"] = "spectr_g"
spectr_key["hese2019_central"]       = "spectr_c"
spectr_key["hese2019_plussigma"]     = "spectr_b"
spectr_key["hese2019_minussigma"]    = "spectr_a"





