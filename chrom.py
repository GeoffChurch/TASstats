RAYS = 2 # chromatids per chromosome

def chunkList(l, chunkSize):
    return zip(*(l[i::chunkSize] for i in range(RAYS)))

def getConfigAssume(s1):
    return getConfig(s1,range(len(s1)))

def getConfig(s1, s2):
    #s1 = list(sorted(chunkList(s1, RAYS))) # maybe use binary search
    #s2 = list(sorted(chunkList(s2, RAYS)))

    s1 = list(chunkList(s1, RAYS))
    s2 = list(chunkList(s2, RAYS))
    
    ret = []

    #print('-----------------')
    #print('\n'.join(map(lambda x: str(x[0][0])+' '+str(x[1][0])+'\n'+str(x[0][1])+' '+str(x[1][1]),zip(s1,s2))))
    
    for i,tup in enumerate(s1):

        if tup == None: # already seen
            continue

        # find length of orbit
        end, cur = tup # TODO don't assume SPOKES = 2
        
        orbitlen=1
        while cur != end:
            s = s2 if (orbitlen&1) else s1
            
            for i,x in enumerate(s):

                if x is None or x is tup:
                    continue
                
                if cur == x[0]: # TODO use 'is'?
                    cur = x[1]
                    s[i] = None
                    break
                
                elif cur == x[1]:
                    cur = x[0]
                    s[i] = None
                    break
                
            orbitlen += 1
        ret.append(orbitlen)


    #print('\t',tuple(sorted(ret)))
    return tuple(sorted(ret))

def countConfigurations(n):
    from multiprocessing import Pool
    pool = Pool()
    from itertools import permutations
    from collections import Counter
    return Counter(pool.map(getConfigAssume,permutations(range(n))))

def main():
    from sys import argv

    print(countConfigurations(int(argv[1])))
    
if __name__ == '__main__':
    main()
