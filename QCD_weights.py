# First you will need to import some modules
import ROOT as rt
import ConfigParser
import argparse
from ROOT import *
import numpy as np
import functions as f 
from array import array


def main():

    rt.gStyle.SetOptFit(1);
    rt.gROOT.SetBatch(rt.kTRUE)

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', dest='era', help='ERA' ,choices = ['2016_pre','2016_post','2017','2018'], default = '2018')
    args = parser.parse_args()

    era=args.era

    # read in config 
    config = ConfigParser.ConfigParser()
    config.read('setting_for_QCD.cfg')

    if (era=="2018"): 
         inDir=config.get('INPUT','input_directory_2018')
    elif (era=="2017"):
        inDir = config.get('INPUT','input_directory_2017')
    elif  (era=="2016_pre"):
        inDir = config.get('INPUT','input_directory_2016_pre')
    elif (era=="2016_post"):
        inDir = config.get('INPUT', 'input_directory_2016_post')

    preselection = config.get('SELECTION', 'preselection')
    selection_muon_antiiso = config.get('SELECTION','selection_muon_antiiso')
    selection_electron_antiiso = config.get('SELECTION','selection_electron_antiiso')
    selection_electron_iso = config.get('ISO_SELECTION_ELECTRON','iso_ele')
    selection_os = config.get('SELECTION','selection_os')
    selection_ss = config.get('SELECTION','selection_ss')

    jet_selection = dict(config.items('JET_BINS'))

    weights_common = config.get('COMMON_WEIGHTS', 'weights_common')
    #weights_processes = dict(config.items('WEIGHTS_PER_PROCESS'))

    nbins = int(config.get('OUTPUT','nbins'))
    xmin = float(config.get('OUTPUT','xmin'))
    xmax = float(config.get('OUTPUT','xmax'))

#currently running for different Njets is done separately and the root files are hadd together, Instead of Recreate maybe update the root file everytime -> gives segmentation fault now! have to think how to fix this    
    
    if (era=="2018"):
        outFile = rt.TFile(config.get('OUTPUT','outFile_2018'), "RECREATE")
    elif (era=="2017"):
        outFile = rt.TFile(config.get('OUTPUT','outFile_2017'), "RECREATE")
    elif (era=="2016_pre"):
        outFile = rt.TFile(config.get('OUTPUT','outFile_2016_pre'), "RECREATE")       
    elif (era=="2016_post"):
        outFile= rt.TFile(config.get('OUTPUT','outFile_2016_post'),"RECREATE")    
 
 #open trees
#inDir = "/nfs/dust/cms/user/makou/bbh_analysis_NTuples/HTauTau_emu/Inputs/NTuples_QCDEstimation_2018"
    f0,tree_Data =f.openTree(inDir+"/em-NOMINAL_ntuple_MuonEG_"+era+".root","TauCheck")
    f1,tree_TTbar = f.openTree(inDir+"/em-NOMINAL_ntuple_TTbar_"+era+".root", "TauCheck") 
    f2,tree_DYJets =f.openTree(inDir+"/em-NOMINAL_ntuple_DYJets_"+era+".root", "TauCheck")
    f3,tree_SingleTop = f.openTree(inDir+"/em-NOMINAL_ntuple_SingleTop_"+era+".root", "TauCheck" )          
    f4,tree_WJets = f.openTree(inDir+"/em-NOMINAL_ntuple_WJets_"+era+".root" , "TauCheck"       )
    f5,tree_Diboson = f.openTree(inDir+"/em-NOMINAL_ntuple_Diboson_"+era+".root" , "TauCheck" )
    
    bg_trees= {"dy": tree_DYJets, "singletop": tree_SingleTop, "ttbar": tree_TTbar, "wjets": tree_WJets, "diboson": tree_Diboson}
     

