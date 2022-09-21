import ROOT
from ROOT import TCanvas,TLine, TFile, TProfile, TNtuple, TH1F,TH1D, TH2F, TCut
from ROOT import gROOT, gBenchmark, gRandom, gSystem, gStyle, gROOT,TStyle
from ROOT import TPaveLabel, TPave, TArrow, TText, TPaveText

import numpy as np
from math import *

ROOT.EnableImplicitMT()
ROOT.gStyle.SetHistLineWidth(2)
ROOT.gStyle.SetOptStat(0)
bin_y_offset=20
bin_low=0.0
bin_high=0.3

cut_lists=["dz",
	"chisq_dump",
	"chisq1_target",
	"abs(dy-1.6)",
	"abs(x1_st1 + x2_st1)",
	"abs(z1_v - z2_v)",
	"chisq1_dump",
	"chisq2_dump",
	"abs(py1_st1-py1_st3)"]

h_bins = [[50,0,500],
	 [100,0,150],
	 [100,0,150],
	 [50,0,1.0],
	 [50,0.0,50.0],
	 [20,0.0,200.0],
	 [50,0.0,50.0],
	 [50,0.0,50.0],
	 [50,0.0,5.0]]
h_names = ["vetrex_z",
 	 "chisq_dump",
	 "chisq1_target",
	 "vertex_y_1.6",
	 "x_st1_st2",
	 "track_zVertex_diff",
	 "chisq1_dump",
	 "chisq2_dump",
	 "py2_st1_py2_st3"]

titles = ["vetrex_z; vetrex_z;",
	"chisq_dump; chisq_dump;",
	"chisq1_target; chisq1_target;", 
	"Dimuon vertex: (y-1.6cm) ;vertex_y_1.6;",
	"abs(x_{st1}^{#mu+} + x_{st1}^{#mu-});abs(x1_st1 + x2_st1);",
	"abs(z^{#mu+}_{v} - z^{#mu-}_{v}); abs(z1_v - z2_v);",
	"chisq1_dump; chisq1_dump;",
	"chisq2_dump; chisq2_dump",
	"Y Momentum Differences between St1 and St3;abs(py2_st1 − py2_st3);"]
event_filter = "dz>0&&costh<0.5 && mass>4.5 && mass<8.0 && chisq1_dump>0"  #this filter will be applied for all the FoM plots
def getSig(h_data,h_sqrt_int,h_mc, h_mc_int):
	c01 = ROOT.TCanvas("c01","c1",1800,600)
	c01.Divide(3,1)
	c01.cd(1)
	h_data.GetYaxis().SetMaxDigits(3)
	h_data.GetYaxis().SetTitleOffset(0.0)
	h_data.SetTitle(str(titles[i_list])+"Counts")
	h_data.Draw()
	h_data.SetLineColor(1)
	c01.cd(2)
	h_mc.SetLineColor(7)
	h_mc.GetYaxis().SetMaxDigits(3)
	h_mc.SetTitle(str(titles[i_list])+"Counts")
	h_mc.Draw()
	nbin = h_data.GetNbinsX()
	for i_bin in range(1,nbin+1):	
		h_sqrt_int.SetBinContent(i_bin, ROOT.TMath.Sqrt(h_data.Integral(1,i_bin)))
		h_mc_int.SetBinContent(i_bin, h_mc.Integral(1,i_bin))
		#print ("i_bin: ", i_bin, "h_hata bin: ",h_hata.GetBinContent(i_bin), " sqrt integral: ", ROOT.TMath.Sqrt(h_data.Integral(1,i_bin)))
	c01.cd(3)
	h_mc_int.SetMarkerStyle(21)
	h_mc_int.SetMinimum(0)
	h_mc_int.Divide(h_sqrt_int)
	h_mc_int.SetLineColor(2)
	h_mc_int.SetTitle(str(titles[i_list])+"FoM")
	h_mc_int.SetName(str(hMC.GetName())+"_sig")
	h_mc_int.Draw("HIST")
	print("max values of bin: ", h_mc_int.GetMaximumBin())
	print("max values of bin center: ", h_mc_int.GetXaxis().GetBinCenter(h_mc_int.GetMaximumBin()))
	x_bincenter= h_mc_int.GetXaxis().GetBinCenter(h_mc_int.GetMaximumBin())
	l = ROOT.TLine(x_bincenter,0.0,x_bincenter,h_mc_int.GetMaximum())
	l.SetLineColor(3);
	l.Draw("same")
	c01.Update()
	ROOT.gPad.Update()
	c01.SaveAs("plot/"+str(h_mc_int.GetName())+".pdf")
	h_sqrt_int.Delete()
	h_mc_int.Delete()
	return h_mc_int

rdf_mc = ROOT.RDataFrame("result_mc", "test.root")
rdf_unmix = ROOT.RDataFrame("result", "combined.root")

c02 = ROOT.TCanvas("c02","")
for i_list in range(0,len(cut_lists)):
	c02.Divide(3,1)
	print(cut_lists[i_list])
	print(h_bins[i_list][0], ": ", h_bins[i_list][1], h_bins[i_list][2])
	h1 =ROOT.TH1D("h1","h1",h_bins[i_list][0], h_bins[i_list][1], h_bins[i_list][2])
	h2 =ROOT.TH1D("h2","h2",h_bins[i_list][0], h_bins[i_list][1], h_bins[i_list][2])
	hMC = rdf_mc.Filter(event_filter).Define("def_mc",str(cut_lists[i_list])).Histo1D((str(h_names[i_list]), str(h_names[i_list]),  h_bins[i_list][0], h_bins[i_list][1], h_bins[i_list][2]),"def_mc")
	hData = rdf_unmix.Filter(event_filter).Define("def_data",str(cut_lists[i_list])).Histo1D((str(h_names[i_list]), str(h_names[i_list]),  h_bins[i_list][0], h_bins[i_list][1], h_bins[i_list][2]),"def_data")
	h_sig = getSig(hData,h1,hMC,h2)
