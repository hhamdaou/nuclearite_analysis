import numpy as np
import scipy.constants as sc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

#from icecube import icetray#, dataclasses, dataio, tableio, common_variables, improvedLinefit, portia#, recclasses, sim_services, phys_services
#from icecube.icetray import I3Units
#from icecube.dataclasses import I3MCTree, I3Particle, I3RecoPulseSeriesMap, I3RecoPulse, I3MapStringDouble
#from icecube.tableio import I3TableWriter
#from icecube.hdfwriter import I3HDFTableService
#from I3Tray import *

matplotlib.rcParams['font.family']='serif'
matplotlib.rcParams['font.size']=14
matplotlib.rcParams['axes.grid']=True
matplotlib.rcParams['xtick.labelsize']='x-small'
matplotlib.rcParams['ytick.labelsize']='x-small'
matplotlib.rcParams['legend.fontsize']='x-small'
matplotlib.rcParams['legend.numpoints']=1


halfoom    = 3.1622776601683795 #         half of an order of magnitude ->      sqrt(10)
quarteroom = 1.7782794100389228 # half of half of an order of magnitude -> sqrt(sqrt(10))




def make_plotting_interval(therange,theoption="0"):
	"""Yield aninterval that nicely includes the given values and some surrounding area"""
	lo, hi = therange

	if theoption in ["log"]:
		# The interval is logarithmic
		outrange = [ lo/((hi/lo)**0.15), hi*((hi/lo)**0.15) ]
	elif theoption in [0., 0, "0"]:
		# The interval is linear and the lower bound is be 0
		outrange = [                 0., hi+((hi   )*0.13)  ]
	elif theoption in ["", "lin"]:
		# The interval is linear
		outrange = [ lo-((hi-lo)*0.15),  hi+((hi-lo)*0.15)  ]

	return outrange

class ABPlot1D:
	#-*- coding: utf-8 -*-

	def __init__(self):
		import numpy as np
		import matplotlib
		matplotlib.use('Agg')
		import matplotlib.pyplot as plt
		from matplotlib.colors import LogNorm
		from matplotlib import cm
		#matplotlib.rcParams['font.family']='serif'
		matplotlib.rcParams['font.family']='STIXGeneral'
		matplotlib.rcParams['font.size']=18
		matplotlib.rcParams['axes.grid']=True
#		matplotlib.rcParams.update({'font.size': 18})
#		matplotlib.rcParams['mathtext.default']='regular'
#		matplotlib.rcParams['xtick.labelsize']='x-small'
#		matplotlib.rcParams['ytick.labelsize']='x-small'
#		matplotlib.rcParams['legend.fontsize']='x-small'
#		matplotlib.rcParams['legend.fontsize']='normal'
		matplotlib.rcParams['legend.numpoints']=1

		self.data_keys=[]
		self.legend={}
		self.colors={}
		self.x_edges={}
		self.x_values={}
		self.y_values={}
		self.y_uperr={}
		self.y_loerr={}
		self.leg_order={}
		self.title="The Plot Title"
		self.x_label="The x axis"
		self.y_label="The y axis"
		self.x_range=[0.,1.]
		self.y_range=[0.,1.]
		self.y_log=False
		self.x_log=False
		self.histogram={}
		self.linestyle={}
		self.linewidth={}
		self.marker={}
		self.marker_size={}
		self.maxvals={}
		self.maxval=np.nan

		self.has_line=False
		self.has_lines=False
		self.x_line=np.array([])
		self.y_line=np.array([])
		self.line_colors=[]
		self.line_labels=[]
		self.line_labels_left=False
		self.line_labels_style="normal"
		self.line_label_colors=[]
		self.line_labels_small=False
		self.has_texts=False
		self.x_text=np.array([])
		self.y_text=np.array([])
		self.text_colors=[]
		self.text_labels=[]
		self.text_styles=[]
		self.text_labels_small=False

		self.grid_major_only=False
		self.IC_workinprogress=False
		self.position_IC_workinprogress=[np.nan,np.nan]
		self.poskey_IC_workinprogress=""
		self.IC_preliminary=False
		self.position_IC_preliminary=[np.nan,np.nan]
		self.poskey_IC_preliminary=""
		self.path_save=""
		self.name_save=""
		self.larger_marks = False
		self.wide_legends = False  # Check this if the legend texts are wide and the number of legend columns needs to be reduced
	#	self.errors_nonzerologmask=np.array([])
		self.verbose=1