# Create canvas
    c = rt.TCanvas("c", "canvas", 800,800)
    
    for jetbins in jet_selection:
        bins = [0.3,0.9,1.5,2.0,2.4,2.8,3.2,3.6,4.0,4.4,4.8,6.0]  #v1
        nbins =11
        if (jetbins=="njet0") :
            bins = [0.3,1.2,2.0,2.6,3.2,3.8,4.4,5.0,6.0] #v1
            nbins=8
        #making histo for os and ss in isolations and antiiso region
        h_os = rt.TH1F("hist_os","hist_os",nbins,array('d',bins))
        h_ss = rt.TH1F("hist_ss","hist_ss",nbins,array('d',bins))
        h_os_validation = rt.TH1F("hist_os_validation","hist_os_validation",nbins,array('d',bins))
        h_ss_validation = rt.TH1F("hist_ss_validation","hist_ss_validation",nbins,array('d',bins))

        h_os_bg = rt.TH1F("hist_os_bg","hist_os_bg",nbins,array('d',bins))
        h_ss_bg = rt.TH1F("hist_ss_bg","hist_ss_bg",nbins,array('d',bins))
        h_os_bg_validation = rt.TH1F("hist_os_bg_validation","hist_os_bg_validation",nbins,array('d',bins))
        h_ss_bg_validation = rt.TH1F("hist_ss_bg_validation","hist_ss_bg_validation",nbins,array('d',bins))
        h_os_bg_total = rt.TH1F("hist_os_bg_total","hist_os_bg_total",nbins,array('d',bins))
        h_ss_bg_total = rt.TH1F("hist_ss_bg_total","hist_ss_bg_total",nbins,array('d',bins))
        h_os_bg_total_validation = rt.TH1F("hist_os_bg_total_validation","hist_os_bg_total_validation",nbins,array('d',bins))
        h_ss_bg_total_validation = rt.TH1F("hist_ss_bg_total_validation","hist_ss_bg_total_validation",nbins,array('d',bins))

        h_os_bg_total = None
        h_ss_bg_total = None
        h_os_bg_total_validation = None
        h_ss_bg_total_validation = None
        
        tree_Data.Draw("dr_tt>>hist_os",preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_iso + "&&" + selection_os + "&&" + jet_selection[jetbins])
        tree_Data.Draw("dr_tt>>hist_ss",preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_iso + "&&" + selection_ss + "&&" + jet_selection[jetbins])
        tree_Data.Draw("dr_tt>>hist_os_validation",preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_antiiso + "&&" + selection_os + "&&" + jet_selection[jetbins])
        tree_Data.Draw("dr_tt>>hist_ss_validation",preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_antiiso + "&&" + selection_ss + "&&" + jet_selection[jetbins])
        print ("os: data: integral " + str(h_os.Integral()))
        print ("ss: data: integral " + str(h_ss.Integral()))
        
        for bg in bg_trees:
            bg_trees[bg].Draw("dr_tt>>hist_os_bg",weights_common + "*(" + preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_iso + "&&" + selection_os + "&&" + jet_selection[jetbins] + ")")
            bg_trees[bg].Draw("dr_tt>>hist_ss_bg",weights_common + "*(" + preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_iso + "&&" + selection_ss + "&&" + jet_selection[jetbins] + ")")
            bg_trees[bg].Draw("dr_tt>>hist_os_bg_validation",weights_common + "*(" + preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_antiiso + "&&" + selection_os + "&&" + jet_selection[jetbins] + ")")
            bg_trees[bg].Draw("dr_tt>>hist_ss_bg_validation",weights_common + "*(" + preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_antiiso + "&&" + selection_ss + "&&" + jet_selection[jetbins] + ")")
        
            print ("os: background: integral " + bg + " " + str(h_os_bg.Integral()))
            print ("ss: background: integral " + bg + " " + str(h_ss_bg.Integral()))    
        
            if h_os_bg_total is None :
                h_os_bg_total = h_os_bg.Clone()
                h_ss_bg_total = h_ss_bg.Clone()
                h_os_bg_total_validation = h_os_bg_validation.Clone()
                h_ss_bg_total_validation = h_ss_bg_validation.Clone()
            else :
                h_os_bg_total.Add(h_os_bg)
                h_ss_bg_total.Add(h_ss_bg)
                h_os_bg_total_validation.Add(h_os_bg_validation)
                h_ss_bg_total_validation.Add(h_os_bg_validation)
        
       
        print ("BG / OS DATA = " + str(h_os_bg_total.Integral()/h_os.Integral()) + " in category " + str(jetbins))
        print ("BG / SS DATA = " + str(h_ss_bg_total.Integral()/h_ss.Integral()) + " in category " + str(jetbins))

        print ("BG / OS DATA (validation region) = " + str(h_os_bg_total_validation.Integral()/h_os_validation.Integral()) + " in category " + str(jetbins))
        print ("BG / SS DATA (validation region) = " + str(h_ss_bg_total_validation.Integral()/h_ss_validation.Integral()) + " in category " + str(jetbins))
       
        print ("Data before subtraction : " + str(h_os.Integral()))
        print ("BG before subtraction : " + str(h_os_bg_total.Integral()))
        
        #subtract data from MC in ss and os region
        h_os.Add(h_os_bg_total,-1.)
        h_ss.Add(h_ss_bg_total,-1.)
        print ("Data after subtraction : " + str(h_os.Integral()))
        h_os_validation.Add(h_os_bg_total_validation,-1.)
        h_ss_validation.Add(h_ss_bg_total_validation,-1.)
    
        ratio = h_os.Clone()
        ratio.Divide(ratio, h_ss)
        #ratio=h_os.Divide(h_ss)
        #print("ratio_2", ratio )
        
        #fit to polynomial function for dr[0,6] and 3 parameters corresponding to pol2
        def pol2(p,x):
            return sum((a*x**i for i,a in enumerate(p)))
        #rt.TF1("fitFunc","pol2",0,6,3)
        f1=rt.TF1("f1","pol2")#,0,6,3)
    
        #f1=ratio.Fit("pol2")
        f1.SetLineColor(2);
        f1.SetParameter(0,1);
        f1.SetParameter(1,0);
        f1.SetParameter(2,0);
        
        ratio.Fit("f1","Q");
        ratio.GetXaxis().SetTitle("#DeltaR(e,#mu)")
        ratio.SetTitle("")
        ratio.GetYaxis().SetTitle("OS/SS transfer factor")
        ratio.Draw("E")
        
        
        bins = []
        n = xmax/0.05
        for i in range(0,int(n+1)) :
            bins.append(0.05*i)
        grint  =  rt.TGraphErrors(len(bins)-1);
        for k in range(0,len(bins)-1) :
            grint.SetPoint(k, bins[k], 0);
        (rt.TVirtualFitter.GetFitter()).GetConfidenceIntervals(grint,0.68);
        grint.SetLineColor(rt.kBlue);

        grint_Up = rt.TGraphErrors(len(bins)-1);
        grint_Down = rt.TGraphErrors(len(bins)-1);
        for k in range(0,len(bins)-1) :
            x = rt.Double(0)
            value = rt.Double(0)
            grint.GetPoint(k,x,value);
            value_up = value + grint.GetErrorYhigh(k);
            value_down = value - grint.GetErrorYhigh(k);
            grint_Up.SetPoint(k, bins[k], value_up );
            grint_Down.SetPoint(k, bins[k], value_down );

        grint_Up.Draw("same")
        grint_Down.Draw("same")
        
        outFile.cd()
        transfer_function = ratio.GetFunction("pol2");
        transfer_function = ratio.GetFunction("f1");
        transfer_function.SetName("OS_SS_transfer_factors_" + jetbins)
        grint_Up.SetName("OS_SS_transfer_factors_" + jetbins + "_UP")
        grint_Down.SetName("OS_SS_transfer_factors_" + jetbins + "_DOWN")
        grint_Up.Write()
        grint_Down.Write()
        transfer_function.Write()
        c.Print("figures_"+era+"/transfer_factor_drtt_"+ jetbins + ".pdf")
        
       
        # validation factors 
        ratio_validation = h_os_validation.Clone()
        ratio_validation.Divide(ratio_validation, h_ss_validation)
        ratio_validation.Fit("f1")
        ratio_validation.Draw("E")

        grint_validation  =  rt.TGraphErrors(len(bins)-1);
        for k in range(0,len(bins)-1) :
            grint_validation.SetPoint(k, bins[k], 0);
        (rt.TVirtualFitter.GetFitter()).GetConfidenceIntervals(grint_validation,0.68);
        grint_validation.SetLineColor(rt.kBlue);

        grint_validation_Up = rt.TGraphErrors(len(bins)-1);
        grint_validation_Down = rt.TGraphErrors(len(bins)-1);
        for k in range(0,len(bins)-1) :
            x = rt.Double(0)
            value = rt.Double(0)
            grint_validation.GetPoint(k,x,value);
            value_up = value + grint_validation.GetErrorYhigh(k);
            value_down = value - grint_validation.GetErrorYhigh(k);
            grint_validation_Up.SetPoint(k, bins[k], value_up );
            grint_validation_Down.SetPoint(k, bins[k], value_down );

        grint_validation_Up.Draw("same")
        grint_validation_Down.Draw("same")

        outFile.cd()
        transfer_function_validation = ratio_validation.GetFunction("f1");
        transfer_function_validation.SetName("OS_SS_transfer_factors_validation_" + jetbins)
        grint_validation_Up.SetName("OS_SS_transfer_factors_validation_" + jetbins + "_UP")
        grint_validation_Down.SetName("OS_SS_transfer_factors_validation_" + jetbins + "_DOWN")
        grint_validation_Up.Write()
        grint_validation_Down.Write()
        transfer_function_validation.Write()
        c.Print("figures_"+era+"/transfer_factor_drtt_validation_"+ jetbins + ".pdf")

        del h_os
        del h_ss
        del h_os_validation
        del h_ss_validation

        del h_os_bg
        del h_ss_bg
        del h_os_bg_validation
        del h_ss_bg_validation
        del h_os_bg_total
        del h_ss_bg_total
        del h_os_bg_total_validation
        del h_ss_bg_total_validation

def openTree(filename,treename):
    f1 = rt.TFile(filename)
    tree = f1.Get(treename)
    return(f1,tree)
         
        
if __name__ == '__main__':
    main()