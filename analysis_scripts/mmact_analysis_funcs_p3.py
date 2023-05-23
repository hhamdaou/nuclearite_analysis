--- /mnt/ceph1-npx/user/hhamdaoui/nuclearite_analysis/analysis_scripts/mmact_analysis_funcs.py	(original)
+++ /mnt/ceph1-npx/user/hhamdaoui/nuclearite_analysis/analysis_scripts/mmact_analysis_funcs.py	(refactored)
@@ -76,7 +76,7 @@
 		if frame["EHEPortiaEventSummarySRT"].GetTotalBestNPE()>=value:
 			passed_cut = True
 		if passed_cut is True:
-			print 'passed npe cut :', passed_cut
+			print('passed npe cut :', passed_cut)
 	return passed_cut
 #def cut_eheana_npe_above_25000(frame):
 #	return cut_eheana_npe_above_value(frame,25000.)
@@ -88,7 +88,7 @@
 		if frame["EHEPortiaEventSummarySRT"].GetTotalNch()>=value:
 			passed_cut = True
 		if passed_cut is True:
-			print 'passed Nch cut :', passed_cut
+			print('passed Nch cut :', passed_cut)
 	return passed_cut
 #def cut_eheana_nch_above_100(frame):
 #	return cut_eheana_nch_above_value(frame,100.)
@@ -100,7 +100,7 @@
 		if frame["EHEOpheliaSRT_ImpLF"].fit_quality>=value:
 			passed_cut = True
 		if passed_cut is True:
-			print 'passed fit_quality cut :', passed_cut
+			print('passed fit_quality cut :', passed_cut)
 	return passed_cut
 #def cut_eheana_fitquality_above_30(frame):
 #	return cut_eheana_fitquality_above_value(frame,30.)
@@ -112,7 +112,7 @@
 		if np.log10(frame["EHEPortiaEventSummarySRT"].GetTotalBestNPE())>=value:
 			passed_cut = True
 		if passed_cut is True:
-			print 'passed log10(npe) cut :', passed_cut
+			print('passed log10(npe) cut :', passed_cut)
 	return passed_cut
 
 # log10(npe) depending on fit_quality
@@ -134,7 +134,7 @@
 		log10npe_limit = 5.2
 	passed_cut = keep_log10npe_above_value(frame,log10npe_limit)
 	if passed_cut is True:
-		print 'passed log10(npe) depending on fit_quality :', passed_cut
+		print('passed log10(npe) depending on fit_quality :', passed_cut)
 	return passed_cut
 
 # log10(npe) depending on cos(zenith)
@@ -152,7 +152,7 @@
 		log10npe_limit = 4.6 + 1.85*np.sqrt(1-((coszenith-1.)/0.94)**2)
 	passed_cut = keep_log10npe_above_value(frame,log10npe_limit)
 	if passed_cut is True:
-		print 'log10(npe) depending on cos(zenith):', passed_cut
+		print('log10(npe) depending on cos(zenith):', passed_cut)
 	return passed_cut
 
 # decrease counting weight of each event
@@ -185,7 +185,7 @@
 	if lev=="trigger":
 		passed_cut = True
 		if passed_cut is False:
-			print 'Trigger Failed'
+			print('Trigger Failed')
 	# Trigger Level
 	if lev=="ehefilter":
 		passed_cut = keep_slop(frame)
@@ -581,8 +581,8 @@
 
 	p_tlength = np.linalg.norm(p_dir)/p_speed
 
-	prod_angle_t = np.array([ hit_prod_angle( p_t, p_pos, p_tlength, p_dir, hit.time, np.array([x for x in omgeo[omkey].position]), indexofrefraction ) for omkey, hitlist in pulsemap.items() for hit in hitlist ])
-	prod_weights = np.array([ hit.charge for omkey, hitlist in pulsemap.items() for hit in hitlist ])
+	prod_angle_t = np.array([ hit_prod_angle( p_t, p_pos, p_tlength, p_dir, hit.time, np.array([x for x in omgeo[omkey].position]), indexofrefraction ) for omkey, hitlist in list(pulsemap.items()) for hit in hitlist ])
+	prod_weights = np.array([ hit.charge for omkey, hitlist in list(pulsemap.items()) for hit in hitlist ])
 
 	prod_angle_t = prod_angle_t.transpose()
 