#		self.eventlines_x={}
#		self.eventlines_col={}
#		self.eventlines_label={}

	def calc_maxvals(self):
		self.maxvals = { key: max(self.y_values[key]) if len(self.y_values[key])>0 else 0. for key in list(self.y_values.keys()) }
		self.maxval  = max([ self.maxvals[key] for key in list(self.maxvals.keys()) ]) if len(list(self.maxvals.keys()))>0 else 0.

	def auto_y_range(self,linlog="lin"):
		self.calc_maxvals()
		if linlog=="lin":
		#	self.y_range = [0,1.2*max([max(self.y_values[key]) if len(self.y_values[key])>0 else 0. for key in self.y_values.keys()]) if len(self.y_values.keys())>0 else 1.]
		#	if max([max(self.y_values[key]) for key in self.y_values.keys()])==0:
		#		self.y_range = [0.,1.]
			self.y_range = [ 0., 1.2*self.maxval if self.maxval>0 else 1.]
		elif linlog=="log":
		#	self.y_range = [0.00001*3.1622776601683795*max([max(self.y_values[key]) if len(self.y_values[key])>0 else 0.1 for key in self.y_values.keys()]) if len(self.y_values.keys())>0 else 0.1, 3.1622776601683795*max([max(self.y_values[key]) if len(self.y_values[key])>0 else 10. for key in self.y_values.keys()]) if len(self.y_values.keys())>0 else 10.]
		#	if max([max(self.y_values[key]) for key in self.y_values.keys()])==0:
		#		self.y_range = [0.1,10.]
			self.y_range = [0.0001*halfoom*self.maxval if self.maxval>0 else 0.01*halfoom, halfoom*self.maxval if self.maxval>0 else 10.*halfoom ]
			if self.maxval>0:
				for i in range(4):
					if min(self.maxvals.values()) < self.y_range[0]:
						self.y_range[0] *= 0.1
		elif linlog=="log3":
			self.y_range = [0.001*halfoom*self.maxval if self.maxval>0 else 0.01*halfoom, halfoom*self.maxval if self.maxval>0 else 10.*halfoom ]
			if self.maxval>0:
				for i in range(4):
					if min(self.maxvals.values()) < self.y_range[0]:
						self.y_range[0] *= 0.1

		else:
			exit("The phrasing '{}' is not an acceptable key for linear or logarithmic plotting - use 'lin' or 'log' or 'log3'".format(linlog))

	def set_title_x_y_labels(self, title,x_label,y_label):
		self.title   = title
		self.x_label = x_label
		self.y_label = y_label

	def set_x_y_ranges(self, x_range, y_range):
		self.x_range = x_range
		self.y_range = y_range

	def plot(self):

#		from misc import ABVerbosePrint
#		plotvbp = ABVerbosePrint()
#		plotvbp.label1, plotvbp.label2 = "AB", "PLOT"
#		plotvbp.script_verbose_level = self.verbose

		self.ax = plt.subplot(111)
		plt.gcf().subplots_adjust(bottom=0.15)

		if (self.x_edges=={} and self.x_values=={}) or self.y_values=={}:
			print(":-------------------\nERROR\n:-------------------")
			print("YOU NEED TO ENTER THE VALUES TO PLOT!!")
			print("(A dict self.x_edges for histograms, self.x_values for line plots and self.y_values for either.)")

		self.n_lines=len(self.data_keys)

#		if self.histogram=={}:
#			for key in self.data_keys:
#				self.histogram[key] = False
#
#		if self.linestyle=={}:
#			for key in self.data_keys:
#				self.linestyle[key] = "solid"
#
#		if self.linewidth=={}:
#			for key in self.data_keys:
#				self.linewidth[key] = 1.
#
#		if self.marker=={}:
#			for key in self.data_keys:
#				self.marker[key] = "."

		# setting default values
		for key in self.data_keys:
			if key not in list(self.histogram.keys()):
				self.histogram[key] = False
			if key not in list(self.linestyle.keys()):
				self.linestyle[key] = "solid"
			if key not in list(self.linewidth.keys()):
				self.linewidth[key] = 1.
			if key not in list(self.marker.keys()):
				self.marker[key] = "."

		self.lines={}
		for key in self.data_keys:
			if self.histogram[key]:
				if self.y_log:   ###### ENABLE CHANGE OF MARKERSIZE!
					self.lines[key] = plt.semilogy(
					    [    b        for b in self.x_edges[key] for x in (0, 1)][1:-1],
					    [max(h,1e-80) for h in self.y_values[key] for x in (0, 1)],
					    label     = self.legend[key],
					    color     = self.colors[key],
					    linestyle = self.linestyle[key],
					    linewidth = self.linewidth[key]
					    )
				else:
					self.lines[key] = plt.Line2D(
					    [b for b in self.x_edges[key] for x in (0, 1)][1:-1],
					    [h for h in self.y_values[key] for x in (0, 1)],
					    label     = self.legend[key],
					    color     = self.colors[key],
					    linestyle = self.linestyle[key],
					    linewidth = self.linewidth[key]
					    )
			else:
				if self.y_log:
					self.lines[key] = plt.semilogy(
					                            self.x_values[key],
					    [ max(y,1e-80) for y in self.y_values[key] ],
					    label     = self.legend[key],
					    color     = self.colors[key],
					    linestyle = self.linestyle[key],
					    linewidth = self.linewidth[key],
					    marker    = self.marker[key]
					    )
				else:
					self.lines[key] = plt.Line2D(
					    self.x_values[key],
					    self.y_values[key],
					    label     = self.legend[key],
					    color     = self.colors[key],
					    linestyle = self.linestyle[key],
					    linewidth = self.linewidth[key],
					    marker    = self.marker[key]
					    )

		plt.xlim(self.x_range)
		plt.ylim(self.y_range)

		if self.grid_major_only:
			plt.grid(True,which="major")

		self.box = self.ax.get_position()
