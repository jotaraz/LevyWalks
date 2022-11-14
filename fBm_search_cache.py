import matplotlib.pyplot as plt
import numpy as np
from fbm import FBM
from numba import jit
import sys

inp = sys.argv

number = int(inp[1])
boxsize = int(inp[2]) #1000#0
ss = int(inp[3])
LD = float(inp[4])
#boxsize = 1000#0

#boxsize = 1000#0
Lfree = 40
innerbox = 5*Lfree
length = 100000
Re = 1.0
num_targets = int(boxsize**2 / Lfree**2)


grid_scale = 10*Lfree
num_cells = int(boxsize / grid_scale)
boxsize = num_cells * grid_scale
num_per_cell = 10*int(num_targets/num_cells**2)
grid_indices = np.zeros((int(boxsize / grid_scale) ** 2, num_per_cell))
grid_indices_len = np.zeros(int(boxsize / grid_scale) ** 2)


def generate_lines(a): #Turns a float array into a string array
    L = []
    for i in range(len(a)):
        L.append(str(a[i]) + ' \n')
    return L

@jit(nopython=True)
def grid(tx, ty): #this function puts all the indices of the obstacles in the (i,j)-th cell in the i*num_cells+j entry of grid_indices
    grid_indices = np.zeros((num_cells ** 2, num_per_cell), dtype=np.int32)
    grid_indices_len = np.zeros(num_cells ** 2, dtype=np.int32) #this array contains the number of obstacles in each cell
    for k in range(num_targets):
        i = int(tx[k] / grid_scale)
        j = int(ty[k] / grid_scale)
        index = num_cells * i + j
        grid_indices[index][int(grid_indices_len[index])] = k
        grid_indices_len[index] += 1
    return grid_indices, grid_indices_len

def save(times, H, LD):
    filename = 'fBm_data/FAT_H'+str(round(H,3))+'_LD'+str(LD)+'_B'+str(boxsize)+'_T'+str(length)+'_'+str(number)+'_v5.txt'
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
def calculate_neighbors(i_x, i_y, cache): #, cache_check):
    #this function calculates this square for (i_x, i_y) if that hasn't been done yet and returns the whole cache
    s = np.sum(cache[i_x][i_y])
    if(s == 0): #the cache array starts filed with zeros, so if all the entries are still 0, their sum is 0 and the square still has to be calculated
        cache[i_x][i_y] = np.array([((i_x - 1) % num_cells) * num_cells + (i_y - 1) % num_cells,
                                    ((i_x - 1) % num_cells) * num_cells + i_y,
                                    ((i_x - 1) % num_cells) * num_cells + (i_y + 1) % num_cells,
                                    ((i_x + 0) % num_cells) * num_cells + (i_y - 1) % num_cells,
                                    ((i_x + 0) % num_cells) * num_cells + i_y,
                                    ((i_x + 0) % num_cells) * num_cells + (i_y + 1) % num_cells,
                                    ((i_x + 1) % num_cells) * num_cells + (i_y - 1) % num_cells,
                                    ((i_x + 1) % num_cells) * num_cells + i_y,
                                    ((i_x + 1) % num_cells) * num_cells + (i_y + 1) % num_cells])
    return cache   


@jit(nopython=True)
def calc_trajectory(length, H, LD, tx, ty, x_sample, y_sample):
    x0, y0 = initial_pos(tx, ty)
    
    (grid_indices, grid_indices_len) = grid(tx, ty)
    cache = np.zeros((num_cells, num_cells, 9))
    
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

        i_x = int(x[j] / grid_scale)
        i_y = int(y[j] / grid_scale)
        cache = calculate_neighbors(i_x, i_y, cache)
        adjacent_indices = cache[i_x][i_y]

        found = 0
        i = 0
        while(found == 0 and i < (len(adjacent_indices))): #every adjacent cell (and the cell itself) is considered
            index = int(adjacent_indices[i])
            for cell_index in range(grid_indices_len[index]): #and all their obstacles
                c_x = tx[grid_indices[index][cell_index]] #position of the obstacle
                c_y = ty[grid_indices[index][cell_index]]
                if((c_x - x[j])**2 + (c_y - y[j])**2 < Re**2): #distance^2 between particle and obstacle
                    t_FA = j
                    found = 1
                    break
            i += 1
        j += 1
        
    x = np.array(x)
    y = np.array(y)

    disp_max = max(np.max(np.abs(x[1:]-x[:-1])), np.max(np.abs(y[1:]-y[:-1])))
    return x, y, disp_max, t_FA
    
def MSD_loop(ss, length, H):
    SSD = np.zeros(length)
    for i in range(ss):
        SSD += calc_trajectory(length, H)**2
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
    x0 = (np.random.rand()-0.5)*innerbox + boxsize/2
    y0 = (np.random.rand()-0.5)*innerbox + boxsize/2
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
    tx, ty = create_targets()
    f = FBM(n=length, hurst=H, length=1, method='daviesharte')
    x_sample = LD * 2**0.5 * f.fgn() * length**H
    y_sample = LD * 2**0.5 * f.fgn() * length**H
    x, y, dx_max, t_FA = calc_trajectory(length, H, LD, tx, ty, x_sample, y_sample)
    
    
    
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

    #draw_targets(tx, ty, np.max(x), np.min(x), np.max(y), np.min(y))
    #plt.plot(x[0], y[0], 'ro')        
    #plt.plot(x, y, '.-')        
    return dx_max, t_FA


H = [0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9]
t_FA = np.zeros(len(H))
#ss = 200
#LD = 1

dx_max = 0

while(True):
    for i in range(len(H)):
        times = []
        for j in range(ss):
            print(j, '/', ss)
            dx, t_temp = calc_first_arrival(length, H[i], LD)
            dx_max = max(dx, dx_max)
            t_FA[i] += t_temp
            times.append(t_temp)
        print('H = ', H[i], ', j=', j, ', dx=', dx_max, ', eta=', 1/np.mean(np.array(times)))
        dx_max = 0
        save(times, H[i], LD)

#t_FA /= ss
#plt.plot(2*H, 1/t_FA)

            
#calc_first_arrival(10000, 0.9, 1)

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
