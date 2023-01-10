import ROOT as rt
import argparse
import ConfigParser
import json
from array import array
from ROOT import TF1
import argparse

def main() :

    rt.gStyle.SetPaintTextFormat("4.2f")
    rt.gStyle.SetOptStat(0);
    rt.gROOT.SetBatch(rt.kTRUE)
    rt.gStyle.SetPadTopMargin(0.05);
    rt.gStyle.SetPadBottomMargin(0.16);
    rt.gStyle.SetPadLeftMargin(0.14);
    rt.gStyle.SetPadRightMargin(0.18);
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', dest='era', help='ERA' ,choices = ['2016_pre','2016_post','2017','2018'], default = '2018')
    args = parser.parse_args()

    era=args.era
    
    config = ConfigParser.ConfigParser()
    config.read('settings_for_QCD.cfg')
    if (era=="2018"): 
         inDir=config.get('INPUT','input_directory_2018')
    elif (era=="2017"):
        inDir = config.get('INPUT','input_directory_2017')
    elif  (era=="2016_pre"):
        inDir = config.get('INPUT','input_directory_2016_pre')
    elif (era=="2016_post"):
        inDir = config.get('INPUT', 'input_directory_2016_post')

    
    jet_selection = dict(config.items('JET_BINS'))
    # read in trees ----------------------------------------------------------------------------------------------------------------
    f_Data,t_Data = qcdweights.openTree(inDir+"em-NOMINAL_ntuple_MuonEG_"+era+".root","TauCheck")
    f_DY,t_DY = qcdweights.openTree(inDir+"em-NOMINAL_ntuple_DYJets_"+era+".root","TauCheck")
    f_SingleTop,t_SingleTop = qcdweights.openTree(inDir+"em-NOMINAL_ntuple_SingleTop_"+era+".root","TauCheck")
    f_TTbar,t_TTbar = qcdweights.openTree(inDir+"em-NOMINAL_ntuple_TTbar_"+era+".root","TauCheck")
    f_WJets,t_WJets = qcdweights.openTree(inDir+"em-NOMINAL_ntuple_WJets_"+era+".root","TauCheck")
    f_Diboson,t_Diboson = qcdweights.openTree(inDir+"em-NOMINAL_ntuple_Diboson_"+era+".root","TauCheck")
    trees = {"data" : t_Data, "dy" : t_DY, "singletop": t_SingleTop, "ttbar" : t_TTbar, "wjets": t_WJets, "diboson": t_Diboson}

    # read in fitted functions for weights in bins of njet and deltaR --------------------------------------------------------------
    if (era=="2018"): 
        f_weights = rt.TFile(config.get('OUTPUT','outFile_2018'), "UPDATE")
    elif (era=="2017"):
        f_weights = rt.TFile(config.get('OUTPUT','outFile_2017'), "UPDATE")
    elif (era=="2016_pre"):
        f_weights = rt.TFile(config.get('OUTPUT','outFile_2016_pre'), "UPDATE")    
    elif (era=="2016_post"):
        f_weights = rt.TFile(config.get('OUTPUT','outFile_2016_post'), "UPDATE")    
    f_weights.cd()

    transfer_functions ={}
    transfer_functions_validation ={}
    for jet_category in jet_selection :
        transfer_functions.update({jet_category: f_weights.Get("OS_SS_transfer_factors_"+str(jet_category))})
        transfer_functions_validation.update({jet_category: f_weights.Get("OS_SS_transfer_factors_validation_"+str(jet_category))})

    # define histograms for non-closure weights ------------------------------------------------------------------------------------
    binsx = json.loads(config.get('OUTPUT','binsx'))
    binsy = json.loads(config.get('OUTPUT','binsy'))
    h_OS = rt.TH2F("OS","OS",len(binsx)-1,array('d',binsx),len(binsx)-1,array('d',binsy))
    h_SS = rt.TH2F("SS","SS",len(binsx)-1,array('d',binsx),len(binsx)-1,array('d',binsy))

    h_OS_bg = rt.TH2F("OS_bg","OS_bg",len(binsx)-1,array('d',binsx),len(binsx)-1,array('d',binsy))
    h_SS_bg = rt.TH2F("SS_bg","SS_bg",len(binsx)-1,array('d',binsx),len(binsx)-1,array('d',binsy))

    h_OS_validation = rt.TH2F("OS_validation","OS_validation",len(binsx)-1,array('d',binsx),len(binsx)-1,array('d',binsy))
    h_SS_validation = rt.TH2F("SS_validation","SS_validation",len(binsx)-1,array('d',binsx),len(binsx)-1,array('d',binsy))

    h_OS_bg_validation = rt.TH2F("OS_bg_validation","OS_bg_validation",len(binsx)-1,array('d',binsx),len(binsx)-1,array('d',binsy))
    h_SS_bg_validation = rt.TH2F("SS_bg_validation","SS_bg_validation",len(binsx)-1,array('d',binsx),len(binsx)-1,array('d',binsy))

    c = rt.TCanvas("c","c",800,800)
    #---------------------------------------------------------------------------------------------------------------------------------
    for process in trees :
        for event in trees[process] :
            iso_1 = getattr(event, "iso_1")
            iso_2 = getattr(event, "iso_2")
            pt_1 = getattr(event, "pt_1")
            pt_2 = getattr(event, "pt_2")
            os = getattr(event, "os")
            njets = getattr(event, "njets")
            dr_tt = getattr(event, "dr_tt")
            xsec_lumi_weight = getattr(event, "xsec_lumi_weight")
            nbtag = getattr(event, "nbtag")
            prefiring_weight = getattr(event, "prefiringweight")
            if process == "data" :
                weight = 1.0
            else :
                weight = config.get('COMMON_WEIGHTS', 'weights_common')
            if pt_1 < float(config.get('SELECTION','pt_ele_cut')) :
                continue
            if pt_2 < float(config.get('SELECTION','pt_muon_cut')) :
                continue
            if rt.TMath.Max(pt_1,pt_2) < float(config.get('SELECTION','maxpt_cut')) :
                continue
            if nbtag!=0 :
                continue
            # fill histograms for weights for signal region -----------------------------------------------------------------------
            if iso_1 < float(config.get('SELECTION','iso_1')) :
                if (iso_2 < float(config.get('SELECTION','iso_2')) ) or (float(iso_2 > config.get('SELECTION','iso_max'))) :
                    continue
                if njets==0 :
                    qcdweight = transfer_functions["njet0"].Eval(dr_tt)
                elif njets ==1 :
                    qcdweight = transfer_functions["njet1"].Eval(dr_tt)
                else :
                    qcdweight = transfer_functions["njetgt2"].Eval(dr_tt)
                if os > 0.5 :
                    if process == "data" :
                        h_OS.Fill(pt_2,pt_1,weight)
                    else :
                        h_OS_bg.Fill(pt_2,pt_1,weight)
                else :
                    if process == "data" :
                        h_SS.Fill(pt_2,pt_1,weight*qcdweight)
                    else :
                        h_SS_bg.Fill(pt_2,pt_1,weight*qcdweight)
            # fill histograms for weights for validation region -----------------------------------------------------------------------
            if (iso_1 > float(config.get('SELECTION','iso_1')) and iso_1 < float(config.get('SELECTION','iso_max'))) :
                if (iso_2 < float(config.get('SELECTION','iso_2'))) or (iso_2 > float(config.get('SELECTION','iso_max'))) :
                    continue
                if njets==0 :
                    qcdweight = transfer_functions_validation["njet0"].Eval(dr_tt)
                elif njets ==1 :
                    qcdweight = transfer_functions_validation["njet1"].Eval(dr_tt)
                else :
                    qcdweight = transfer_functions_validation["njetgt2"].Eval(dr_tt)
                if os > 0.5 :
                    if process == "data" :
                        h_OS_validation.Fill(pt_2,pt_1,weight)
                    else :
                        h_OS_bg_validation.Fill(pt_2,pt_1,weight)
                else :
                    if process == "data" :
                        h_SS_validation.Fill(pt_2,pt_1,weight*qcdweight)
                    else :
                        h_SS_bg_validation.Fill(pt_2,pt_1,weight*qcdweight)

    # determine non-closure correction ---------------------------------------------------------------------------------------------------
    h_OS.Add(h_OS_bg,-1.)
    h_SS.Add(h_SS_bg,-1.)
    h_OS_validation.Add(h_OS_bg_validation,-1.)
    h_SS_validation.Add(h_SS_bg_validation,-1.)

    ratio = h_OS.Clone()
    ratio.Divide(ratio, h_SS)
    ratio.GetXaxis().SetTitle("p_{T} muon [GeV]")
    ratio.GetYaxis().SetTitle("p_{T} electron [GeV]")
    ratio.GetXaxis().SetTitleOffset(1.2)
    ratio.GetZaxis().SetTitleOffset(1.2)
    ratio.GetZaxis().SetRangeUser(0,1.4)
    ratio.SetTitle("")
    ratio.GetZaxis().SetTitle("OS/SS transfer factor")
    ratio.Draw("textcolz")
    c.Update()
    c.Print("figures_"+era+"/non_closure_correction_pt.pdf")
    ratio.Draw("textcolz e")
   
    f_weights.cd()
    ratio.SetName("NonClosureCorrection")
    ratio.Write()

    ratio_validation = h_OS_validation.Clone()
    ratio_validation.Divide(ratio_validation, h_SS_validation)
    ratio_validation.Draw("textcolz")
    c.Update()
    c.Print("figures_"+era+"/non_closure_correction_pt_validation.pdf")

    f_weights.cd()
    ratio_validation.SetName("NonClosureCorrectionValidation")
    ratio_validation.Write()


if __name__ == '__main__' :
   main()