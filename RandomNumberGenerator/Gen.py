from time import time
# Generates random integer from 0 to limit

def primeGen(n): 
    prime,p = [1 for i in range(n + 1)],2 
    prime[0:2]= [0,0]
    while (p*p < n+1): 
        if (prime[p]): 
            for i in range(p * 2, n + 1, p): 
                prime[i]=0
        p += 1

    l=[ p for p in range(n+1) if prime[p]]
    return l


#generates a random number from 0 to limit
def random(limit):
    primeList = primeGen(int(1e6))
    s=int(str(time()).split('.')[1])
    seed = s%10
    s//=10
    prime=primeList[s%len(primeList)]
    prime2=primeList[100:200][s%100]
    seed = (seed * prime2 + 39)%prime
    return seed%(limit+1)

def test():
    for i in range(20):
        print(random(5))

test()





