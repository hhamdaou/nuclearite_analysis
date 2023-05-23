import os, sys
#import time, random, os, sys, json
import numpy as np
#import scipy.constants as sc
#import matplotlib
#from matplotlib.colors import LogNorm

#from icecube import icetray#, dataclasses, dataio, tableio, common_variables, improvedLinefit, portia#, recclasses, sim_services, phys_services
#from icecube.icetray import I3Units
#from icecube.dataclasses import I3MCTree, I3Particle, I3RecoPulseSeriesMap, I3RecoPulse, I3MapStringDouble
#from icecube.tableio import I3TableWriter
#from icecube.hdfwriter import I3HDFTableService
#from I3Tray import *




# from Anna Pollmann
def get_feldmancousins_upperlimit( n_bg, n_ob, confidence=0.90 ):
	import numpy as np
	if np.isnan(n_bg) or np.isnan(n_ob):
		return np.nan
	#else:
	from ROOT import TFeldmanCousins
	f = TFeldmanCousins( confidence )
	return f.CalculateUpperLimit( n_ob, n_bg )

def get_feldmancousins_lowerlimit( n_bg, n_ob, confidence=0.90 ):
	import numpy as np
	if np.isnan(n_bg) or np.isnan(n_ob):
		return np.nan
	#else:
	from ROOT import TFeldmanCousins
	f = TFeldmanCousins( confidence )
	return f.CalculateLowerLimit( n_ob, n_bg )

def get_feldmancousins_sensitivity_DEPRECATED( n_bg, confidence=0.90, end_n_ob=29, give_std=False ):
	import numpy as np
	if np.isnan(n_bg):
		return np.nan
	#else:
	n_ob = np.arange(end_n_ob)
	mu_fc = np.array([get_feldmancousins_upperlimit(n_bg, n, confidence) for n in n_ob])
	coeff_a = n_bg**n_ob * np.exp(-n_bg)
	coeff_b = 1./np.array([np.math.factorial(n) for n in n_ob])
	if not give_std:
		return sum(mu_fc*coeff_a*coeff_b)
	#else:
	return sum(mu_fc*coeff_a*coeff_b), np.nan, np.nan

def get_poisson(k,mu):
	import scipy as sp
	import scipy.stats as spst
	if k!=int(k):
		return (np.exp(-mu) * mu**k / np.math.gamma(k+1))
	elif mu==0:
		return (np.exp(-mu) * mu**k / np.math.factorial(k))
	else:
		return spst.poisson.pmf(k,mu)

def get_poisson_arr(klow,mu,kend=100):
	def get_linspace_mostly_integers(klow,kend):
		if kend!=int(kend):
			exit("Damn, this is not supposed to happen")
		if klow!=int(klow):
			return np.concatenate((np.array([klow]),np.linspace(int(klow)+1,kend,kend-(int(klow)+1)+1)))
		else:
			return np.linspace(klow,kend,kend-klow+1)
	return np.array([ get_poisson(k,mu) for k in get_linspace_mostly_integers(klow,kend) ]), get_linspace_mostly_integers(klow,kend)

def get_ncrit_from_poisson(n_bg,alpha=5.733e-7):
	# alpha=5.733e-7 corresponds to the 5 sigma two-sided tails of a Gaussian
	# alpha=2.700e-3 corresponds to the 3 sigma two-sided tails of a Gaussian
	import numpy as np
	P_arr, n_arr = get_poisson_arr(0,n_bg)
	P_sum_arr = np.cumsum(P_arr[::-1])[::-1]
	n_crit = n_arr[P_sum_arr<=alpha][0]
	P_sum  = P_sum_arr[P_sum_arr<=alpha][0]
	return n_crit, P_sum

