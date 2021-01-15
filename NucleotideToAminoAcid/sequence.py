tableA={"GG":"Arg","GA":"Arg","GC":"Ser","GU":"Ser","AG":"Lys","AA":"Lys","AC":"Asn","AU":"Asn","CA":"Thr","CG":"Thr","CC":"Thr","CU":"Thr","UG":"Met","UA":"Ile","UC":"Ile","UU":"Ile"}
tableC={"GG":"Arg","GA":"Arg","GC":"Arg","GU":"Arg","AG":"Gln","AA":"Gln","AC":"His","AU":"His","CA":"Pro","CG":"Pro","CC":"Pro","CU":"Pro","UG":"Leu","UA":"Leu","UC":"Leu","UU":"Leu"}
tableU={"GG":"Trp","GA":"STOP","GC":"Cys","GU":"Cys","AG":"STOP","AA":"STOP","AC":"Tyr","AU":"Tyr","CA":"Ser","CG":"Ser","CC":"Ser","CU":"Ser","UG":"Leu","UA":"Leu","UC":"Phe","UU":"Phe"}
tableG={"GG":"Gly","GA":"Gly","GC":"GLy","GU":"Gly","AG":"Glu","AA":"GLu","AC":"Asp","AU":"Asp","CA":"Ala","CG":"Ala","CC":"ALa","CU":"Ala","UG":"Val","UA":"Val","UC":"Val","UU":"Val"}

amino=""

print("Welcome to the nucleotide sequence to amino acid sequence converter","This evaluates ACTGU and ignores rest characters","Do you Want an input file? y/N:",sep="\n")
choice=input()

if choice.lower()=='y':
    printf("Enter the name of file, make sure it's in the directory you are executing this code")
    nm=input()
    try:
        f=open(nm,'r+')
        sequence=f.read()
        f.close()
    except:
        print("Error opening file please input")
        sequence=input()    
else:
    sequence=input("Enter the nucleotide sequence :\t")

sequence=sequence.upper()
sequence=sequence.replace("T","U")
seq=""
for i in sequence: #ignoring rest characters
    if i=="A" or i=="G" or i=="C" or i=="U":
        seq+=i
seq=seq[:len(seq)-(len(seq)%3)]    #ignoring waste nucleotides at the end.    
i=0
while(i<len(seq)):
    if seq[i]=="A":
        amino+=tableA[seq[i+1]+seq[i+2]]
    elif seq[i]=="C":
        amino+=tableC[seq[i+1]+seq[i+2]]    
    elif seq[i]=="U":
        amino+=tableU[seq[i+1]+seq[i+2]]
    else:
        amino+=tableG[seq[i+1]+seq[i+2]]
    i+=3

print("The amino acid sequence:")
print(amino)               