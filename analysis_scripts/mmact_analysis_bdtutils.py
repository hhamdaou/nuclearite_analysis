
bdttrainfraction = 1./4

bdtvars = {
#	"bdta": [ # The Conservative
#		"ptlog10npe"        ,
#		"bmcoszen"          , "bmbeta"            ,
#		"mprsde"            ,
#	],
#	"bdtb": [ # The Moderate
#		"ptlog10npe"        , "ptnch"             ,
#		"bmcoszen"          , "bmbeta"            , "bmcentrality"      ,
#		"cvtictimefwhm"     , "cvtrclength"       , "cvtrcavgdistq"     ,
#	],
#	"bdtc": [ # The Modernist
#		"ptlog10npe"        , "ptnch"             , "ptrhope"           , 
#		"bmcoszen"          , "bmbeta"            , "bmcentrality"      ,
#		"mprsde"            , "corsdx"            , "corsdt"            , 
#		"bmcvdihdlengthfillratio" , "bmcvdihalengthfillratio" , "bmcvtrclengthfillratio"  , 
#		"bmcvtictimefwhmfillratio", "bmcvtictimetotfillratio" , "bmcvhisrelativecogoffset"  , 
#	],
#	"bdtd": [ # The Inclusive
#		"ptlog10npe"        , "ptnch"             , "ptrhope"           , 
#		"bmcoszen"          , "bmazi"             , "bmbeta"            , "bmcentrality"      , "bmgeomlength"      , "bmgeomtime"        , 
#		"cvdihdlength"      , "cvdihdsmoothness"  , #"cvdihdqdirect"     , "cvdihdqearly"      , "cvdihdqlate"       , 
#		"cvdihalength"      , "cvdihasmoothness"  , #"cvdihaqdirect"     , "cvdihaqearly"      , "cvdihaqlate"       , 
#		"cvhiscog"          , "cvtictimefwhm"     , "cvtictimetot"      , "cvtrclength"       , "cvtrcsmoothness"   , "cvtrcavgdistq"     , 
#		"mpavge"            , "mpstde"            , "mprsde"            , 
#		"coavgx"            , "costdx"            , "corsdx"            , "coavgt"            , "costdt"            , "corsdt"            , 
#		"bmcvdihdlengthfillratio" , "bmcvdihalengthfillratio" , "bmcvtrclengthfillratio"  , 
#		"bmcvtictimefwhmfillratio", "bmcvtictimetotfillratio" , "bmcvhisrelativecogoffset"  , 
#	],
	"bdte": [ # The Realist
		"ptlog10npe"        , #"ptnch"             , #"ptrhope"           ,
		"bmcoszen"          , "bmbeta"            , "bmcentrality"      ,
		"cvtictimefwhm"     ,
		"cvtrcavgdistq"     ,
		"mprsde"            ,
		"bmcvtrclengthfillratio"  ,
		"bmcvhisrelativecogoffset"  ,
	],
	"bdte_thesisorder": [ # The Realist
		"bmbeta"            , 
		"cvtictimefwhm"     ,
		"cvtrcavgdistq"     ,
		"mprsde"            ,
		"bmcvtrclengthfillratio"  ,
		"bmcvhisrelativecogoffset"  ,
		"ptlog10npe"        ,
		"bmcoszen"          ,
		"bmcentrality"      ,
	],
}

bdtnames = sorted(bdtvars.keys())

bdtcutvalues = {
#	"bdta": 1.,
#	"bdtb": 1.,
#	"bdtc": 1.,
#	"bdtd": 1.,
	"bdte": 1.,
}

bdt_script_train = "$I3_SRC/pybdt/resources/scripts/train.py"

#bdtcaptions = {
##	"bdta": "The Conservative",
##	"bdtb": "The Moderate",
##	"bdtc": "The Modernist",
##	"bdtd": "The Inclusive",
#	"bdte": "The Realist",
#}