#		print("| NOTE | If you want to avoid whitespace at the top of your plot when you remove the plot title, follow instructions in comments!")
		# Do this instead
		#self.ax.set_position([self.box.x0, self.box.y0+self.box.height*0.05, self.box.width, self.box.height*0.95])
		#
		# OR EVEN BETTER
		#self.ax.set_position([self.box.x0, self.box.y0+SOMETHING, SOME_CM, SOME_CM])
		# AND THEN CUSTOMIZE
		# fig.set_size_inches(SOME_CM_DIV_BY_TWO_POINT_FIFTYFOUR, SOME_CM_DIV_BY_TWO_POINT_FIFTYFOUR)
		self.ax.set_position([self.box.x0, self.box.y0, self.box.width, self.box.height*0.9])

		if not self.y_log:
			for key in sorted(self.data_keys):
				self.ax.add_line(self.lines[key])

		if self.y_uperr!={} and self.y_loerr!={}:
			for key in self.data_keys:
				if self.histogram[key]:
					plt.fill_between(
						np.array([ b for b in self.x_edges[key]                                                                       for x in (0,1) ])[1:-1],
						np.array([ h for h in np.array([ yl if not (yl==0. and self.y_log) else 1e-100 for yl in self.y_loerr[key] ]) for x in (0,1) ]),
						np.array([ h for h in np.array([ yu if not (yu==0. and self.y_log) else 1e-99  for yu in self.y_uperr[key] ]) for x in (0,1) ]),
						alpha     = 0.25,
						edgecolor = "k",
						facecolor = self.colors[key],
						linewidth = 0.
						)
				else:
					plt.fill_between(
						self.x_values[key],
						np.array([ yl if not (yl==0. and self.y_log) else 1e-100 for yl in self.y_loerr[key] ]),
						np.array([ yu if not (yu==0. and self.y_log) else 1e-99  for yu in self.y_uperr[key] ]),
						alpha     = 0.25,
						edgecolor = "k",
						facecolor = self.colors[key],
						linewidth = 0.
						)


		self.n_legend_columns=1
		if self.n_lines<=3:
			self.n_legend_columns=self.n_lines
		elif self.n_lines<=6:
			self.n_legend_columns=bool(self.n_lines%2)+int(self.n_lines/2)
		else:
			self.n_legend_columns=bool(self.n_lines%3)+int(self.n_lines/3)
		if self.wide_legends:
			self.n_legend_columns -= 1

		if self.leg_order:
			self.leg_handles, self.leg_labels = self.ax.get_legend_handles_labels()
#			labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0])) # sort both labels and handles by labels
			self.leg_order_index = len(self.data_keys)*[-1]
			for idk,dk in zip(list(range(len(self.data_keys))),self.data_keys):
				self.leg_order_index[self.leg_order[dk]] = idk
#			plt.legend([self.leg_handles[idx] for idx in self.leg_order_index],[self.leg_labels[idx] for idx in self.leg_order_index])
			self.ax.legend(
				[self.leg_handles[idx] for idx in self.leg_order_index],
				[self.leg_labels[idx] for idx in self.leg_order_index],
				loc="lower center", bbox_to_anchor=(0.5, 1.015),
				ncol=self.n_legend_columns, borderaxespad=0., frameon=False
				)
		else:
			self.ax.legend( loc="lower center", bbox_to_anchor=(0.5, 1.015),
				ncol=self.n_legend_columns, borderaxespad=0., frameon=False
				)

		self.n_legend_rows=1
		self.n_legend_rows=min(3,bool(self.n_lines%3) + int(self.n_lines/3))


		if self.has_line:
			line_cut = plt.Line2D( self.x_line, self.y_line, color="black", linewidth=1.5 )

		if self.has_lines:
			lines_cut = []
			for x,y,col,lab in zip(self.x_line,self.y_line,(self.line_label_colors if self.line_label_colors else self.line_colors),self.line_labels):
				lines_cut += [ plt.Line2D( x, y, color=col, linewidth=(1. if self.line_labels_small else 1.5) ) ]
				self.ax.text( x[1] + 0.02*(self.x_range[1]-self.x_range[0])*( 1. if not self.line_labels_left else -1. ), y[1],
					"{}".format(lab),
					horizontalalignment="left" if not self.line_labels_left else "right",
					verticalalignment="center",
					style=self.line_labels_style,
					size=(12 if self.line_labels_small else 16), color=col )

		if self.has_texts:
			texts_cut = []
			for x,y,col,lbl,stl in zip(self.x_text,self.y_text,self.text_colors,self.text_labels,self.text_styles):
				self.ax.text( x, y,
					"{}".format(lbl),
					horizontalalignment="left",
					verticalalignment="center",
					style=stl,
					size=(12 if self.text_labels_small else 16), color=col )


		if self.IC_workinprogress:
			if self.poskey_IC_workinprogress:
				py, px  = str(self.poskey_IC_workinprogress[0]), str(self.poskey_IC_workinprogress[1])
				px_keys = { "l": 0.20, "c": 0.50, "r": 0.80 } # left,  center, right
				py_keys = { "l": 0.20, "c": 0.50, "u": 0.80 } # lower, center, upper
				self.position_IC_workinprogress[0]=self.x_range[0]+(self.x_range[1]-self.x_range[0])*px_keys[px]
				xpos                              =self.x_range[0]+(self.x_range[1]-self.x_range[0])*px_keys[px]
				self.position_IC_workinprogress[1]=self.y_range[0]+(self.y_range[1]-self.y_range[0])*py_keys[py]
				ypos_ic                           =self.y_range[0]+(self.y_range[1]-self.y_range[0])*(py_keys[py]+0.05)
				ypos_wip                          =self.y_range[0]+(self.y_range[1]-self.y_range[0])*(py_keys[py]-0.05)
				if self.y_log:
					self.position_IC_workinprogress[1]=self.y_range[0]*(self.y_range[1]/self.y_range[0])**py_keys[py]
					ypos_ic                           =self.y_range[0]*(self.y_range[1]/self.y_range[0])**(py_keys[py]+0.05)
					ypos_wip                          =self.y_range[0]*(self.y_range[1]/self.y_range[0])**(py_keys[py]-0.05)
				self.ax.text( xpos, ypos_ic,
					"IceCube",
					horizontalalignment="center",
					verticalalignment="center",
					size=18, color="red" )
				self.ax.text( xpos, ypos_wip,
					"Work-in-Progress",
					horizontalalignment="center",
					verticalalignment="center",
					size=15, color="red" )
