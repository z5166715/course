import matplotlib.pyplot as plt
import numpy as np

def ran_network(v1,v2):
    n=np.random.uniform(v1,v2,1000)
    return n

v1=1.2
v2=1.47
bins=20
in_t=ran_network(v1,v2)

plt.hist(in_t, bins,edgecolor="black")
plt.xlabel('network_l')  
plt.ylabel('frequency')  
plt.show()
