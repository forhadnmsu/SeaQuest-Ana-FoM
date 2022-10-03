import ROOT
from ROOT import TPaveLabel, TPave, TArrow, TText, TPaveText, TH1, TH2
import numpy as np
from math import *
TH1.SetDefaultSumw2(True)
TH2.SetDefaultSumw2(True)
ROOT.EnableImplicitMT()
ROOT.gStyle.SetHistLineWidth(2)
ROOT.gStyle.SetOptStat(0)
bin_y_offset=20
bin_low=0.0
bin_high=0.3

cut_lists=[["atan(y1_st3/y1_st1)",[50,0.4,1.8], "atan_y1_st3_y1_st1","atan(y1_st3/y1_st1);atan(y1_st3/y1_st1);"],
	["atan(y2_st3/y2_st1)",[50,0.4,1.8], "atan_y2_st3_y2_st1","atan(y2_st3/y2_st1);atan(y2_st3/y2_st1);"],
	["z1_v",[50,-250,250], "z1_v","z1_v;z2_v;"],
	["z2_v",[50,-250,250], "z2_v","z2_v;z2_v;"],
	["pz1_st1",[20,5,80], "pz1_st1","pz1_st1;pz1_st1;"],
	["pz2_st1",[20,5,80], "pz2_st1","pz2_st1;pz2_st1;"],
	["x1_t*x1_t+(y1_t-1.6)*(y1_t-1.6)",[50,0,1500], "x1_t1_y1_toffset2","#mu^{+} Transverse Distance at Target;x1_t*x1_t+(y1_t-1.6)*(y1_t-1.6);"],
	["x1_d*x1_d+(y1_d-1.6)*(y1_d-1.6)",[50,0,300], "x1_d1_y1_toffset2","#mu^{-} Transverse Distance at Dump;x1_d*x1_d+(y1_d-1.6)*(y1_d-1.6);"],
	["x2_t*x2_t+(y2_t-1.6)*(y2_t-1.6)",[50,0,1500], "x2_t2_y2_toffset2","#mu^{+} Transverse Distance at Target;x2_t*x2_t+(y2_t-1.6)*(y2_t-1.6);"],
	["x2_d*x2_d+(y2_d-1.6)*(y2_d-1.6)",[50,0,300], "x2_d2_y2_toffset2","#mu^{-} Transverse Distance at Dump;x2_d*x2_d+(y2_d-1.6)*(y2_d-1.6);"],
	["abs(px1_st1-px1_st3)",[50,0.412,0.42], "px1_st1_px1_st3","abs(Px_{#mu+}^{}_{st1} - Px_{#mu+}^{}_{st3});abs(px1_st1 − px1_st3);"],
	["abs(py1_st1-py1_st3)",[50,0,0.005], "py1_st1_py1_st3","abs(Py_{#mu+}^{}_{st1} - Py_{#mu+}^{}_{st3});abs(py1_st1 − py1_st3);"],
	["abs(px2_st1-px2_st3)",[50,0.412,0.42], "px2_st1_px2_st3","abs(Px_{#mu-}^{}_{st1} - Px_{#mu-}^{}_{st3});abs(px2_st1 − px2_st3);"],
	["abs(py2_st1-py2_st3)",[50,0,0.005], "py2_st1_py2_st3","abs(Py_{#mu-}^{}_{st1} - Py_{#mu-}^{}_{st3});abs(py2_st1 − py2_st3);"],
	["abs(pz1_st1-pz1_st3)",[50,0,0.06], "pz1_st1_pz1_st3","abs(Pz_{#mu+}^{}_{st1} - Pz_{#mu+}^{}_{st3});abs(pz1_st1 − pz1_st3);"],
	["abs(pz2_st1-pz2_st3)",[50,0,0.06], "pz2_st1_pz2_st3","abs(Pz_{#mu-}^{}_{st1} - Pz_{#mu-}^{}_{st3});abs(pz2_st1 − pz2_st3);"],
	["chisq1_target-chisq1_dump",[20,-20,80], "chisq1_target-chisq1_dump","#chi_{#mu+}^{2}_{target} - #chi_{#mu+}^{2}_{dump}; chisq1_target - chisq1_dump;"],
	["chisq2_target-chisq2_dump",[20,-20,80], "chisq2_target-chisq2_dump","#chi_{#mu-}^{2}_{target} - #chi_{#mu-}^{2}_{dump}; chisq2_target - chisq2_dump;"],
	["y1_st1*y1_st3",[50,0,2000], "y1_st1*y1_st3","y1_st1*y1_st3;y1_st1*y1_st3;"],
	["y2_st1*y2_st3",[50,0,2000], "y2_st1*y2_st3","y2_st1*y2_st3;y2_st1*y2_st3;"],
	["nHits1 + nHits2",[30,20.5,50.5],"nHits1 + nHits2","nHits in #mu^{+} and #mu^{-} tracks combined; nHits1 + nHits2;"],
	["nHits1St1 + nHits2St1",[20,0.5,20.5],"nHits1St1 + nHits2St1","nHits of #mu^{+} and #mu^{-} in St1 ;nHits1St1 + nHits2St1;"],
	["dz",[50,-200,250], "vetrex_z","vetrex_z;vetrex_z;"],
	["abs(dy-1.6)",[50,0,0.5], "vertex_y-1.6","Dimuon vertex: (y-1.6cm) ;vertex_y_1.6;"],
	["abs(x1_st1 + x2_st1)",[50,0,50.0], "x_st1_st2","abs(x_{st1}^{#mu+} + x_{st1}^{#mu-});abs(x1_st1 + x2_st1)"],
	["dx*dx+(dy-1.6)*(dy-1.6)",[20,0.0,0.20], "dx2_dyOff2","dx*dx + (dy-1.6)*(dy-1.6);dx*dx + (dy-1.6)*(dy-1.6);"],
	["abs(z1_v - z2_v)",[20,0.0,200.0], "track_zVertex_diff","abs(z^{#mu+}_{v} - z^{#mu-}_{v}); abs(z1_v - z2_v);"],
	["chisq_dimuon",[50,0,50.0], "chisq_dimuon","chisq_dimuon; chisq_dimuon;"],
	["xF",[50,-1.0,1.0], "xF","xF;xF;"],
	["dpx*dpx+dpy*dpy",[50,0,10], "dpx*dpx+dpy*dpy","dpx*dpx+dpy*dpy;dpx*dpx+dpy*dpy;"],
	["abs(dpx)",[50,0,2.5], "abs(dpx)","abs(dpx);abs(dpx);"],
	["abs(dpy)",[50,0,5.5], "abs(dpy)","abs(dpy);abs(dpy);"],
	["abs(dpz)",[50,15,120], "abs(dpz)","abs(dpz);abs(dpz);"],
	["abs(dx)",[20,0,0.5], "abs(dx)","abs(dx);abs(dx);"],
	["abs(dy-1.6)",[20,0,0.4], "abs(dy-1.6)","abs(dy-1.6);abs(dy-1.6);"]
	]

