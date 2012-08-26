# wordnum.py: A solution to the ITA word numbers puzzle.
# Problem: "If the integers from 1 to 999,999,999 are written as 
#  words, sorted alphabetically, and concatenated, what is the 51
#  billionth letter?" 
#  <http://www.itasoftware.com/careers/puzzle_archive.html>
# Solution: The first key insight is to recognize only 1 .. 999 are 
#  causing the sorting difficulty. The second is to recognize
#  that within a place, the numbers repeat consistently such that
#  you can derive the starting and ending indices within a place.
#  With those two insights binary search can be extended with 
#  additional tracking information to find the solution.
# Copyright (c) 2011 Corey Abshire.

import sys, copy

def wordnumgen():
    '''Make a list of the numbers one to ninehundredninetynine.'''
    ones = ',one,two,three,four,five,six,seven,eight,nine'.split(',')
    teen = 'ten,eleven,twelve'.split(',')
    teen += [w + 'teen' for w in 'thir,four,fif,six,seven,eigh,nine'.split(',')]
    tens = ',,twenty,thirty,forty,fifty,sixty,seventy,eighty,ninety'.split(',')
    hund = [''] + [o + 'hundred' for o in ones[1:]]
    wnum = lambda h,t,o: hund[h] + tens[t] + (t == 1 and teen[o] or ones[o])
    return [wnum(h,t,o) for h in range(10) for t in range(10) for o in range(10)]
WN = wordnumgen()

class Num():
    '''A wordnum w matching value v at multipler m in place p and containing place c.'''
    def __init__(self, w, v, m, p):
        self.w = w; self.v = v; self.m = m; self.k = len(w); self.p = p
    def key(self, o, wk):
        return o + (wk * self.tc) + self.tk
    def sum(self, s, v):
        return s + (v * self.tc) + self.ts

class Place():
    '''A numeric place based on word w at multipler m, containing place p.'''
    def __init__(self, w, m, p):
        self.w = w
        self.p = p
        self.c = p and [copy.copy(n) for n in p.c] or []
        self.c = self.c + [Num(WN[i]+w,i*m,m,self) for i in xrange(1,1000)]
        self.k = p and sum(n.k * n.m + n.p.k for n in p.c) or 0
        self.s = p and sum(n.v * n.m + n.p.s for n in p.c) or 0
        self.c.sort(key=lambda n: n.w)
        tc = 0
        tk = 0
        ts = 0
        for n in self.c:
            tc += n.m
            tk += (n.k * n.m) + n.p.k
            ts += (n.v * n.m) + n.p.s
            n.tk = tk
            n.ts = ts
            n.tc = tc

def bisect(c, target, o, k, lo, hi):
    i = (hi + lo) / 2
    print lo, hi, i
    if hi <= lo:
        print target, c[i].key(o,k), c[i].w, i, lo, hi
        return i
    n = c[i]
    v = n.key(o,k)
    print target, v, n.w, i, lo, hi
    if target > v:
        print 'right'
        return bisect(c, target, o, k, i + 1, hi)
    else:
        print 'left'
        return bisect(c, target, o, k, lo, i - 1)

def search(p, target, w='', k=0, v=0, o=0, s=0):
    '''Find target word number and sum to that point in place p.'''
    pos = bisect(p.c, target, o, k, 0, len(p.c))
    print pos
    if pos > 0:
        o = p.c[pos].key(o, k)
        s = p.c[pos].sum(s, v)
    print len(p.c)
    n = p.c[pos]; 
    print n.w
    w += n.w; k += n.k; v += n.v; o += k; s += v
    if n.p.p and o < target:
        return search(n.p.p, target, w, k, v, o, s)
    else:
        return w, s

def maketree(places=',thousand,million'.split(',')):
    '''Make a tree of places, returning the top place.'''
    place = None
    for i in xrange(len(places)):
        place = Place(places[i], pow(1000, i), place)
    return place

if __name__ == '__main__':
    print '%s\n%s' % search(maketree(), int(sys.argv[1]))