#			else:
#				if np.isnan(self.position_IC_workinprogress[0]):
#					self.position_IC_workinprogress[0]=self.x_range[0]+(self.x_range[1]-self.x_range[0])*0.5
#				if np.isnan(self.position_IC_workinprogress[1]):
#					if self.y_log:
#						self.position_IC_workinprogress[1]=self.y_range[0]*(self.y_range[1]/self.y_range[0])**0.5
#					else:
#						self.position_IC_workinprogress[1]=self.y_range[0]+(self.y_range[1]-self.y_range[0])*0.5
#				self.ax.text(
#					self.position_IC_workinprogress[0],
#					self.position_IC_workinprogress[1],
#					"IceCube Work-in-Progress",
#					horizontalalignment="center",
#					verticalalignment="center",
#					size=18, color="red" )

		if self.IC_preliminary:
			if self.poskey_IC_preliminary:
				py, px  = str(self.poskey_IC_preliminary[0]), str(self.poskey_IC_preliminary[1])
				px_keys = { "l": 0.20, "c": 0.50, "r": 0.80, "a": 0.30, "e": 0.70, } # left,  center, right
				py_keys = { "l": 0.20, "c": 0.50, "u": 0.80, "a": 0.17, "e": 0.83, } # lower, center, upper
				alignx_keys = { "l": "left", "c": "center", "r": "right" }
				xwidth = (self.x_range[1]-self.x_range[0])
				self.position_IC_preliminary[0] = self.x_range[0] + xwidth *  px_keys[px]
				xpos                            = self.x_range[0] + xwidth *  px_keys[px]
				self.position_IC_preliminary[1] = self.y_range[0] + (self.y_range[1]-self.y_range[0]) *  py_keys[py]
				ypos_ic_0                       = self.y_range[0] + (self.y_range[1]-self.y_range[0]) * (py_keys[py]-0.03+0.000)
				ypos_ic_1                       = self.y_range[0] + (self.y_range[1]-self.y_range[0]) * (py_keys[py]-0.03+0.008)
				ypos_prlm_0                     = self.y_range[0] + (self.y_range[1]-self.y_range[0]) * (py_keys[py]-0.03-0.070)
				ypos_prlm_1                     = self.y_range[0] + (self.y_range[1]-self.y_range[0]) * (py_keys[py]-0.03-0.065)
				if self.y_log:
					self.position_IC_preliminary[1]=self.y_range[0]*(self.y_range[1]/self.y_range[0])**py_keys[py]
					ypos_ic_0                      =self.y_range[0]*(self.y_range[1]/self.y_range[0])**(py_keys[py]-0.03+0.000)
					ypos_ic_1                      =self.y_range[0]*(self.y_range[1]/self.y_range[0])**(py_keys[py]-0.03+0.008)
					ypos_prlm_0                    =self.y_range[0]*(self.y_range[1]/self.y_range[0])**(py_keys[py]-0.03-0.070)
					ypos_prlm_1                    =self.y_range[0]*(self.y_range[1]/self.y_range[0])**(py_keys[py]-0.03-0.065)
#				self.ax.text( xpos, ypos_ic_0,
#					"IceCube",
#					horizontalalignment=alignx_keys[px],
#					verticalalignment="center",
#					size=20, color="red" ) #, variant="small-caps" )
#				self.ax.text( xpos, ypos_prlm_0,
#					"Preliminary",
#					horizontalalignment=alignx_keys[px],
#					verticalalignment="center",
#					size=16, color="red" ) #, variant="small-caps" )
				self.ax.text( xpos-xwidth*0.14,  ypos_ic_0,   "I",          horizontalalignment="center", verticalalignment="bottom", size=32, color="red" )
				self.ax.text( xpos-xwidth*0.083, ypos_ic_1,   "CE",         horizontalalignment="center", verticalalignment="bottom", size=24, color="red" )
				self.ax.text( xpos-xwidth*0.01,  ypos_ic_0,   "C",          horizontalalignment="center", verticalalignment="bottom", size=32, color="red" )
				self.ax.text( xpos+xwidth*0.09,  ypos_ic_1,   "UBE",        horizontalalignment="center", verticalalignment="bottom", size=24, color="red" )
				self.ax.text( xpos-xwidth*0.13,  ypos_prlm_0, "P",          horizontalalignment="center", verticalalignment="bottom", size=20, color="red" )
				self.ax.text( xpos+xwidth*0.02,  ypos_prlm_1, "RELIMINARY", horizontalalignment="center", verticalalignment="bottom", size=15, color="red" )

		plt.xlabel( self.x_label )
		plt.ylabel( self.y_label )


		plt.suptitle( self.title, y=0.96+0.01*self.n_legend_rows, fontsize="large" )
		if self.larger_marks:
			plt.suptitle( self.title, y=0.97+0.01*self.n_legend_rows, fontsize="large" )

		if self.has_line:
			self.ax.add_line(line_cut)
		if self.has_lines:
			for line_cut in lines_cut:
				self.ax.add_line(line_cut)

		fig = matplotlib.pyplot.gcf()
		fig.set_size_inches(8, 6)
		if self.larger_marks:
			fig.set_size_inches(6.4, 4.8)