def get_mulds_from_poisson(n_bg,n_crit,beta=0.5):
	# beta=0.1 gives statistical power 1-beta = 90 %
	import numpy as np
	mu_lds = 0.0
	P_sum = np.sum(get_poisson_arr(n_crit,n_bg+mu_lds)[0])
	incr_arr = np.array([10.,1,0.1,0.01,0.001])
	for incr in incr_arr:
		while P_sum < (1-beta):
			mu_lds = round( mu_lds+incr, 6 )
			P_sum  = np.sum(get_poisson_arr(n_crit,n_bg+mu_lds)[0])
		if incr != incr_arr[-1]:
			mu_lds = round( mu_lds-incr, 6 )
			P_sum  = np.sum(get_poisson_arr(n_crit,n_bg+mu_lds)[0])
	return mu_lds, P_sum # Put in rounding to ~6 decimal places on mulds in order to avoid floating point errors - don't put this on Psum!

def get_model_discovery_potential(n_bg,n_sg):
	n_bg, n_sg = float(n_bg), float(n_sg)
	n_crit, P_alpha = get_ncrit_from_poisson(n_bg)
	mu_lds, P_beta  = get_mulds_from_poisson(n_bg,n_crit)
	return mu_lds / max( n_sg, 1e-20 )

def get_model_indication_potential(n_bg,n_sg):
	n_bg, n_sg = float(n_bg), float(n_sg)
	n_crit, P_alpha = get_ncrit_from_poisson(n_bg,2.700e-3)
	mu_lds, P_beta  = get_mulds_from_poisson(n_bg,n_crit)
	return mu_lds / max( n_sg, 1e-20 )

def get_feldmancousins_sensitivity( n_bg, confidence=0.90, end_n_ob=29, give_std=False ):
	import numpy as np
	if np.isnan(n_bg):
		return np.nan
	n_ob = np.arange(end_n_ob)
	mu_fc         = np.array([ get_feldmancousins_upperlimit(n_bg, n, confidence) for n in n_ob ])
	coeff_poisson = np.array([ get_poisson(n,n_bg)                                for n in n_ob ])
	if not give_std:
		return sum(mu_fc*coeff_poisson)
	return sum(mu_fc*coeff_poisson), np.nan, np.nan

def get_feldmancousins_sensitivity_expanded( n_bg_exp, n_bg_lim, confidence=0.90, end_n_ob=29, give_std=False ):
	import numpy as np
	if np.isnan(n_bg_exp):
		return np.nan
	if np.isnan(n_bg_lim):
		return np.nan
	n_ob = np.arange(end_n_ob)
	mu_fc         = np.array([ get_feldmancousins_upperlimit(n_bg_lim, n, confidence) for n in n_ob ])
	coeff_poisson = np.array([ get_poisson(n,n_bg_exp)                                for n in n_ob ])
	if not give_std:
		return sum(mu_fc*coeff_poisson)
	return sum(mu_fc*coeff_poisson), np.nan, np.nan

def get_model_rejection_factor(n_bg,n_sg):
	import numpy as np
	if np.isscalar(n_bg) and np.isscalar(n_sg):
		sens = float(get_feldmancousins_sensitivity(n_bg))
		n_sg = float(n_sg) if n_sg>=1e-20*sens else 1e-20*sens
		return sens / float(n_sg)
	elif (not np.isscalar(n_bg)) and (not np.isscalar(n_sg)):
		sens = np.array([ get_feldmancousins_sensitivity(nb) for nb in n_bg ]).astype(float)
		n_sg = np.array([ max(ns,1e-20*min(sens)) for ns in n_sg ]).astype(float)
		return sens / n_sg
	#else:
	return np.nan

def get_model_rejection_factor_expanded(n_bg_exp,n_bg_lim,n_sg):
	import numpy as np
	if np.isscalar(n_bg_exp) and np.isscalar(n_bg_lim) and np.isscalar(n_sg):
		sens = float(get_feldmancousins_sensitivity_expanded(n_bg_exp,n_bg_lim))
		n_sg = float(n_sg) if n_sg>=1e-20*sens else 1e-20*sens
		return sens / float(n_sg)
	elif (not np.isscalar(n_bg_exp)) and (not np.isscalar(n_bg_lim)) and (not np.isscalar(n_sg)):
		sens = np.array([ get_feldmancousins_sensitivity_expanded(nb_exp,nb_lim) for nb_exp,nb_lim in zip(n_bg_exp,n_bg_lim) ]).astype(float)
		n_sg = np.array([ max(ns,1e-20*min(sens)) for ns in n_sg ]).astype(float)
		return sens / n_sg
	#else:
	return np.nan