event_filter_mc = "dz>0.0&&fpga1==1&&mass>4.5 && mass<8.0&&costh<0.5 &&chisq1_target>0&& chisq1_dump>0 &&chisq2_target>0&& chisq2_dump>0 && xF>-0.3&& xF<1.0"  #this filter will be applied  to the MC
event_filter_data = "dz>0.0&&costh<0.5 && mass>4.5 && mass<8.0 &&chisq1_target>0&& chisq1_dump>0 &&chisq2_target>0&& chisq2_dump>0 && xF>-0.3&& xF<1.0"  #this filter will be applied to the Data
def getSig(h_data,h_sqrt_int1,h_sqrt_int2,h_mc, h_mc_int1, h_mc_int2):
	c01 = ROOT.TCanvas("c01","c01",1200,1200)
	c01.Divide(2,2)
	c01.cd(1)
	#h_data.Add(h_data_mix.GetPtr(),-1)
	h_data.GetYaxis().SetMaxDigits(3)
	h_data.GetYaxis().SetTitleOffset(0.0)
	h_data.SetTitle("Unmix - Mix = Signal Data: "+ str(cut_lists[i_list][3])+"Counts")
	h_data.Draw("HIST")
	h_data.SetLineColor(4)
	c01.cd(2)
	h_mc.SetLineColor(2)
	h_mc.GetYaxis().SetMaxDigits(3)
	h_mc.SetTitle("Monte Carlo: "+ str(cut_lists[i_list][3])+"Counts")
	h_mc.Draw("hist")
	#c01.SaveAs("test_"+str(i_list)+".png")
	nbin = h_data.GetNbinsX()
	for i_bin in range(1,nbin+1):	
		h_sqrt_int1.SetBinContent(i_bin, ROOT.TMath.Sqrt(h_data.Integral(1,i_bin)))
		h_sqrt_int2.SetBinContent(i_bin, ROOT.TMath.Sqrt(h_data.Integral(i_bin,nbin)))
		h_mc_int1.SetBinContent(i_bin, h_mc.Integral(1,i_bin))
		h_mc_int2.SetBinContent(i_bin, h_mc.Integral(i_bin,nbin))
		#print ("i_bin: ", i_bin, "h_data bin: ",h_data.GetBinContent(i_bin), " sqrt integral: ", ROOT.TMath.Sqrt(h_data.Integral(1,i_bin)))
	'''
	c01.cd(3)
	h_mc_int1.SetMarkerStyle(21)
	h_mc_int1.SetMinimum(0)
	h_mc_int1.Divide(h_sqrt_int1)
	h_mc_int1.SetLineColor(2)
	h_mc_int1.SetTitle(str(cut_lists[i_list][3])+"FoM")
	h_mc_int1.SetName(str(hMC.GetName())+"_sig")
	h_mc_int1.Draw("HIST")
	x_bincenter= h_mc_int1.GetXaxis().GetBinCenter(h_mc_int1.GetMaximumBin())
	l = ROOT.TLine(x_bincenter,0.0,x_bincenter,h_mc_int1.GetMaximum())
	l.SetLineColor(3);
	l.Draw("same")
	'''
	c01.cd(3)
	h_mc_int2.SetMarkerStyle(21)
	h_mc_int2.SetMinimum(0)
	h_mc_int2.Divide(h_sqrt_int2)
	h_mc_int2.SetLineColor(6)
	x_bincenter2= round(h_mc_int2.GetXaxis().GetBinCenter(h_mc_int2.GetMaximumBin()),4)
	h_mc_int2.SetTitle("FoM Lower Limit: "+str(cut_lists[i_list][0])+">"+str( x_bincenter2)+";"+str(cut_lists[i_list][0])+";FoM")
	h_mc_int2.SetName(str(hMC.GetName())+"_sig")
	h_mc_int2.Draw("HIST")
	l2 = ROOT.TLine(x_bincenter2,0.0,x_bincenter2,h_mc_int2.GetMaximum())
	l2.SetLineColor(3)
	l2.Draw("same")

	c01.cd(4)
	h_mc_int1.SetMarkerStyle(21)
	h_mc_int1.SetMinimum(0)
	h_mc_int1.Divide(h_sqrt_int1)
	h_mc_int1.SetLineColor(6)
	h_mc_int1.Draw("HIST")
	x_bincenter= round(h_mc_int1.GetXaxis().GetBinCenter(h_mc_int1.GetMaximumBin()),4)
	h_mc_int1.SetTitle("FoM Upper Limit: "+str(cut_lists[i_list][0])+"<"+str( x_bincenter)+";"+str(cut_lists[i_list][0])+";FoM")
	h_mc_int1.SetName(str(hMC.GetName())+"_sig")
	h_mc_int1.Draw("HIST")
	l = ROOT.TLine(x_bincenter,0.0,x_bincenter,h_mc_int1.GetMaximum())
	l.SetLineColor(3);
	l.Draw("same")

	print("max values of bin: ", h_mc_int1.GetMaximumBin())
	print("max values of bin center: ", h_mc_int1.GetXaxis().GetBinCenter(h_mc_int1.GetMaximumBin()))

	c01.Update()
	ROOT.gPad.Update()
	#c01.SaveAs("plot/"+str(h_mc_int1.GetName())+".pdf")
	c01.SaveAs("plot/fom_"+str(i_list)+"_.pdf")
	h_sqrt_int1.Delete()
	h_sqrt_int2.Delete()
	h_mc_int1.Delete()
	h_mc_int2.Delete()
	return h_mc_int1