@@ -622,7 +622,7 @@
 	                                                                np.array([track.dir.x,track.dir.y,track.dir.z]), \
 	                                                                np.array([w for w in omgeo[omkey].position]) ) ) \
 	                       <= max_dist \
-	                for omkey, hitlist in pm.items() }
+	                for omkey, hitlist in list(pm.items()) }
 
 	# Deleting the output map if already there
 	del frame[output_pm_name]
@@ -786,7 +786,7 @@
           "t_burn": { "IC40":     35.32, "IC59":     33.04, "IC79":     33.23,
                       "IC86-I":   33.56, "IC86-II":  34.70, "IC86-III": 33.98,
                       "IC86-IV":  34.71, "IC86-V":   37.17, "IC86-VI":   0.0,   }, }
-	return sum([ t["t_live"][icxx]-t["t_burn"][icxx] for icxx in t["t_live"].keys() if "IC86" in icxx ]) * I3Units.day
+	return sum([ t["t_live"][icxx]-t["t_burn"][icxx] for icxx in list(t["t_live"].keys()) if "IC86" in icxx ]) * I3Units.day
 
 # THIS IS THE CORRECT EXPERIMENTAL LIVETIME
 def t_live_IC86_exprm(startyr,endyr,whichsample="phys"):
@@ -1023,8 +1023,8 @@
 
 def read_ABurgmanGenNum(frame):
 	gen, num = "", ""
-	gen = "__".join([g for g,k in frame["ABurgmanGen"].items() if k])
-	num = "__".join([n for n,k in frame["ABurgmanNum"].items() if k])
+	gen = "__".join([g for g,k in list(frame["ABurgmanGen"].items()) if k])
+	num = "__".join([n for n,k in list(frame["ABurgmanNum"].items()) if k])
 	if "__" in gen:
 		exit("More than one gen given")
 	if "__" in num:
@@ -1047,16 +1047,16 @@
 	pm = I3RecoPulseSeriesMap.from_frame(frame,input_pm_name)
 
 	# Extracting a sorted list of the recorded charge of each DOM in the hit map
-	alltotcharges = np.sort([ sum([hit.charge for hit in hitlist]) for hitlist in pm.values() ])[::-1]
+	alltotcharges = np.sort([ sum([hit.charge for hit in hitlist]) for hitlist in list(pm.values()) ])[::-1]
 
 	# Recording the dimmest charge among the ten percent brightest DOMs
 	dimmestbrightcharge = alltotcharges[int(0.1*len(alltotcharges))+1]
 
 	# The DOMs that are bright enough, i.e. have a summed charge higher than the dimmest allowed charge
-	brightenough = { omkey: sum([hit.charge for hit in hitlist])>dimmestbrightcharge for omkey, hitlist in pm.items() }
+	brightenough = { omkey: sum([hit.charge for hit in hitlist])>dimmestbrightcharge for omkey, hitlist in list(pm.items()) }
 
 	# The index of the median hit per hit DOM
-	indexmedian = { omkey: int(0.5*len(hitlist)) for omkey, hitlist in pm.items() }
+	indexmedian = { omkey: int(0.5*len(hitlist)) for omkey, hitlist in list(pm.items()) }
 
 	# Deleting the output map if already there
 	del frame[output_pm_name]
@@ -1068,7 +1068,7 @@
 #	add_BrightestMedianMap(frame,"InIcePulsesSRTTW","BrightestMedianInIcePulsesSRTTW")
 
 def delete_all_CV(frame):
-	for framekey in frame.keys():
+	for framekey in list(frame.keys()):
 		if "CV_" in framekey:
 			del frame[framekey]
 
