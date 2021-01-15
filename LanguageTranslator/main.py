from googletrans import Translator, LANGUAGES


def displayLang():
    c=1
    for i in (LANGUAGES.values()):
        print(c,")",i,end="\t",sep="")
        c+=1
        if(c%10==0): print()


def Translate():
    string = input("Enter text : \t")
    a=sorted(LANGUAGES.values())
    try:
        s= a[int(input("Enter source language number or type auto for automatic:\t"))-1]
    except:
        s="auto"
    d= a[int(input("Enter destination language number:\t"))-1]

    translator=Translator()
    output = translator.translate(text=string,dest=d,src=s)
    print("\n",output.text)
    print(" Pronunciation :", output.pronunciation)

def main():
    print("Language Translator")    
    displayLang()
    print("\n \nOPTIONS:")
    print("0 : exit , 1: Translate , 2: Display")
    choice=int(input())
    while(choice):
        if(choice==1):
            Translate()
        else:
            displayLang()
        print("\n \nOPTIONS:")
        print("0 : exit , 1: Translate , 2: Display")
        choice=int(input())

main()        

