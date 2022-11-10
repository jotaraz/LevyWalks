import matplotlib.pyplot as plt
import numpy as np
from fbm import FBM

def calc_trajectory(length, H):
    f = FBM(n=length, hurst=H, length=1, method='daviesharte')
    x_sample = f.fgn()
    #y_sample = f.fgn()
    
    #print(x_sample)
    #print(y_sample)
    #avg_abs = np.sum(np.abs(x_sample))/length
    #avg_abs2 = np.sum(x_sample**2)/length
    
    #print('H=', H, ' avg=', avg_abs)
    
    
    
    
    #x = np.cumsum(x_sample)
    #y = np.cumsum(y_sample)
    #return x, y
    return x_sample[0] # avg_abs, avg_abs2


def loop(ss, length, H):
    avg1 = 0
    avg2 = 0
    for i in range(ss):
        c = calc_trajectory(length, H)
        avg1 += np.abs(c)
        avg2 += c**2
        
    return avg1/ss, avg2/ss


length = 1000
a = []
a2 = []
b = []
b2 = [] #[0.7315431275341852*2**0.5]
H = np.linspace(0.01, 0.99, 20)
for i in range(len(H)):
    v, v2 = loop(length, 100, H[i]) #calc_trajectory(length, H[i])
    a.append(v)
    a2.append(v2)
    #b.append((1/2)**(H[i]*20))
    #b2.append((1/2**0.5)**(H[i]*20))
    #b2.append(b2[-1]/2**0.5)
             
plt.plot(H, a)
plt.plot(H, a2)
#plt.plot(H, b)
#plt.plot(H, 0.75/0.93*np.array(b2))

#plt.xscale('log')
#plt.yscale('log')

plt.show()