def get_nsg_using_uncertainty( n_sg, sigma_sg):
	import numpy as np
	import scipy as sp
	hat_n_sg_arr = np.arange(int(max(100,n_sg*3,n_sg+sigma_sg*2))+1)
	PG_arr       = np.array([ get_PoisGaus( hat_n_sg, n_sg, sigma_sg) for hat_n_sg in hat_n_sg_arr ])
#	for hatn,pg in zip(hat_n_sg_arr,PG_arr):
#		print "{:4}  *  {:13.5e}  =  {:13.5e}".format(hatn,pg,hatn*pg)
	return sum( hat_n_sg_arr * PG_arr )

def get_nbg_using_uncertainty( n_bg, sigma_bg):
	import numpy as np
	import scipy as sp
	hat_n_bg_arr = np.arange(int(max(100,n_bg*3,n_bg+sigma_bg*2))+1)
	PG_arr       = np.array([ get_PoisGaus( hat_n_bg, n_bg, sigma_bg) for hat_n_bg in hat_n_bg_arr ])
	return sum( hat_n_bg_arr * PG_arr )

def get_muninety_using_uncertainty_INVALID( n_bg, sigma_bg, n_ob):
	import numpy as np
	import scipy as sp
	hat_n_bg_arr = np.arange(int(max(100,n_bg*3,n_bg+sigma_bg*2))+1)
	hat_muninuety_arr = np.array([ get_feldmancousins_upperlimit(nb,n_ob) for nb in hat_n_bg_arr ])
	PG_arr       = np.array([ get_PoisGaus( hat_n_bg, n_bg, sigma_bg) for hat_n_bg in hat_n_bg_arr ])
	for hatn,hatmu,pg in zip(hat_n_bg_arr,hat_muninuety_arr,PG_arr):
		print("{:4}  ->  {:13.5e}  *  {:13.5e}  =  {:13.5e}".format(hatn,hatmu,pg,hatmu*pg))
	return sum( hat_muninuety_arr * PG_arr )

def get_PoisGaus( hatnsg, nsg, sigma ):
	import numpy as np
	import scipy as sp
	import scipy.integrate as spintgr
	intgr_lo_bound = max(-nsg, -sigma*5.)
	intgr_up_bound =            sigma*5.
	return spintgr.quad( get_PoisGaus_integrand, intgr_lo_bound, intgr_up_bound, args=(hatnsg,nsg,sigma) )[0]

def get_PoisGaus_integrand( x, hatnsg, nsg, sigma ):
	import numpy as np
#	print "x = {:11.3e}  hatnsg = {:11.3e}  nsg = {:11.3e}  sigma = {:11.3e}  return = {:11.3e}".format(x,hatnsg,nsg,sigma,( ( (nsg+x)**hatnsg * np.e**(-(nsg+x)) ) / np.math.factorial(hatnsg) ) * ( (1./(sigma*np.sqrt(2*np.pi))) * np.e**(-0.5*(x/sigma)**2) ))
#	print ( ( (n+x)**hatn * np.e**(-(n+x)) ) / np.math.factorial(hatn) ) * ( (1./(sgm*np.sqrt(2*np.pi))) * np.e**(-0.5*(x/sgm)**2) )
	return ( ( (nsg+x)**hatnsg * np.e**(-(nsg+x)) ) / np.math.factorial(hatnsg) ) * ( (1./(sigma*np.sqrt(2*np.pi))) * np.e**(-0.5*(x/sigma)**2) )

# To test this over several values, do
#
#print 6*" ",
#for rel_unc in np.linspace(0.02,0.52,26):
#	print "{:6}".format(rel_unc),
#print ""
#for nsg in np.linspace(1,35,35):
#	print "{:6}".format(int(nsg)),
#	for rel_unc in np.linspace(0.02,0.52,26):
#		try:
#			print "{:6}".format(round(get_nsg_uncertainty(nsg,nsg*rel_unc),2)),
#		except OverflowError:
#			print "{:6}".format("-X-"),
#	print ""


