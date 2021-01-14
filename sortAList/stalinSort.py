
import argparse
# Time Complexity O(max(l) - min(l))
def stalinSort(l):
    m=float("-inf")
    sortl=[]
    for i in l:
        if(i>=m): 
            sortl.append(i)
            m=i
    return sortl

parser=argparse.ArgumentParser()
parser.add_argument('-l','--list', nargs='+', help='<Required> Set flag', required=True)
args=parser.parse_args()
print(stalinSort(list(map(int,args.list))))

