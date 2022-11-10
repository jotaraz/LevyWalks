import numpy as np
import matplotlib.pyplot as plt

length = 500000
cut = 10

def generate_levy(length, a):
    x = np.random.rand(length)
    y = np.power(x, -1/a) - 1       #the distribution for the waiting time
    z = []                          #cut off noise
    for yt in y:
        if(yt < cut):
            z.append(yt)

    return z


def create_hist(length, a):
    y = generate_levy(length, a)
    xmax = max(y)
    H = np.histogram(y, bins=100*int(xmax), density=True)   
    HY = H[0]
    HX = (H[1][1:]+H[1][:-1])/2

    plt.plot(HX, HY, label='hist a='+str(a))                #plots the histogram
    Y = np.linspace(np.min(HX), xmax, int(100*xmax))        #x-axis for the analytical density
    density = a/(1+Y)**(a+1)                                #if we didnt cut off the noise, this would be the observed density. it is the density / pdf given by PhysRevE.100.012117
    norm = HY[0] / density[0]                               #due to the cut, the norm is not 0
    plt.plot(Y, norm * density, label='1/(1+y)^1+'+str(a))


create_hist(length, 0.3)
create_hist(length, 1.0)
create_hist(length, 1.8)

plt.xscale('log')
plt.yscale('log')

plt.legend()
plt.show()
