import matplotlib.pyplot as plt
import numpy as np

def ran_arrival(lam):
    u=np.random.uniform(0,1,1000)
    t=-np.log(1-u)/lam
    return t


lam=5.720
bins=20
in_t=ran_arrival(lam)

plt.hist(in_t, bins,edgecolor="black")
plt.xlabel('inter_arrival')  
plt.ylabel('frequency')  
plt.show()
