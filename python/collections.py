#!/usr/bin/python3
import collections, heapq, operator, itertools

a,*b,c=(1,2,3,4)
#    ->a=1,b=[2,3],c=4

collections.deque([1,2,3,4],2)
#    ->[1,2]

heapq.nlargest(3,[1,2,3,3,4])
#    ->[3,3,4]

heapq.nsmallest(3,[1,2,3,3,4])
#    ->[1,2,3]

c=collections.defaultdict(list)
c['a'].append(1)
c['a'].append(2)
d=collections.defaultdict(set)
d['a'].add(1)
d['b'].add(2)
#    -> c={'a':[1,2]}
#       d={'a':{1},'b':{2}}

# reverse key and value
a={'a':1,'b':2}
sorted(zip(a.keys(),a.values()))
#    ->[(2,'b'),(1,'a')]

b=collections.Counter([1,2,3,3])
b.most_common(1)
#    ->[(3,1)]

rows = [
        {'a':1, 'b':2, 'c':3},
        {'a':1, 'b':2, 'c':4},
        {'a':1, 'b':2, 'c':5},
        {'a':1, 'b':3, 'c':5}
        ]
row_by_c = sorted(rows, key=operator.itemgetter('c'))
#   ->  {'a':1, 'b':2, 'c':5},
#       {'a':1, 'b':3, 'c':5},
#       {'a':1, 'b':2, 'c':4},
#       {'a':1, 'b':2, 'c':3}

group_by_c = itertools.groupby(rows, key=operator.itemgetter('c'))
#   ->  (3,{'a':1, 'b':2, 'c':3}),
#       (4,{'a':1, 'b':2, 'c':4}),
#       (5,{'a':1, 'b':2, 'c':5},
#       {'a':1, 'b':3, 'c':5})

def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False

ivals = list(filter(is_int,[1,2,3,-2,'asd']))
#   ->[1, 2, 3, -2]

list(itertools.compress([1,2,3,0],[True,True,False,True]))
#   ->[1,2,0]

# immutable
d = collections.namedtuple('a',['b','c'])
e = d('11','22')
#   ->e['b']='11'
#     e['c']='22'
e = e._replace(c='33')