def get_model_conclusions_nev(n_bg,n_sg):
	nev_keys, nev, nev_expl = ["nsg","nbg"], {"nsg":n_sg,"nbg":n_bg}, {"nsg":"Expected number of signal events","nbg":"Expected number of background events"}
	# For alpha numbers below, see https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule#Table_of_numerical_values

	nev_keys         += ["mu90"]
	nev["mu90"]       = get_feldmancousins_sensitivity(n_bg)
	nev_expl["mu90"]  = "Average lowest upper limit on signal (90 % CL) that can be claimed"
	nev_keys         += ["mrf"]
	nev["mrf"]        = get_model_rejection_factor(n_bg,n_sg)
	nev_expl["mrf"]   = "Model Rejection Factor"

	nev_keys                += ["ncrit_7sigma"]
	nev["ncrit_7sigma"], P   = get_ncrit_from_poisson(n_bg,alpha=2.560e-12)
	nev_expl["ncrit_7sigma"] = "The lowest number of observed events needed to claim 'other effects' with 7 sigma"
	nev_keys                += ["mulds_7sigma"]
	nev["mulds_7sigma"], P   = get_mulds_from_poisson(n_bg,nev["ncrit_7sigma"])
	nev_expl["mulds_7sigma"] = "Lowest detectable signal at 7 sigma, i.e. the lowest number of signal events that can give the given n_crit"

	nev_keys                += ["ncrit_6sigma"]
	nev["ncrit_6sigma"], P   = get_ncrit_from_poisson(n_bg,alpha=1.973e-9)
	nev_expl["ncrit_6sigma"] = "The lowest number of observed events needed to claim 'other effects' with 6 sigma"
	nev_keys                += ["mulds_6sigma"]
	nev["mulds_6sigma"], P   = get_mulds_from_poisson(n_bg,nev["ncrit_6sigma"])
	nev_expl["mulds_6sigma"] = "Lowest detectable signal at 6 sigma, i.e. the lowest number of signal events that can give the given n_crit"

	nev_keys                += ["ncrit_5sigma"]
	nev["ncrit_5sigma"], P   = get_ncrit_from_poisson(n_bg,alpha=5.733e-7)
	nev_expl["ncrit_5sigma"] = "The lowest number of observed events needed to claim 'other effects' with 5 sigma"
	nev_keys                += ["mulds_5sigma"]
	nev["mulds_5sigma"], P   = get_mulds_from_poisson(n_bg,nev["ncrit_5sigma"])
	nev_expl["mulds_5sigma"] = "Lowest detectable signal at 5 sigma, i.e. the lowest number of signal events that can give the given n_crit"
	nev_keys                += ["mdp_5sigma"]
	nev["mdp_5sigma"]        = get_model_discovery_potential(n_bg,n_sg)
	nev_expl["mdp_5sigma"]   = "Model Discovery Potential for 5 sigma"

	nev_keys                += ["ncrit_4sigma"]
	nev["ncrit_4sigma"], P   = get_ncrit_from_poisson(n_bg,alpha=6.334e-5)
	nev_expl["ncrit_4sigma"] = "The lowest number of observed events needed to claim 'other effects' with 4 sigma"
	nev_keys                += ["mulds_4sigma"]
	nev["mulds_4sigma"], P   = get_mulds_from_poisson(n_bg,nev["ncrit_4sigma"])
	nev_expl["mulds_4sigma"] = "Lowest detectable signal at 4 sigma, i.e. the lowest number of signal events that can give the given n_crit"

	nev_keys                += ["ncrit_3sigma"]
	nev["ncrit_3sigma"], P   = get_ncrit_from_poisson(n_bg,alpha=2.700e-3)
	nev_expl["ncrit_3sigma"] = "The lowest number of observed events needed to claim 'other effects' with 3 sigma"
	nev_keys                += ["mulds_3sigma"]
	nev["mulds_3sigma"], P   = get_mulds_from_poisson(n_bg,nev["ncrit_3sigma"])
	nev_expl["mulds_3sigma"] = "Lowest detectable signal at 3 sigma, i.e. the lowest number of signal events that can give the given n_crit"
	nev_keys                += ["mdp_3sigma"]
	nev["mdp_3sigma"]        = get_model_indication_potential(n_bg,n_sg)
	nev_expl["mdp_3sigma"]   = "Model Discovery Potential for 3 sigma"

	nev_keys                += ["ncrit_2sigma"]
	nev["ncrit_2sigma"], P   = get_ncrit_from_poisson(n_bg,alpha=4.550e-2)
	nev_expl["ncrit_2sigma"] = "The lowest number of observed events needed to claim 'other effects' with 2 sigma"
	nev_keys                += ["mulds_2sigma"]
	nev["mulds_2sigma"], P   = get_mulds_from_poisson(n_bg,nev["ncrit_2sigma"])
	nev_expl["mulds_2sigma"] = "Lowest detectable signal at 2 sigma, i.e. the lowest number of signal events that can give the given n_crit"

	nev_keys                += ["ncrit_1sigma"]
	nev["ncrit_1sigma"], P   = get_ncrit_from_poisson(n_bg,alpha=3.173e-1)
	nev_expl["ncrit_1sigma"] = "The lowest number of observed events needed to claim 'other effects' with 1 sigma"
	nev_keys                += ["mulds_1sigma"]
	nev["mulds_1sigma"], P   = get_mulds_from_poisson(n_bg,nev["ncrit_1sigma"])
	nev_expl["mulds_1sigma"] = "Lowest detectable signal at 1 sigma, i.e. the lowest number of signal events that can give the given n_crit"

	return 	nev_keys, nev, nev_expl


