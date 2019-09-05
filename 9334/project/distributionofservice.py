import matplotlib.pyplot as plt
import numpy as np

def ran_service(a1,a2,b):
    u=np.random.uniform(0,1,1000)
    b_=1-b
    r=b_/(a2**b_-a1**b_)
    s_t=((b_/r)*(u+((r/b_)*a1**b_)))**(1/b_)
    return s_t


a1=0.050
a2=0.300
b=0.740
bins=20
in_t=ran_service(a1,a2,b)

plt.hist(in_t, bins,edgecolor="black")
plt.xlabel('service')  
plt.ylabel('frequency')  
plt.show()