#		plt.tight_layout()
		plt.savefig(self.path_save+self.name_save+".pdf")

		plt.close()






class ABHist2D:
	#-*- coding: utf-8 -*-

	def __init__(self):
		import matplotlib
		matplotlib.use('Agg')
		import matplotlib.pyplot as plt
		from matplotlib.colors import LogNorm
		from matplotlib import cm
		#matplotlib.rcParams['font.family']='serif'
		matplotlib.rcParams['font.family']='STIXGeneral'
		matplotlib.rcParams['font.size']=18
		matplotlib.rcParams['axes.grid']=True
#		matplotlib.rcParams.update({'font.size': 18})
#		matplotlib.rcParams['mathtext.default']='regular'
#		matplotlib.rcParams['xtick.labelsize']='x-small'
#		matplotlib.rcParams['ytick.labelsize']='x-small'
#		matplotlib.rcParams['legend.fontsize']='x-small'
#		matplotlib.rcParams['legend.fontsize']='normal'
		matplotlib.rcParams['legend.numpoints']=1

		self.data_keys=[]
		self.x_points={}
		self.y_points={}
		self.x_line={}
		self.y_line={}
		self.col_line={}
#		self.title="The Plot Title"
		self.title={}
		self.x_label="The x axis"
		self.y_label="The y axis"
		self.x_range=[0.,1.]
		self.y_range=[0.,1.]
		self.x_bins=20
		self.y_bins=20
		self.values_log=False
		self.colorbar_label = ""
		self.colorbar_range = []
		self.values_weight={}
		self.key_title={}
		self.has_line=False
		self.IC_workinprogress=False
		self.position_IC_workinprogress=[np.nan,np.nan]
		self.poskey_IC_workinprogress=""
		self.IC_preliminary=False
		self.position_IC_preliminary=[np.nan,np.nan]
		self.poskey_IC_preliminary=""
		self.path_save=""
		self.name_save=""
		self.verbose=1
		self.auto_hist_range=1.e6
		self.larger_marks = False

	def set_x_y_labels(self,x_label,y_label):
		self.x_label = x_label
		self.y_label = y_label

	def set_x_y_ranges_bins(self, x_range, y_range, x_bins, y_bins):
		self.x_range = x_range
		self.y_range = y_range
		self.x_bins  = x_bins
		self.y_bins  = y_bins



	def plot(self):

		for key in self.data_keys:

			self.ax = plt.subplot(111)
			plt.gcf().subplots_adjust(bottom=0.15)


			if self.x_points=={} or self.y_points=={}:
				print(":-------------------\nERROR\n:-------------------")
				print("YOU NEED TO ENTER THE VALUES TO PLOT!")
				print("(A dict self.x_edges for histograms, self.x_values for line plots and self.y_values for either.)")

			if self.has_line:
				if not ( self.x_line and self.y_line):
					exit( "Hey, you said there was a line, but there really wasn't a line! (You set 'has_line=True', but didn't give values for 'x_line' and/or 'y_line')" ) 
				line_cut = plt.Line2D( self.x_line[key], self.y_line[key], color=(self.col_line if self.col_line else "black"), linewidth=2. )
				if not any( (val<=self.x_range[1] and val>=self.x_range[0]) for val in  self.x_line[key]):
					print(":-------------------\nWARNING\n:-------------------")
					print("NONE OF THE X-VALUES YOU HAVE CHOSEN FOR YOUR LINE AT",key,"ARE WITHIN THE GIVEN X-RANGE!")
				if not any( (val<=self.y_range[1] and val>=self.y_range[0]) for val in  self.y_line[key]):
					print(":-------------------\nWARNING\n:-------------------")
					print("NONE OF THE Y-VALUES YOU HAVE CHOSEN FOR YOUR LINE AT",key,"ARE WITHIN THE GIVEN Y-RANGE!")

			if self.values_log:
				hist_xy, bins_x, bins_y, img_xy = plt.hist2d(
					self.x_points[key],
					self.y_points[key],
					bins    = (self.x_bins,self.y_bins),
					range   = ((self.x_range[0],self.x_range[1]),(self.y_range[0],self.y_range[1])),
					norm    = LogNorm(),
					weights = self.values_weight[key], )
			else:
				hist_xy, bins_x, bins_y, img_xy = plt.hist2d(
					self.x_points[key],
					self.y_points[key],
					bins    = (self.x_bins,self.y_bins),
					range   = ((self.x_range[0],self.x_range[1]),(self.y_range[0],self.y_range[1])),
			#		norm    = LogNorm(),
					weights = self.values_weight[key], )

			if self.auto_hist_range>0.:
				hist_range = [ np.amin(hist_xy[hist_xy>0.]), np.amax(hist_xy[hist_xy>0.]) ]
				if hist_range[0]<hist_range[1]/self.auto_hist_range:
					hist_range[0]=hist_range[1]/self.auto_hist_range
					if self.values_log:
						hist_xy, bins_x, bins_y, img_xy = plt.hist2d(
							self.x_points[key],
							self.y_points[key],
							bins    = (self.x_bins,self.y_bins),
							range   = ((self.x_range[0],self.x_range[1]),(self.y_range[0],self.y_range[1])),
							norm    = LogNorm(),
							weights = self.values_weight[key],
							vmin    = hist_range[0],
							vmax    = hist_range[1], )
					else:
						hist_xy, bins_x, bins_y, img_xy = plt.hist2d(
							self.x_points[key],
							self.y_points[key],
							bins    = (self.x_bins,self.y_bins),
							range   = ((self.x_range[0],self.x_range[1]),(self.y_range[0],self.y_range[1])),
					#		norm    = LogNorm(),
							weights = self.values_weight[key],
							vmin    = hist_range[0],
							vmax    = hist_range[1], )

			if self.IC_workinprogress:
				if np.isnan(self.position_IC_workinprogress[0]):
					self.position_IC_workinprogress[0]=(self.x_range[1]+self.x_range[0])/2.
				if np.isnan(self.position_IC_workinprogress[1]):
					self.position_IC_workinprogress[1]=(self.y_range[1]+self.y_range[0])/2.

				self.ax.text(
					self.position_IC_workinprogress[0],
					self.position_IC_workinprogress[1],
					"IceCube Work-in-Progress",
					horizontalalignment="center",
					verticalalignment="center",
					size=16, color="red" )

			if self.IC_preliminary:
				if np.isnan(self.position_IC_preliminary[0]):
					self.position_IC_preliminary[0]=(self.x_range[1]+self.x_range[0])/2.
				if np.isnan(self.position_IC_preliminary[1]):
					self.position_IC_preliminary[1]=(self.y_range[1]+self.y_range[0])/2.

				self.ax.text(
					self.position_IC_preliminary[0],
					self.position_IC_preliminary[1],
					"IceCube Preliminary",
					horizontalalignment="center",
					verticalalignment="center",
					size=16, color="red" )

			plt.xlabel(self.x_label)
			plt.ylabel(self.y_label)
			plt.suptitle( self.title[key], y=0.97, fontsize="large" )
			if any([ hx>0 for hy in hist_xy for hx in hy ]):
				if self.colorbar_range:
					plt.clim(*self.colorbar_range)
				cbar=plt.colorbar()
