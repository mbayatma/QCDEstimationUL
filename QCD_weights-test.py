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
    weights_processes = dict(config.items('WEIGHTS_PER_PROCESS'))

    nbins = int(config.get('OUTPUT','nbins'))
    xmin = float(config.get('OUTPUT','xmin'))
    xmax = float(config.get('OUTPUT','xmax'))

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
     f0,tree_Data =f.openTree(inDir+"/em-NOMINAL_ntuple_MuonEG_2018.root","TauCheck")
     f1,tree_TTbar = f.openTree(inDir+"/em-NOMINAL_ntuple_TTbar_2018.root", "TauCheck") 
    f2,tree_DYJets =f.openTree(inDir+"/em-NOMINAL_ntuple_DYJets_2018.root", "TauCheck")
     f3,tree_SingleTop = f.openTree(inDir+"/em-NOMINAL_ntuple_SingleTop_2018.root", "TauCheck" )          
    f4,tree_WJets = f.openTree(inDir+"/em-NOMINAL_ntuple_WJets_2018.root" , "TauCheck"       )
    f5,tree_Diboson = f.openTree(inDir+"/em-NOMINAL_ntuple_Diboson_2018.root" , "TauCheck" )
    bkg_trees= {"dy": tree_DYJets, "singletop": tree_SingleTop, "ttbar": tree_TTbar, "wjets": tree_WJets, "diboson": tree_Diboson}
     

# Create canvas
   c = rt.TCanvas("c", "canvas", 800,800)
    for jetbin in jet_selection:
        bins =[11, 0.3,6.0]
        nbins=11 
    
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
        
        tree_Data.Draw("dr_tt>>hist_os",preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_iso + "&&" + selection_os + "&&" + jet_selection[jetbin])
        tree_Data.Draw("dr_tt>>hist_ss",preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_iso + "&&" + selection_ss + "&&" + jet_selection[jetbin])
        tree_Data.Draw("dr_tt>>hist_os_validation",preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_antiiso + "&&" + selection_os + "&&" + jet_selection[jetbin])
        tree_Data.Draw("dr_tt>>hist_ss_validation",preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_antiiso + "&&" + selection_ss + "&&" + jet_selection[jetbin])
        print ("os: data: integral " + str(h_os.Integral()))
        print ("ss: data: integral " + str(h_ss.Integral()))
        
    for bg in bkg_trees:
        bkg_trees[bg].Draw("dr_tt>>hist_os_bg",weights_common + "(" + preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_iso + "&&" + selection_os + "&&" + jet_selection[jetbin] + ")")
        bkg_trees[bg].Draw("dr_tt>>hist_ss_bg",weights_common + "(" + preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_iso + "&&" + selection_ss + "&&" + jet_selection[jetbin] + ")")
        bkg_trees[bg].Draw("dr_tt>>hist_os_bg_validation",weights_common + "(" + preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_antiiso + "&&" + selection_os + "&&" + jet_selection[jetbin] + ")")
        bkg_trees[bg].Draw("dr_tt>>hist_ss_bg_validation",weights_common + "(" + preselection + "&&" + selection_muon_antiiso + "&&" + selection_electron_antiiso + "&&" + selection_ss + "&&" + jet_selection[jetbin] + ")")
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
        
        print ("----------------------------------------------------------------------------------------")       
        print ("BG / OS DATA = " + str(h_os_bg_total.Integral()/h_os.Integral()) + " in category " + str(jetbin))
        print ("BG / SS DATA = " + str(h_ss_bg_total.Integral()/h_ss.Integral()) + " in category " + str(jetbin))

        print ("BG / OS DATA (validation region) = " + str(h_os_bg_total_validation.Integral()/h_os_validation.Integral()) + " in category " + str(jetbin))
        print ("BG / SS DATA (validation region) = " + str(h_ss_bg_total_validation.Integral()/h_ss_validation.Integral()) + " in category " + str(jetbin))
        print ("----------------------------------------------------------------------------------------" )
        
        print ("Data before subtraction : " + str(h_os.Integral()))
        print ("BG before subtraction : " + str(h_os_bg_total.Integral()))
        h_os.Add(h_os_bg_total,-1.)
        h_ss.Add(h_ss_bg_total,-1.)
        print ("Data after subtraction : " + str(h_os.Integral()))
        h_os_validation.Add(h_os_bg_total_validation,-1.)
        h_ss_validation.Add(h_ss_bg_total_validation,-1.)
    
    

if __name__ == '__main__':
    main()