import ROOT as rt

def openTree(filename,treename):
    f1 = rt.TFile(filename)
    tree = f1.Get(treename)
    return (f1,tree)

def createH1(xaxis_name , nbins, xmin, xmax):
    h1 = rt.TH1D("h_"+xaxis_name,"h_"+xaxis_name, nbins , xmin, xmax)
    return h1

def createH2(xaxis_name , nbins, xmin, xmax, nbinsy, ymin, ymax):
    h2 = rt.TH2D("h_"+xaxis_name,"h_"+xaxis_name, nbins , xmin, xmax, nbinsy, ymin, ymax)
    return h2


def createCanvas() :
    c = rt.TCanvas("c", "canvas", 1100, 800)
    return c

    
def hist2Lists(hist) :

    list_x=[]
    list_y=[]
    list_yerr=[]

    for bin in range(1,hist.GetNbinsX()) : 
        list_x.append(hist.GetBinCenter(bin))
        list_y.append(hist.GetBinContent(bin))
        list_yerr.append(hist.GetBinError(bin))

    return list_x , list_y , list_yerr

def InitHist(hist, xaxis_name, color=1) :

    hist.SetFillColor(color);
    hist.SetFillStyle(1001);
    hist.SetLineColor(1);
    hist.SetLineStyle(1);
    hist.SetLineWidth(2);

    hist.SetMarkerColor(1);
    hist.SetMarkerStyle(20);
    hist.SetMarkerSize(1.0);

    hist.GetXaxis().SetLabelFont(43)
    hist.GetYaxis().SetLabelFont(43)
    hist.GetYaxis().SetTitleFont(43)
    hist.GetYaxis().SetTitleFont(43)

    hist.GetXaxis().SetLabelSize(20)
    hist.GetYaxis().SetLabelSize(20)
    hist.GetXaxis().SetTitleSize(20)
    hist.GetYaxis().SetTitleSize(20)

    hist.GetYaxis().SetTitleOffset(1.55)
    hist.GetYaxis().SetTitleOffset(1.55)

    hist.GetXaxis().SetTitle(xaxis_name)

    hist.SetTitle("")

    hist.SetStats(0)

    return hist
