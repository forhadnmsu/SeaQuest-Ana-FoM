posCut = "atan(y1_st3/y1_st1)>1.2 && atan(y1_st3/y1_st1) <1.6&& z1_v > -31.5 && z1_v < 145.0&& x1_t*x1_t+(y1_t-1.6)*(y1_t-1.6) <1300.0 && x1_d*x1_d+(y1_d-1.6)*(y1_d-1.6) <93.0&& abs(px1_st1-px1_st3)> 0.415 &&  abs(px1_st1-px1_st3)<0.425 && abs(py1_st1-py1_st3)< 0.01&& abs(pz1_st1-pz1_st3)<0.05&&(chisq1_target-chisq1_dump) >-2.5 && (chisq1_target-chisq1_dump)<77.5&&  pz1_st1 > 10 && pz1_st1 < 78 && nHits1 > 13 &&(y1_st1*y1_st3) > 0 &&"
negCut = "atan(y2_st3/y2_st1)>1.2 && atan(y2_st3/y2_st1) <1.6&& z2_v > -31.5 && z2_v < 145.0&& x2_t*x2_t+(y2_t-1.6)*(y2_t-1.6) <1300.0 && x2_d*x2_d+(y2_d-1.6)*(y2_d-1.6) <93.0&& abs(px2_st1-px2_st3)> 0.415 &&  abs(px2_st1-px2_st3)<0.425 && abs(py2_st1-py2_st3)< 0.01&& abs(pz2_st1-pz2_st3)<0.05&&(chisq2_target-chisq2_dump) >-2.5 && (chisq2_target-chisq2_dump)<77.5&&  pz2_st1 > 10 && pz2_st1 < 78 && nHits2 > 13 &&(y2_st1*y2_st3) > 0&&"
dimuCut=  "dz>0.0 && dz< 130.0&& abs(dx) < 0.2 && abs(dy-1.6) < 0.2 &&  abs(dpx) < 2.0 && abs(dpy) < 2.4 && dpz > 32.0 && dpz < 102.0 && dpx*dpx + dpy*dpy < 4.5 && dx*dx + (dy-1.6)*(dy-1.6) < 0.06  && y1_st3*y2_st3 < 0 && nHits1 + nHits2 > 29 && nHits1St1 + nHits2St1 > 8&&"
trigger ="fpga1==1&&"
physics="costh<0.5 && mass>4.5 && mass<8.0"
event_filter_mc= posCut+negCut+dimuCut+trigger+physics
event_filter_data= posCut+negCut+dimuCut+physics

#print (posCut)
#print (negCut)
#print (dimuCut)
#print (event_filter_mc)