#				cbar.set_label(self.colorbar_label, rotation=270)
				cbar.ax.get_yaxis().labelpad = 30
				cbar.ax.set_ylabel(self.colorbar_label, rotation=270)

			if self.IC_preliminary:
				if self.poskey_IC_preliminary:
					py, px  = str(self.poskey_IC_preliminary[0]), str(self.poskey_IC_preliminary[1])
					px_keys = { "l": 0.20, "c": 0.50, "r": 0.80 } # left,  center, right
					py_keys = { "l": 0.20, "c": 0.50, "u": 0.80 } # lower, center, upper
					alignx_keys = { "l": "left", "c": "center", "r": "right" }
					xwidth = (self.x_range[1]-self.x_range[0])
					self.position_IC_preliminary[0] = self.x_range[0] + xwidth *  px_keys[px]
					xpos                            = self.x_range[0] + xwidth *  px_keys[px]
					self.position_IC_preliminary[1] = self.y_range[0] + (self.y_range[1]-self.y_range[0]) *  py_keys[py]
					ypos_ic_0                       = self.y_range[0] + (self.y_range[1]-self.y_range[0]) * (py_keys[py]-0.03+0.000)
					ypos_ic_1                       = self.y_range[0] + (self.y_range[1]-self.y_range[0]) * (py_keys[py]-0.03+0.008)
					ypos_prlm_0                     = self.y_range[0] + (self.y_range[1]-self.y_range[0]) * (py_keys[py]-0.03-0.070)
					ypos_prlm_1                     = self.y_range[0] + (self.y_range[1]-self.y_range[0]) * (py_keys[py]-0.03-0.065)
#					if self.y_log:
#						self.position_IC_preliminary[1]=self.y_range[0]*(self.y_range[1]/self.y_range[0])**py_keys[py]
#						ypos_ic_0                      =self.y_range[0]*(self.y_range[1]/self.y_range[0])**(py_keys[py]-0.03+0.000)
#						ypos_ic_1                      =self.y_range[0]*(self.y_range[1]/self.y_range[0])**(py_keys[py]-0.03+0.008)
#						ypos_prlm_0                    =self.y_range[0]*(self.y_range[1]/self.y_range[0])**(py_keys[py]-0.03-0.070)
#						ypos_prlm_1                    =self.y_range[0]*(self.y_range[1]/self.y_range[0])**(py_keys[py]-0.03-0.065)
#					self.ax.text( xpos, ypos_ic_0,
#						"IceCube",
#						horizontalalignment=alignx_keys[px],
#						verticalalignment="center",
#						size=20, color="red" ) #, variant="small-caps" )
#					self.ax.text( xpos, ypos_prlm_0,
#						"Preliminary",
#						horizontalalignment=alignx_keys[px],
#						verticalalignment="center",
#						size=16, color="red" ) #, variant="small-caps" )
					self.ax.text( xpos-xwidth*0.14,  ypos_ic_0,   "I",          horizontalalignment="center", verticalalignment="bottom", size=32, color="red" )
					self.ax.text( xpos-xwidth*0.083, ypos_ic_1,   "CE",         horizontalalignment="center", verticalalignment="bottom", size=24, color="red" )
					self.ax.text( xpos-xwidth*0.01,  ypos_ic_0,   "C",          horizontalalignment="center", verticalalignment="bottom", size=32, color="red" )
					self.ax.text( xpos+xwidth*0.09,  ypos_ic_1,   "UBE",        horizontalalignment="center", verticalalignment="bottom", size=24, color="red" )
					self.ax.text( xpos-xwidth*0.13,  ypos_prlm_0, "P",          horizontalalignment="center", verticalalignment="bottom", size=20, color="red" )
					self.ax.text( xpos+xwidth*0.02,  ypos_prlm_1, "RELIMINARY", horizontalalignment="center", verticalalignment="bottom", size=15, color="red" )


			if self.has_line:
				self.ax.add_line(line_cut)

			fig = matplotlib.pyplot.gcf()
			fig.set_size_inches(8, 6)
			if self.larger_marks:
				fig.set_size_inches(6.4, 4.8)

			plt.savefig(self.path_save+self.name_save+"__"+self.key_title[key]+".pdf")

			plt.close()






