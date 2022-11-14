import matplotlib.pyplot as plt
import numpy as np
from fbm import FBM

def calc_trajectory(length, H, LD):
    f = FBM(n=length, hurst=H, length=1, method='daviesharte')
    x_sample = LD * 2**0.5 * length**H * f.fgn() 
    #y_sample = f.fgn()
    
    #print(x_sample)
    #print(y_sample)
    #avg_abs = np.sum(np.abs(x_sample))/length
    #avg_abs2 = np.sum(x_sample**2)/length
    
    #print('H=', H, ' avg=', avg_abs)
    
    x = np.cumsum(x_sample)
    #y = np.cumsum(y_sample)
    #return x, y
    return x #_sample[0] # avg_abs, avg_abs2


def loop(ss, length, H, LD):
    avg1 = 0
    avg2 = 0
    SSD = np.zeros(length)
    for i in range(ss):
        SSD += calc_trajectory(length, H, LD)**2

    x = np.linspace(1, length, length)
    plt.plot(x, 2*LD**2 * x**(2*H))
    plt.plot(x, SSD/ss, '.-')

ss = 100
loop(ss, 200, 0.7, 0.4)
loop(ss, 200, 0.3, 8)



plt.xscale('log')
plt.yscale('log')

plt.show()
