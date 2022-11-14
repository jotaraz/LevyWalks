import matplotlib.pyplot as plt
import numpy as np
from fbm import FBM
from numba import jit
import sys

inp = sys.argv

number = int(inp[1])
LD = float(inp[2]) #1000#0
#boxsize = 1000#0

boxsize = 1000
Lfree = 40
innerbox = 2*Lfree
Re = 1.0
num_targets = int(boxsize**2 / Lfree**2)
print(num_targets, (boxsize/Lfree)**2)

#targets_x = np.zeros(num_targets)
#targets_y = np.zeros(num_targets)

def generate_lines(a): #Turns a float array into a string array
    L = []
    for i in range(len(a)):
        L.append(str(a[i]) + ' \n')
    return L


def save(times, H, LD):
    filename = 'fBm_data/FAT_H'+str(round(H,3))+'_LD'+str(LD)+'_B'+str(boxsize)+'_'+str(number)+'v3.txt'
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
        

#@jit(nopython=True)
def calc_trajectory(length, H, tx, ty, x_sample, y_sample):
    print('initial pos')
    x0, y0 = initial_pos(tx, ty, innerbox, 1, num_targets)
    x = [x0]#np.zeros(length)
    y = [y0]#np.zeros(length)

    print('start calc')
    j = 1
    found = 0
    t_FA = 2*len(x_sample)
    while(j < len(x_sample) and found == 0):
        print(j, x[j-1], y[j-1])
        
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


@jit(nopython=True)
def create_targets():
    print('create targets')
    targets_x = np.zeros(num_targets) #[np.random.rand() * boxsize]
    targets_y = np.zeros(num_targets) #[np.random.rand() * boxsize]

    for j in range(1, num_targets):
        if(j % 1000 == 0):
            print(j, ' / ', num_targets)
        tx, ty = initial_pos(targets_x, targets_y, boxsize, 2, j)
        targets_x[j] = tx
        targets_y[j] = ty
        
    return targets_x, targets_y

@jit(nopython=True)
def initial_pos(tx, ty, randbox, factor, temp_length):
    x0 = (np.random.rand()-0.5)*randbox + boxsize/2
    y0 = (np.random.rand()-0.5)*randbox + boxsize/2
    tooclose = 0
    for j in range(temp_length):
        if((tx[j]-x0)**2 + (ty[j]-y0)**2 < (factor*Re)**2):
            tooclose = 1
            break
    if(tooclose == 1):
        x0, y0 = initial_pos(tx, ty, randbox, factor, temp_length)
    return x0, y0

def draw_targets(tx, ty, xmax, xmin, ymax, ymin):
    print('draw targets')
    xax = np.linspace(-Re, Re, 20)
    yax = (Re**2-xax**2)**0.5
    for j in range(num_targets):
        if(xmin-Re < tx[j] and tx[j] < xmax+Re and ymin-Re < ty[j] and ty[j] < ymax+Re):
            plt.plot(tx[j]+xax, ty[j]+yax, 'k')
            plt.plot(tx[j]+xax, ty[j]-yax, 'k')
            

        

def calc_first_arrival(length, H, LD):
    print('create fBm')
    f = FBM(n=length, hurst=H, length=1, method='daviesharte')
    xs = LD * 2**0.5 * f.fgn() * length**H
    ys = LD * 2**0.5 * f.fgn() * length**H
    times = []
    start_index = 0
    tx, ty = create_targets()

    minx = boxsize
    maxx = 0 
    miny = boxsize
    maxy = 0
    
    while(start_index < 20):# length ):
        x, y, t_FA = calc_trajectory(length, H, tx, ty, xs[start_index:], ys[start_index:])
        times.append(t_FA)
        start_index += t_FA
        plt.plot(x, y, '.-')        
        plt.plot(x[0], y[0], 'ro')
        minx = min(minx, min(x))
        maxx = max(maxx, max(x))
        miny = min(miny, min(y))
        maxy = max(maxy, max(y))
    
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
    draw_targets(tx, ty, maxx, minx, maxy, miny)
    
    return times


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


print(boxsize**2, '=L^2 ? N lf^2 = ', num_targets, '*', Lfree, '^2 = ', num_targets*Lfree**2)


plt.show()