class ABPlotCorrMat:

	def __init__(self):
		import matplotlib
		matplotlib.use('Agg')
		import matplotlib.pyplot as plt
		from matplotlib.colors import LogNorm
		from matplotlib import cm
		#matplotlib.rcParams['font.family']='serif'
		matplotlib.rcParams['font.family']='STIXGeneral'
		matplotlib.rcParams['font.size']=18
		matplotlib.rcParams['axes.grid']=True
#		matplotlib.rcParams.update({'font.size': 18})
#		matplotlib.rcParams['mathtext.default']='regular'
#		matplotlib.rcParams['xtick.labelsize']='x-small'
#		matplotlib.rcParams['ytick.labelsize']='x-small'
#		matplotlib.rcParams['legend.fontsize']='x-small'
#		matplotlib.rcParams['legend.fontsize']='normal'
		matplotlib.rcParams['legend.numpoints']=1

		self.data_keys=[]
		self.legend={}
		self.data_sets={}
		self.title="The Plot Title"
		self.axis_range=[0.,1.]
		self.n_bins=1
		self.values_log=False
#		self.IC_preliminary=False
#		self.position_IC_preliminary=[np.nan,np.nan]
		self.IC_workinprogress=False
		self.position_IC_workinprogress=[np.nan,np.nan]
		self.path_save=""
		self.name_save=""
		self.larger_marks=True
		self.verbose=1

	def set_title(self, title):
		self.title   = title

	def plot(self):

		self.ax = plt.subplot(111)

		self.axis_range = [0.,float(len(self.data_keys))]
		self.n_bins     = len(self.data_keys)

		self.correlation_matrix = np.corrcoef( np.array([ np.nan_to_num(self.data_sets[key]) for key in self.data_keys ]) )

		for i in range(len(self.data_keys)):
			self.correlation_matrix[i][i]=np.nan

		im=plt.imshow(self.correlation_matrix, interpolation="nearest", vmin=-1., vmax=1.)

	#	if self.IC_workinprogress:
	#		if np.isnan(self.position_IC_workinprogress[0]):
	#			self.position_IC_workinprogress[0]=(self.axis_range[1]+self.axis_range[0])/2.
	#		if np.isnan(self.position_IC_workinprogress[1]):
	#			self.position_IC_workinprogress[1]=(self.axis_range[1]+self.axis_range[0])/2.

	#		self.ax.text(
	#			self.position_IC_workinprogress[0],
	#			self.position_IC_workinprogress[1],
	#			"IceCube Work-in-Progress",
	#			horizontalalignment="center",
	#			verticalalignment="center",
	#			size=16, color="red" )

		self.ax.set_xticklabels( [ self.legend[key] for key in self.data_keys ], rotation=90)
		self.ax.set_yticklabels( [ self.legend[key] for key in self.data_keys ] )
		self.ax.set_xticks( list(range(self.n_bins)) )
		self.ax.set_yticks( list(range(self.n_bins)) )

		fig = matplotlib.pyplot.gcf()
		fig.set_size_inches(8, 6)
		if self.larger_marks:
			fig.set_size_inches(6.4, 5.6)
		fig.subplots_adjust(left=0.3)
		fig.subplots_adjust(bottom=0.3)

#		cbar=plt.colorbar(im)
##		cbar.set_label(self.colorbar_label, rotation=270)
#		cbar.ax.get_yaxis().labelpad = 30
#		cbar.ax.set_ylabel("Correlation Coefficient", rotation=270)
#		cbar.ticks([-1.,-0.5,0,0.5,1.])

		plt.suptitle( self.title, y=0.97, fontsize="large" )
		plt.colorbar()

		plt.savefig(self.path_save+self.name_save+".pdf")

		plt.close()









class ABPlotCorrRow:

	def __init__(self):
		import matplotlib
		matplotlib.use('Agg')
		import matplotlib.pyplot as plt
		from matplotlib.colors import LogNorm
		from matplotlib import cm
		#matplotlib.rcParams['font.family']='serif'
		matplotlib.rcParams['font.family']='STIXGeneral'
		matplotlib.rcParams['font.size']=18
		matplotlib.rcParams['axes.grid']=True
#		matplotlib.rcParams.update({'font.size': 18})
#		matplotlib.rcParams['mathtext.default']='regular'
#		matplotlib.rcParams['xtick.labelsize']='x-small'
#		matplotlib.rcParams['ytick.labelsize']='x-small'
#		matplotlib.rcParams['legend.fontsize']='x-small'
#		matplotlib.rcParams['legend.fontsize']='normal'
		matplotlib.rcParams['legend.numpoints']=1

		self.data_keys=[]
		self.legend={}
		self.data_sets={}
		self.title="The Plot Title"
		self.single_key = ""
		self.axis_range=[0.,1.]
		self.n_bins=1
		self.values_log=False