rdf_mc = ROOT.RDataFrame("result_mc", "combinedLH2GMC.root")  # Messy MC 
rdf_unmix = ROOT.RDataFrame("result", "combinedLH2Data.root") # Unmix roadset-67-LH2 data
rdf_mix = ROOT.RDataFrame("result_mix", "combinedLH2Data.root") #mix roadset-67-LH2 data

for i_list in range(0,len(cut_lists)):
	h1 =ROOT.TH1D("h1","h1",cut_lists[i_list][1][0], cut_lists[i_list][1][1], cut_lists[i_list][1][2])
	h2 =ROOT.TH1D("h2","h2",cut_lists[i_list][1][0], cut_lists[i_list][1][1], cut_lists[i_list][1][2])
	h3 =ROOT.TH1D("h3","h3",cut_lists[i_list][1][0], cut_lists[i_list][1][1], cut_lists[i_list][1][2])
	h4 =ROOT.TH1D("h4","h4",cut_lists[i_list][1][0], cut_lists[i_list][1][1], cut_lists[i_list][1][2])
	hMC = rdf_mc.Filter(event_filter_mc).Define("def_mc",str(cut_lists[i_list][0])).Histo1D((str(cut_lists[i_list][2]),str(cut_lists[i_list][3]), cut_lists[i_list][1][0], cut_lists[i_list][1][1], cut_lists[i_list][1][2]),"def_mc", "weight")
	hData = rdf_unmix.Filter(event_filter_data).Define("def_data",str(cut_lists[i_list][0])).Histo1D((str(cut_lists[i_list][2]),str(cut_lists[i_list][3]), cut_lists[i_list][1][0], cut_lists[i_list][1][1], cut_lists[i_list][1][2]),"def_data")
	hDataMix = rdf_mix.Filter(event_filter_data).Define("def_mix",str(cut_lists[i_list][0])).Histo1D((str(cut_lists[i_list][2]),str(cut_lists[i_list][3]), cut_lists[i_list][1][0], cut_lists[i_list][1][1], cut_lists[i_list][1][2]),"def_mix")

	hData_signal = hData.Clone("hData_signal")
	#hData_signal.Draw()
	hData_signal.Add(hDataMix.GetPtr(), -1);
	h_sig = getSig(hData_signal,h1,h2,hMC,h3, h4)
