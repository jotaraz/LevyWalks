import numpy as np
import matplotlib.pyplot as plt

def read_and_plot(filename):
    data = np.loadtxt(filename, skiprows=2)
    time = data[:,0]
    SSD  = data[:,1]
    lines = []
    with open(filename) as f:
        lines = f.readlines()
    j = float(lines[1][2:])
    a = float(lines[0][2:])

    plt.plot(time, SSD/j)
    if(a < 1):            
        plt.plot(time, time**2, '-', label='t^2')
    else:            
        plt.plot(time, time**(3-a), '-', label='t^'+str(3-a))
    

#read_and_plot('LevyWalkNS_data/te6_a0.5_0.txt')
read_and_plot('LevyWalkNS_data/te6_a0.5.txt')
read_and_plot('LevyWalkNS_data/te6_a1.0.txt')

plt.xscale('log')
plt.yscale('log')

plt.legend()
plt.show()