#		self.IC_preliminary=False
#		self.position_IC_preliminary=[np.nan,np.nan]
		self.IC_workinprogress=False
		self.position_IC_workinprogress=[np.nan,np.nan]
		self.path_save=""
		self.name_save=""
		self.larger_marks=True
		self.verbose=1

	def set_title(self, title):
		self.title   = title

	def plot(self):

		self.ax = plt.subplot(111)
		if self.single_key not in self.data_keys:
			exit("Single key not in data keys list")
		self.data_keys = [self.single_key] + [ dk for dk in self.data_keys if dk!=self.single_key ]

		self.axis_range = [1.,float(len(self.data_keys))]
		self.n_bins     = len(self.data_keys)

		self.correlation_matrix = np.corrcoef( np.array([ np.nan_to_num(self.data_sets[key]) for key in self.data_keys ]) )

		for i in range(len(self.data_keys)):
			self.correlation_matrix[i][i]=np.nan

		im=plt.imshow(self.correlation_matrix, interpolation="nearest", vmin=-1., vmax=1.)

	#	if self.IC_workinprogress:
	#		if np.isnan(self.position_IC_workinprogress[0]):
	#			self.position_IC_workinprogress[0]=(self.axis_range[1]+self.axis_range[0])/2.
	#		if np.isnan(self.position_IC_workinprogress[1]):
	#			self.position_IC_workinprogress[1]=(self.axis_range[1]+self.axis_range[0])/2.

	#		self.ax.text(
	#			self.position_IC_workinprogress[0],
	#			self.position_IC_workinprogress[1],
	#			"IceCube Work-in-Progress",
	#			horizontalalignment="center",
	#			verticalalignment="center",
	#			size=16, color="red" )

		self.ax.set_xticklabels( [ self.legend[key] for key in self.data_keys[1:] ], rotation=90)
		self.ax.set_yticklabels( [ self.legend[key] for key in self.data_keys[0:1] ] )
		self.ax.set_xticks( list(range(self.n_bins))[1:] )
		self.ax.set_yticks( list(range(self.n_bins))[0:1] )
		self.ax.set_xlim( [list(range(self.n_bins))[1:][0]-0.5,list(range(self.n_bins))[1:][-1]+0.5] )
		self.ax.set_ylim( [list(range(self.n_bins))[0:1][0]-0.5,list(range(self.n_bins))[0:1][-1]+0.5] )

		fig = matplotlib.pyplot.gcf()
		fig.set_size_inches(8, 4)
		if self.larger_marks:
			fig.set_size_inches(6.4, 5.6)
		fig.subplots_adjust(left=0.3)
		fig.subplots_adjust(bottom=0.3)

#		cbar=plt.colorbar(im)
##		cbar.set_label(self.colorbar_label, rotation=270)
#		cbar.ax.get_yaxis().labelpad = 30
#		cbar.ax.set_ylabel("Correlation Coefficient", rotation=270)
#		cbar.ticks([-1.,-0.5,0,0.5,1.])

		plt.suptitle( self.title, y=0.97, fontsize="large" )
		plt.colorbar()

		plt.savefig(self.path_save+self.name_save+".pdf")

		plt.close()








































'''

####
#
#   THIS BELOW WAS USED FOR THE ARIANNA ANTENNA PLOTTING
#
####

def plot_this( configs, confdir, filename, data_origin, x_keys, y_keys, x_arrays, y_arrays, otherkeys, linecolors ):

	autocols = ["y-","r-","g-","b-","c-","m-"]

	plt.figure()

	ax = plt.subplot(111)

	x_key   = x_keys[0]
	y_key   = y_keys[0]
	x_array = x_arrays[0]
	y_array = y_arrays[0]

	title_xy = configs["plot"]["title"][x_key][y_key][data_origin]
	label_x  = configs["plot"]["label"][x_key][data_origin]
	label_y  = configs["plot"]["label"][y_key][data_origin]
	range_x  = configs["plot"]["range"][x_key]
	range_y  = configs["plot"]["range"][y_key]
	lines_xy = []

	for ind, y_key, y_array, otherkey, linecolor in zip(range(len(y_keys)), y_keys, y_arrays, otherkeys, linecolors):
		col = linecolor
		if linecolor == "auto":
			col = autocols[ind%len(autocols)]
		legend_x = configs["plot"]["legend"][x_key][data_origin][otherkey]
		legend_y = configs["plot"]["legend"][y_key][data_origin][otherkey]

		if y_key=="groupdelay_theo":
			line_xy, = plt.plot( x_array, y_array, col )
		#	line_theo, = plt.plot( x_array, y_array, col, label=legend_y )
		#	theo_leg = plt.legend(handles=[line_theo], loc=1)
		#	ax = plt.gca().add_artist(theo_leg)
		else:
			line_xy, = plt.plot( x_array, y_array, col, label=legend_y )
			#lines_xy.append(line_xy)



	plt.xlim(range_x)
	plt.ylim(range_y)

	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width, box.height*0.9])
	plt.legend( loc="lower center", bbox_to_anchor=(0.5, 1.015), ncol=2, borderaxespad=0.,frameon=False)
	plt.xlabel( label_x )
	plt.ylabel( label_y )
	plt.suptitle( title_xy, fontsize="large" )

	plt.savefig(confdir+"/"+configs["directory"]["plots"]+"/plot___"+filename.replace("/","___")+".pdf")

'''








