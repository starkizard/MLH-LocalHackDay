
def add(element):
    if element+"\n" in lines:
        print("Element already in to-do list")
    else:
        lines.append(element+"\n")
    
def remove(pp):
    pp=int(pp)
    try:
        if(pp<=0): raise
        lines.pop(pp-1)
        print(lines)
    except:
        print("Position not found")
   

def TDprint():
    print("Your list: ")
    for i in range(len(lines)): print(i+1,":\t",lines[i])

def inputerr():
    print("Please enter a valid option")


f=open("data.txt","r")
lines=f.readlines()
f.close()

print("Welcome to your To-do list")
print("Options:")
print("\ta [string]   => adds string to ToDo")
print("\tr [position] => removes string at position from ToDo")
print("\tp            => prints ToDo")
print("\te            => Save and Exit")

print( " Please exit through e otherwise changes won't be made")

l=[]
count=0
while(len(l)==0):
    if count==0: count+=1
    else: inputerr()
    l=input("Enter option :\t").split()

while(l[0].lower()!='e'):
    if(l[0].lower()=='a'):
        try:
            if(len(l)==1): raise
            add(" ".join(l[1:]))
        except:
            inputerr()
    elif(l[0].lower()=='r'):
        try:
            if(len(l)==1): raise
            remove(" ".join(l[1:]))
        except:
            inputerr()
    elif(l[0].lower()=='p'):
        TDprint()
    else:
        inputerr()
    l=[]
    count=0
    while(len(l)==0):
        if count==0: count+=1
        else: inputerr()
        l=input("Enter option :\t").split()

f=open("data.txt","w")
f.writelines(lines)
f.close()
    


    