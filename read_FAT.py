import numpy as np
import matplotlib.pyplot as plt

def name(i, H, LD, ni):
    if(ni == 0):
        return 'fBm_data/FAT_H'+str(H)+'_LD'+str(LD)+'_B10000_T100000_'+str(i)+'_v5.txt'
    else:
        return 'fBm_data/FAT_H'+str(H)+'_LD'+str(LD)+'_B10000_T100000_'+str(i)+'_v6.txt'
    

def read_and_plot(H, LD, nameindex):
    filename = name(10, H, LD, nameindex)
    data = np.loadtxt(filename, skiprows=1)
    times = data
    lines = []
    with open(filename) as f:
        lines = f.readlines()
    
    for i in range(11, 25):
        filename = name(i, H, LD, nameindex)
        try:
            data = np.loadtxt(filename, skiprows=1)
            times = np.concatenate((times, data))

        except:
            q=1

    print(H, ', j=', len(times))
    #plt.plot([2*H], [1/np.mean(times)], 'o')
    return 1/np.mean(times)    

#H = [0.1, 0.2, 0.3, 0.5, 0.543, 0.586, 0.629, 0.671, 0.714, 0.757, 0.8, 0.85, 0.9, 0.95]
H = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9])
LD = [1.0, 4.0]

for l in LD:
    
    efficiency = []
    for h in H:
        efficiency.append(read_and_plot(h, l, 0))
    plt.plot(2*H, np.array(efficiency)/max(efficiency), '.-', label='LD='+str(l)+' v5')
    
    efficiency = []
    for h in H:
        efficiency.append(read_and_plot(h, l, 1))
    plt.plot(2*H, np.array(efficiency)/max(efficiency), '.-', label='LD='+str(l)+' v6')


plt.legend()
plt.show()
