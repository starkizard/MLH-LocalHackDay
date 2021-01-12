# Custom Random Number Generator

## How it works:

-> Precalculation: Primes upto 1e6 are generated

-> STEP 1 : founds out the current time through time.time()
-> STEP 2 : Extracts the digits after the floating point and converts them into a new integer
-> STEP 3 : seed is selected as the last digit of the found number
-> STEP 4 : two primes are randomly selected using ( seed % the length of prime list ). one big prime [from range 100th prime to 199th prime] , and one totally random prime uptil the full range that was generated
-> STEP 5: Multiplying the seed with the ranged random prime and adding 39. ( Because why not ) and then modding the whole result by the totally random prime generated
-> STEP 6: THe result is modded with (limit+1) to give a random integer between 0 and limit. both inclusive.