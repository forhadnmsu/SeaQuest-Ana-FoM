import ROOT
from ROOT import TCanvas,TLine, TFile, TProfile, TNtuple, TH1F,TH1D, TH2F, TCut
from ROOT import gROOT, gBenchmark, gRandom, gSystem, gStyle, gROOT,TStyle
from ROOT import TPaveLabel, TPave, TArrow, TText, TPaveText
import numpy as np
import cut
from math import *

ROOT.EnableImplicitMT()
ROOT.gStyle.SetHistLineWidth(2)
ROOT.gStyle.SetOptStat(0)
bin_y_offset=20
n_bin=100
bin_low=-50.0
bin_high=50.0
binlow_p=-5.0
binhi_p=5.0

print("event selection: ",cut.event_filter_mc)
event_filter_mc=cut.event_filter_mc
event_filter_data=cut.event_filter_data
cut_lists=[
	   ["ptrk_x_d",[int(n_bin),float(bin_low),float(bin_high)],"x1_d","x position of #mu^{+} at dump;x1_d; Counts"],
 	   ["ntrk_x_d",[int(n_bin),float(bin_low),float(bin_high)],"x2_d","x position of #mu^{-} at dump;x2_d; Counts"], 
 	   ["ptrk_x_t",[int(n_bin),float(bin_low),float(bin_high)],"x1_t","x position of #mu^{+} at target;x1_t; Counts"], 
 	   ["ntrk_x_t",[int(n_bin),float(bin_low),float(bin_high)],"x2_t","x position of #mu^{-} at target;x2_t; Counts"], 

	   ["ptrk_y_d", [int(n_bin),float(bin_low),float(bin_high)],"y1_d","y position of #mu^{+} at dump;y1_d; Counts"],
           ["ntrk_y_d", [int(n_bin),float(bin_low),float(bin_high)],"y2_d","y position of #mu^{-} at dump;y2_d; Counts"], 
           ["ptrk_y_t", [int(n_bin),float(bin_low),float(bin_high)],"y1_t","y position of #mu^{+} at target;y1_t; Counts"], 
           ["ntrk_y_t", [int(n_bin),float(bin_low),float(bin_high)],"y2_t","y position of #mu^{-} at target;y2_t; Counts"], 

	   ["px1_st1",[int(n_bin),float(binlow_p),float(binhi_p)],"px1_st1","px position of #mu^{+} at St1;px1_st1; Counts"],
 	   ["px2_st1",[int(n_bin),float(binlow_p),float(binhi_p)],"px2_st1","px position of #mu^{-} at St1;px2_st1; Counts"], 
 	   ["px1_st3",[int(n_bin),float(binlow_p),float(binhi_p)],"px1_st3","px position of #mu^{+} at St3;px1_st3; Counts"], 
 	   ["px2_st3",[int(n_bin),float(binlow_p),float(binhi_p)],"px2_st3","px position of #mu^{-} at St3;px2_st3; Counts"], 

	   ["py1_st1",[int(n_bin),float(binlow_p),float(binhi_p)],"py1_st1", "py momentum of #mu^{+} at St1;py1_st1; Counts"],
           ["py2_st1",[int(n_bin),float(binlow_p),float(binhi_p)],"py2_st1", "py momentum of #mu^{-} at St1;py2_st1; Counts"], 
           ["py1_st3",[int(n_bin),float(binlow_p),float(binhi_p)],"py1_st3", "py momentum of #mu^{+} at St3;py1_st3; Counts"], 
           ["py2_st3",[int(n_bin),float(binlow_p),float(binhi_p)],"py2_st3", "py momentum of #mu^{-} at St3;py2_st3; Counts"], 
  ]

rdf_mc = ROOT.RDataFrame("result_mc", "combinedLH2GMC.root")  # Messy MC 
rdf_unmix = ROOT.RDataFrame("result", "combinedLH2Data.root") # Unmix roadset-67-LH2 data
rdf_mix = ROOT.RDataFrame("result_mix", "combinedLH2Data.root") #mix roadset-67-LH2 data

def getSig(h_data_signal,h_mc):
	c01 = ROOT.TCanvas("c01","c01",1200,1200)
	#c01.Divide(2,2)
	factor = h_data_signal.Integral();
	h_mc.Scale(factor/h_mc.Integral());
	n1 = h_data_signal.GetMaximum();
	n2 = h_mc.GetMaximum();
	if n1>n2:
		h_data_signal.SetMaximum(n1+0.01*n1);
	else:
		h_data_signal.SetMaximum(n2+0.01*n2);
	h_data_signal.Draw("HIST")
	h_data_signal.SetLineColor(2)
	h_mc.Draw("HIST same")
	h_mc.SetLineColor(7)
	#h_mc.GetYaxis().SetMaxDigits(3)
	h_mc.SetTitle("Monte Carlo: "+ str(cut_lists[i_list][3])+"Counts")
	c01.SaveAs("plot/test_"+str(i_list)+".png")
	return h_data_signal

for i_list in range(0,len(cut_lists)):
	print ("cut list 2 ",cut_lists[i_list][1][0], cut_lists[i_list][1][1], cut_lists[i_list][1][2])
	hMC = rdf_mc.Filter(event_filter_mc).Define("def_mc",str(cut_lists[i_list][2])).Histo1D((str(cut_lists[i_list][2]),str(cut_lists[i_list][3]), cut_lists[i_list][1][0], cut_lists[i_list][1][1], cut_lists[i_list][1][2]),"def_mc", "weight")
	hData = rdf_unmix.Filter(event_filter_data).Define("def_data",str(cut_lists[i_list][2])).Histo1D((str(cut_lists[i_list][2]),str(cut_lists[i_list][3]), cut_lists[i_list][1][0], cut_lists[i_list][1][1], cut_lists[i_list][1][2]),"def_data")
	hDataMix = rdf_mix.Filter(event_filter_data).Define("def_mix",str(cut_lists[i_list][2])).Histo1D((str(cut_lists[i_list][2]),str(cut_lists[i_list][3]), cut_lists[i_list][1][0], cut_lists[i_list][1][1], cut_lists[i_list][1][2]),"def_mix")
	hData_signal = hData.Clone("hData_signal")
        #hData_signal.Draw()
	hData_signal.Add(hDataMix.GetPtr(), -1)
	h_sig = getSig(hData_signal,hMC) 