def get_limits_for_different_nob(n_bg):
	mu90 = {}
	for n_ob in np.linspace(0,9,10):
		mu90["nob={}".format(n_ob)] = [ get_feldmancousins_lowerlimit(n_bg,n_ob), get_feldmancousins_upperlimit(n_bg,n_ob), ]
	return mu90

# make function for MDF
# P(>=n_crit|mu_b) = sum_(n_k=n_obs)^infty P(n_k|mu_b)
# p(n_k|mu_b) = Poisson(prob of seeing n_k given mu_b)
# mu_b = n_bg


# TROLKE BELOW

def get_rolke_limits( n_ob, rel_delta_n_sg, n_bg, delta_n_bg, bgtype, confidence=0.9 ):
	import ROOT
	from ROOT import TRolke
	tr = TRolke()
	tr.SetCL( confidence )
	if bgtype.lower() == "known":
		tr.SetKnownBkgGaussEff( n_ob, 1., rel_delta_n_sg, n_bg )
	if bgtype.lower() == "gauss":
		tr.SetGaussBkgGaussEff( n_ob, n_bg, 1., rel_delta_n_sg, delta_n_bg )
	ul, ll = ROOT.Double(0), ROOT.Double(0)
	tr.GetLimits( ll, ul )
	return ll, ul

def get_rolke_upperlimit_bgknown_sggauss( n_ob, rel_delta_n_sg, n_bg,             confidence=0.9 ):
	ll, ul = get_rolke_limits( n_ob, rel_delta_n_sg, n_bg, 0., "known", confidence )
	return ul

def get_rolke_upperlimit_bggauss_sggauss( n_ob, rel_delta_n_sg, n_bg, delta_n_bg, confidence=0.9 ):
	ll, ul = get_rolke_limits( n_ob, rel_delta_n_sg, n_bg, delta_n_bg, "gauss", confidence )
	return ul


def get_rolke_sensitivity_bgknown_sggauss( rel_delta_n_sg, n_bg,             confidence=0.90, end_n_ob=29 ):
	import numpy as np
	n_ob          = np.arange(end_n_ob)
	mu_rlk        = np.array([ get_rolke_upperlimit_bgknown_sggauss( n, rel_delta_n_sg, n_bg,             confidence) for n in n_ob ])
	coeff_poisson = np.array([ get_poisson(n,n_bg)                                                                    for n in n_ob ])
	return sum(mu_rlk*coeff_poisson)

