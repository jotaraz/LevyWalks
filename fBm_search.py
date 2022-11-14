import matplotlib.pyplot as plt
import numpy as np
from fbm import FBM
from numba import jit
import sys

inp = sys.argv

number = int(inp[1])
boxsize = int(inp[2]) #1000#0
LD = float(inp[3]) #1000#0
#boxsize = 1000#0

#boxsize = 1000#0
Lfree = 40
innerbox = 10*Lfree
Re = 1.0
num_targets = int(boxsize**2 / Lfree*2)

#targets_x = np.zeros(num_targets)
#targets_y = np.zeros(num_targets)

def generate_lines(a): #Turns a float array into a string array
    L = []
    for i in range(len(a)):
        L.append(str(a[i]) + ' \n')
    return L


def save(times, H, LD):
    filename = 'fBm_data/FAT_H'+str(round(H,3))+'_LD'+str(LD)+'_B'+str(boxsize)+'_'+str(number)+'v2.txt'
    j_new = 0
    try:
        data = np.loadtxt(filename, skiprows=1)

        file1 = open(filename, 'a')
        file1.writelines(generate_lines(times))
        file1.close()
    except:
        file1 = open(filename, 'w')
        file1.write('start \n')
        file1.writelines(generate_lines(times))
        file1.close()
        

@jit(nopython=True)
def calc_trajectory(length, H, tx, ty, x_sample, y_sample):
    x0, y0 = initial_pos(tx, ty)
    x = [x0]#np.zeros(length)
    y = [y0]#np.zeros(length)

    #print('start calc')
    j = 1
    found = 0
    t_FA = length
    while(j < length and found == 0):
        #if(j % 20 == 0):
        #    print(j, x[j-1], y[j-1])
        
        x.append(x[j-1]+x_sample[j])
        y.append(y[j-1]+y_sample[j])
        
        if(x[j] > boxsize):
            x[j] = 2*boxsize-x[j]
            print('boundary')
        elif(x[j] < 0):
            x[j] = -x[j]
            print('boundary')
        if(y[j] > boxsize):
            y[j] = 2*boxsize-y[j]
            print('boundary')
        elif(y[j] < 0):
            y[j] = -y[j]
            print('boundary')
    
        for i in range(num_targets):
            if((x[j]-tx[i])**2+(y[j]-ty[i])**2 < Re**2):
                #print('found ', j)
                t_FA = j
                found = 1
                break
        
        
        j += 1
        
    
    return x, y, t_FA
    
def MSD_loop(ss, length, H, LD):
    SSD = np.zeros(length)
    for i in range(ss):
        f = FBM(n=length, hurst=H, length=1, method='daviesharte')
        xs = LD * 2**0.5 * f.fgn() * length**H
        ys = LD * 2**0.5 * f.fgn() * length**H

        
        SSD += calc_trajectory(length, H, [], [], xs, ys)**2
    x = np.linspace(1, length, length)
    plt.plot(x, SSD/ss * length**(2*H), '.-')
    return SS
    
@jit(nopython=True)
def create_targets():
    targets_x = np.random.rand(num_targets) * boxsize
    targets_y = np.random.rand(num_targets) * boxsize
    return targets_x, targets_y

@jit(nopython=True)
def initial_pos(tx, ty):
    #print('initial pos')
    x0 = np.random.rand()*boxsize
    y0 = np.random.rand()*boxsize
    tooclose = 0
    for j in range(num_targets):
        if((tx[j]-x0)**2 + (ty[j]-y0)**2 < Re**2):
            tooclose = 1
            break
    if(tooclose == 1):
        x0, y0 = initial_pos(tx, ty)
    return x0, y0

def draw_targets(tx, ty, xmax, xmin, ymax, ymin):
    xax = np.linspace(-Re, Re, 20)
    yax = (Re**2-xax**2)**0.5
    for j in range(num_targets):
        if(xmin-Re < tx[j] and tx[j] < xmax+Re and ymin-Re < ty[j] and ty[j] < ymax+Re):
            plt.plot(tx[j]+xax, ty[j]+yax, 'k')
            plt.plot(tx[j]+xax, ty[j]-yax, 'k')
            

        

def calc_first_arrival(length, H, LD):
    f = FBM(n=length, hurst=H, length=1, method='daviesharte')
    xs = LD * 2**0.5 * f.fgn() * length**H
    ys = LD * 2**0.5 * f.fgn() * length**H
    tx, ty = create_targets()
    x, y, t_FA = calc_trajectory(length, H, tx, ty, xs, ys)
    
    
    """
    print('start calc')
    t_FA = length
    i = 0
    not_found = 1
    while(i < length and not_found==1):
        if(i % 20 == 0):
            print(i)
        for j in range(num_targets):
            if((x[i]-tx[j])**2+(y[i]-ty[j])**2 < Re**2):
                t_FA = i
                not_found = 0
                break
        i += 1

    print('t_FA = ', t_FA)
    """
    draw_targets(tx, ty, np.max(x), np.min(x), np.max(y), np.min(y))
    plt.plot(x, y, '.-')        
    plt.plot(x[0], y[0], 'ro')
    return t_FA


H = np.linspace(0.5, 0.8, 8)
#H = [
#H = [0.1, 0.2, 0.3, 0.4, 0.5, 0.54285714] #, 0.58571429, 0.62857143, 0.67142857, 0.71428571, 0.75714286, 0.8, 0.85, 0.9, 0.95]
H = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9]
t_FA = np.zeros(len(H))
ss = 200
length = 10000
#LD = 1

calc_first_arrival(10000, 0.5, LD)

"""
dx = 0
while(True):
    for i in range(len(H)):
        times = []
        for j in range(ss):
            if(j%5==0 and j != 0):
                print('H = ', H[i], ', j=', j, ', dx=', dx)
                #dx = 0
                save(times, H[i], LD)
                times = []
            t_temp = calc_first_arrival(length, H[i], LD)
            #dx_max = max(dx, dx_max)
            t_FA[i] += t_temp
            times.append(t_temp)
        print('H = ', H[i], ', j=', j, ', dx=', dx)
        dx = 0
        save(times, H[i], LD)
"""      


#t_FA /= ss
#plt.plot(2*H, 1/t_FA)

            
#calc_first_arrival(10000, 0.5, 1)

"""
x = np.linspace(0.1, 200, 100)

plt.plot(x, 2*x**0.6)
plt.plot(x, 2*x**1.0)
plt.plot(x, 2*x**1.4)

MSD_loop(ss, 400, 0.3)
MSD_loop(ss, 200, 0.5)
MSD_loop(ss, 100, 0.7)
"""

#plt.xscale('log')
#plt.yscale('log')

plt.show()
