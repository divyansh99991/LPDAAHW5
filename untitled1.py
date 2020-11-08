# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 21:10:24 2020

@author: mitta
"""


import pulp as p
import time
from datetime import timedelta


x = []
month = [0,1,2,3,4]
m = 3
demand = [0,50,40,70,0]

D = dict(zip(month,demand))
E=5
Hcost=32
Fcost=40
S=200
C=8
OTC=3
OTprice=35
W=6


w = p.LpVariable.dicts('w', month, cat = 'Integer', lowBound = 0)
h = p.LpVariable.dicts('h', month, cat = 'Integer', lowBound = 0)
f = p.LpVariable.dicts('f', month, cat = 'Integer', lowBound = 0)
s = p.LpVariable.dicts('s', month, cat = 'Integer', lowBound = 0)
o = p.LpVariable.dicts('o', month, cat = 'Integer', lowBound = 0)
x = p.LpVariable.dicts('x', month, cat = 'Integer', lowBound = 0)

model = p.LpProblem("Porduction Planning", p.LpMinimize)

model += S*sum(w[t] for t in month[1:m+1]) + Fcost*sum(f[t] for t in month[1:2+m]) + Hcost*sum(h[t] for t in month[1:2+m]) + W*sum(s[t] for t in month[1:m+1])+OTprice*sum(o[t] for t in month[1:m+1])
model += w[0] == E
model += s[0] == 0

model += w[m+1] == E

for t in month[1:m+1]:
    model += x[t] == C*w[t] + o[t]
    
for t in month[1:m+2]:
    model += w[t] == w[t-1] + h[t]-f[t]

for t in month[1:m+1]:
    model += s[t] == s[t-1] + x[t]-demand[t]
    

for t in month[0:m+2]:
    model += o[t] <= OTC
    

start_time = time.monotonic()
model.solve()
end_time = time.monotonic()
#print("Status:",p.LpStatus[model.status])
print("MinCost: ",p.value(model.objective))
print("Duration:",timedelta(seconds=end_time - start_time))