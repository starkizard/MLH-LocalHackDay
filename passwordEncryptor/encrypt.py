import argparse
import hashlib

parser=argparse.ArgumentParser()

def algos():
    return sorted([ x for x in hashlib.algorithms_guaranteed])

def enc(password):
    print("\tEncypting...")

    s=password[:]+"Demoknight tf2" #adding salt
    for i in algos():
        if(i.startswith("shake_")): continue
        print("\t",i,":")
        result = getattr(hashlib,i)(s.encode())
        print("\t",result.hexdigest(),"\n")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-p","--password",help = "<Required> ", required=True)
    args=parser.parse_args()
    enc(args.password)

main()
    