def get_rolke_sensitivity_bggauss_sggauss( rel_delta_n_sg, n_bg, delta_n_bg, confidence=0.90, end_n_ob=29 ):
	import numpy as np
	n_ob          = np.arange(end_n_ob)
	mu_rlk        = np.array([ get_rolke_upperlimit_bggauss_sggauss( n, rel_delta_n_sg, n_bg, delta_n_sg, confidence) for n in n_ob ])
	coeff_poisson = np.array([ get_poisson(n,n_bg)                                                                    for n in n_ob ])
	return sum(mu_rlk*coeff_poisson)



def listnorm(thelist,themode="integral",theval=1.):
	import numpy as np
	if len(thelist)==0:
		return np.array([])
	if themode.lower() == "none":
		return np.array(thelist)
	if themode.lower() == "integral":
		return theval*np.array(thelist)/sum(thelist)
	if themode.lower() == "maxvalue":
		return theval*np.array(thelist)/max(thelist)
	if themode.lower() == "average":
		return theval*np.array(thelist)/np.average(thelist)


class gaussian_kde:
	def __init__(self,d=np.array([]),w=np.array([]),e=np.array([-np.infty,np.infty]),n=1000,s=np.nan):
		import numpy as np
		self.data    = np.array(d).astype(float)
		self.weights = np.array(w).astype(float)
		self.edges   = np.array(e).astype(float)
		self.nvals   = int(n)+1
		self.sigma   = float(s)
	def calc_vals(self,flatten_tails_to_uniform=-1.):
		self.kde_x   = np.linspace(self.edges[0], self.edges[1], self.nvals)
		self.kernels = np.array([ we*np.exp(-np.power(self.kde_x-da,2.)/(2*np.power(self.sigma,2.)))
		                          for da, we in zip(self.data, self.weights) ])
		self.kde_y   = np.sum(self.kernels,axis=0)
		if flatten_tails_to_uniform>=2.:
#			self.kde_uniform = listnorm( np.sum(
			self.kde_uniform = np.sum(
			                       np.array([ np.exp(-np.power(self.kde_x-da,2.)/(2*np.power(self.sigma,2.)))
		                               for da in np.linspace(
		                                   self.edges[0]+0.5*(self.edges[1]-self.edges[0])/float(flatten_tails_to_uniform),
		                                   self.edges[1]-0.5*(self.edges[1]-self.edges[0])/float(flatten_tails_to_uniform),
		                                   flatten_tails_to_uniform)
		                               ]),
		                           axis=0 )
#		                           axis=0 ), "maxvalue", 1. )
			self.kde_y = self.kde_y / self.kde_uniform
	def get_kde(self):
		return self.kde_y, self.kde_x
	def calc_and_get_kde(self,flatten_tails_to_uniform=-1.):
		self.calc_vals(flatten_tails_to_uniform)
		return self.get_kde()
# Usage:
#     data    = 4+6*np.random.rand(1000)
#     weights = np.ones(len(data))
#     kern = gaussian_kde(data,weights,[4,10],6000,0.5)
#     either:
#         kern.calc_vals()
#         ys, xs = kern.get_kde()
#     or:
#         ys, xs = kern.calc_and_get_kde()



#def get_averageshiftedhistogram(bins,edges,n_ash):
def get_averageshiftedhistogram(bins,n_ash):
    # This function takes a histogram (given by bins, edges) and averages each bin with an average shifted histogram method
    import numpy as np
    bins     = np.array(bins)
#   edges    = np.array(edges)
    weights  = np.zeros(len(bins))
    bins_ash = np.zeros(len(bins))
    for i in range(len(bins)):
        weights = np.zeros(len(bins))
        weights[i] = n_ash
        for j in range(1,n_ash):
            if i+j <= len(bins)-1:
                weights[i+j] = n_ash - j
            if i-j >= 0:
                weights[i-j] = n_ash - j
        bins_ash[i] = np.sum(weights*bins) / np.sum(weights)
    return bins_ash
