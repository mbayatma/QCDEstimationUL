import os
import argparse 

parser = argparse.ArgumentParser() 
parser.add_argument('-e', dest='era', help='ERA' ,choices = ['2016_pre','2016_post','2017','2018'], default = '2018')
args = parser.parse_args()

era=args.era



cmd = "mkdir output_"+era
os.system(cmd)
cmd = "mkdir figures_"+era
os.system(cmd)
print( "Deleting old weight file ...")
cmd="rm output_"+era+"/QCDweights.root"
os.system(cmd)
print ("Determining OS/SS transfer factors as function of deltaR(e,mu) in bins of different jet multiplicities ...")
cmd="python QCD_weights.py -e "+era
os.system(cmd)
print "Determining non-closure corrections..."
cmd="python Nonclosurecorrection.py -e "+era
os.system(cmd)


