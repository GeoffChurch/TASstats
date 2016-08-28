def disjoint2Sets(X): # equivalent to multicombinations(X, [2]*(len(X)//2))
   def f(X, cur):
      if not X:
         yield cur
         return
      for i in range(1, len(X)):
         for perm in f(X[1:i] + X[i+1:], cur + [(X[0], X[i])]):
            yield perm
   return f(X, [])


def multicombinations(X, part_sizes):
   def getTuples(X, part_sizes, cur):
      #print('\tgetTuples',(X, part_sizes, cur))
      if not part_sizes:
         yield cur
         return
      for A, B in combinations(X[1:], part_sizes[0] - 1):
         for parts in getTuples(B, part_sizes[1:], cur+[X[:1] + A]):
            yield parts
            
   return getTuples(X, part_sizes, [])

def combinations(X, k):
   
   def f(X, A, B, k):
      if not k:
         yield A, B+X
      else:
         for i in range(len(X) - k + 1):
            for newA, newB in f(X[i+1:], A+X[i:i+1], B+X[:i], k-1):
               yield newA, newB

   return f(X, [], [], k)
