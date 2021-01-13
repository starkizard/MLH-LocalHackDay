
import argparse
# Time Complexity O(max(l) - min(l))
def countsort(l):
    mx=float("-inf")
    d={}
    for i in l:
        if i in d:
            d[i]+=1
        else:
            d[i]=1
    sortl=[]
    for i in range(min(l),max(l)+1): 
        if i in d:
            sortl.extend([i]*d[i])
    return sortl

parser=argparse.ArgumentParser()
parser.add_argument('-l','--list', nargs='+', help='<Required> Set flag', required=True)
args=parser.parse_args()
print(countsort(list(map(int,args.list))))
