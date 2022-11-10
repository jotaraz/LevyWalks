import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

def log_monom(x, a, b):
    return b+x*a

def calc_alpha_single(x0, y0, show, a, b):
    x = x0[a:b]
    y = y0[a:b]
    par, cm = opt.curve_fit(log_monom, np.log(x), np.log(y))
    
    Alpha = par[0]
    dAlpha = np.sqrt(np.diag(cm))[0]
    lab = str(round(Alpha, 3))+' ± '+str(round(dAlpha, 3))
    if(show):
        plt.plot(x, np.exp(log_monom(np.log(x), *par)), label=lab)
        
    return Alpha, par[1], np.sqrt(np.diag(cm))[0], np.sqrt(np.diag(cm))[1]

def read_and_plot(a):
    filename = 'LevyWalkNS_data/te7_a'+str(a)+'_0.txt'
    data = np.loadtxt(filename, skiprows=2)
    time = data[:,0]
    SSD  = data[:,1]
    lines = []
    with open(filename) as f:
        lines = f.readlines()
    j = float(lines[1][2:])
    
    for i in range(0, 30):
        filename = 'LevyWalkNS_data/te7_a'+str(a)+'_'+str(i)+'.txt'
        try:
            data = np.loadtxt(filename, skiprows=2)
            SSD  = SSD + data[:,1]
            lines = []
            with open(filename) as f:
                lines = f.readlines()
            j += float(lines[1][2:])

        except:
            q=1
    
    plt.plot(time, SSD/j, label='a='+str(a)+',j='+str(j))
    calc_alpha_single(time, SSD/j, True, -200, -1)
    calc_alpha_single(time, SSD/j, True, -100, -1)
    #if(a < 1):            
    #    plt.plot(time, time**2, '-', label='t^2')
    #else:            
    #    plt.plot(time, time**(3-a), '-', label='t^'+str(3-a))
        


read_and_plot(0.3)
read_and_plot(0.7)
read_and_plot(1.0)
read_and_plot(1.3)
read_and_plot(1.7)

plt.xscale('log')
plt.yscale('log')

plt.legend()
plt.show()
