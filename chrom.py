"""
REALLY slow way of counting chromosome configurations.
"""

# TODO zonal poly

alpha = 2 # chromatids per chromosome

def chunkList(l, chunkSize):
    #return zip(*(l[i::chunkSize] for i in range(alpha)))
    # what follows assumes alpha = 2:
    return zip(l[::chunkSize],l[1::chunkSize])

def disjoint2Sets(X):  # equivalent to multicombinations(X, [2]*(len(X)//2))
   def f(X, cur):
      if not X:
         yield cur
         return
      for i in range(1, len(X)):
         for perm in f(X[1:i] + X[i+1:], cur + [(X[0], X[i])]):
            yield perm
   return f(X, [])

def getConfig(s1):
    #s1 = list(sorted(chunkList(s1, alpha))) # maybe use binary search
    #s2 = list(sorted(chunkList(s2, alpha)))
    #print('getConfig({})'.format(s1))

    s1 = list(s1)
    # s1 = list(chunkList(s1, alpha))

    #s2 = list(defaultList)
    s2 = list(defaultList)
    #print(s1,s2)
    #ss = list(chunkList(s1, alpha)),list(chunkList(s2, alpha))
    
    ret = []

    #print('-----------------')
    #print('\n'.join(map(lambda x: str(x[0][0])+' '+str(x[1][0])+'\n'+str(x[0][1])+' '+str(x[1][1]),zip(s1,s2))))
    
    #for i,tup in enumerate(ss[0]):
    for i,tup in enumerate(s1):
        #print('i:',i)
        if tup is None: # already seen
            continue
        end, cur = tup # TODO don't assume alpha = 2

        s1[i] = None

        # find length of orbit
        orbitlen=1
        while cur is not end:                
            #print('cur:',cur,'end:',end)
            #print('orbitlen:',orbitlen)
            s = s2 if (orbitlen&1) else s1
            #s = ss[orbitlen&1]
            
            for i,tup in enumerate(s):
                #print('i:',i,'tup:',tup,'s:',s)
                if tup is None:
                    continue

                t0,t1 = tup
                
                #if cur is tup[0]:
                if cur is t0:
                    cur = t1
                    s[i] = None
                    break
                
                #if cur is tup[1]:
                if cur is t1:
                    cur = t0
                    s[i] = None
                    break
                
            orbitlen += 1

        ret.append(orbitlen)


    #print('\t',tuple(sorted(ret)))
    return tuple(sorted(ret))

def countConfigurations(n):
    global defaultList
    defaultList = list(chunkList(range(n),alpha))
    from itertools import permutations
    from collections import Counter
    ##
    """
    ctr = Counter()
    from numpy.random import permutation as poop
    for i,perm in enumerate(permutations(range(n))):
    #for i,perm in enumerate(tuple(poop(range(n))) for rang in range(100)):
        print(perm)
        #if not i&8191:
        print()
        print(len(ctr),ctr)
        ctr[getConfig(perm)]+=1
    return
    """
    ##
    from multiprocessing import Pool
    pool = Pool()
    #return Counter(map(getConfig,permutations(range(n))))
    return Counter(pool.imap_unordered(getConfig,disjoint2Sets(list(range(n))), chunksize=2048))
    #return Counter(pool.imap_unordered(getConfig,permutations(range(n)), chunksize=2048))

def main():
    from sys import argv

    n = int(argv[1])

    if n&1:
        raise Exception('Cannot operate on odd numbers')

    print(countConfigurations(n))

    return
    """
    for i in range(0,n+2,2):
        print(i)
        c = countConfigurations(i).most_common()
        from math import ceil, log
        minval, maxval = c[-1][1], c[0][1]
        rawForm = '{{: <{}}}'.format(len(str(maxval)))
        nrmForm = '{{: <{}}}'.format(len(str(maxval//minval)))
        for key,val in reversed(c):
            print('\t',rawForm.format(val),nrmForm.format(val//minval),key)
    """
    
if __name__ == '__main__':
    main()
