import numpy as np
import matplotlib.pyplot as plt

length = 500000
cut = 10
velocity = 1.0

time_sta_exp = -4
time_end_exp = 6
num_xaxis = 1000


log_time_scale = np.power(10, np.linspace(time_sta_exp, time_end_exp, num_xaxis)) 
log_time_scale = log_time_scale[:-1]



def put_on_grid(t_arr, x_arr):
    j = 0
    y_arr = np.zeros(num_xaxis-1)

    kval = 0
    yet = True
    """
    for j in range(1, len(x_arr)):
        for k in range(0, num_xaxis-1):
            if(t_arr[j-1] < log_time_scale[k] and log_time_scale[k] < t_arr[j]):
                y_arr[k] = x_arr[j-1] + (log_time_scale[k]-t_arr[j-1])/(t_arr[j]-t_arr[j-1]) * (x_arr[j]-x_arr[j-1])
                kval = k
    """
    jlast = 0
    for k in range(0, num_xaxis-1):
        for j in range(jlast, len(x_arr)-1):
            #print('k=', k, ', j=', j, ', t_j= ', t_arr[j], ' i_k=', log_time_scale[k])
            if(t_arr[j] < log_time_scale[k]):
                y_arr[k] = x_arr[j] + (log_time_scale[k]-t_arr[j])/(t_arr[j+1]-t_arr[j]) * (x_arr[j+1]-x_arr[j])
            else:
                jlast = j
                break
                
                

    return y_arr

    """
    for i in range(num_xaxis):
        y_arr[i] = x_arr[j] #+ x_arr[j+1])/2
        temp_t = t_arr
        if(log_time_scale[i] > t_arr[j]):
            j += 1
            print(j/len(t_arr), ' : ')
    return y_arr
    """


def generate_mult_levy_walk_noise(length, a):
    x = np.random.rand(length)
    y = np.power(x, -1/a) - 1       #the distribution for the waiting time
    z = []                          #cut off noise
    for yt in y:
        if(yt < cut):
            z.append(yt)
    return y

def generate_single_levy_walk_noise(a):
    x = np.random.rand()
    return np.power(x, -1/a)-1

def generate_traj(time_end, a):
    t = [0]
    x = [0]

    min_dt = 10

    x_short = np.zeros(num_xaxis-1)
    j = 0

    while(t[-1] < time_end):
        deltat = generate_single_levy_walk_noise(a)
        vz = (2*np.random.randint(2) - 1)/2
        deltax = vz*velocity*deltat
        
        t.append(t[-1] + deltat)
        x.append(x[-1] + deltax)

        #do some shit on some last entries
        if(t[-2] > 0):
            k_last = num_xaxis/(time_end_exp-time_sta_exp) * (np.log10(t[-2])-time_sta_exp)
        else:
            k_last = 0
            
        k_now  = num_xaxis/(time_end_exp-time_sta_exp) * (np.log10(t[-1])-time_sta_exp)

        for k in range(int(k_last), int(k_now)+1):
            if(k < num_xaxis-1):
                x_short[k] = x[-2] + (log_time_scale[k]-t[-2])/(t[-1]-t[-2]) * (x[-1]-x[-2])
        

        if(deltat < min_dt):
            min_dt = deltat

    return x_short, min_dt

def save(num_traj, a, x_data):
    filename = 'LevyWalkNS_data/te'+str(time_end_exp)+'_a'+str(a)+'.txt'
    
    

def calc_ensemble(ss, a, time_end):
    
    min_dt = 10
    MSD = np.zeros(num_xaxis-1)
    for j in range(ss):
        if(100*j/ss % 1 == 0):
            print(j/ss)
        xs, deltat = generate_traj(time_end, a)
        #plt.plot(t, x, '.-', label='values')
        #x_proj = put_on_grid(t, x)
        #plt.plot(log_time_scale, xs, 'o', label='short')
    
        if(deltat < min_dt):
            min_dt = deltat

        MSD += xs**2

    MSD /= ss
    plt.plot(log_time_scale, MSD, label='a='+str(a))
    if(a < 1):            
        plt.plot(log_time_scale, log_time_scale**2, '-', label='t^2')
    else:            
        plt.plot(log_time_scale, log_time_scale**(3-a), '-', label='t^'+str(3-a))

#plt.plot(log_time_scale, log_time_scale**2, '-', label='t^2')






#calc_ensemble(100, 0.3, log_time_scale[-1]) #10**time_end_exp)
#calc_ensemble(100, 0.6, log_time_scale[-1]) #10**time_end_exp)
#calc_ensemble(100, 0.9, log_time_scale[-1]) #10**time_end_exp)

calc_ensemble(100, 1.9, log_time_scale[-1]) #10**time_end_exp)


plt.xscale('log')
plt.yscale('log')

plt.legend()
plt.show()
