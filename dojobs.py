import os
import time

filename = 'j5.sh'



#os.system('scp jtaraz@egel.physik.tu-berlin.de:/home/jtaraz/rho0.4_dt5e-07_l7_U500_T100.0_p_0.txt /home/jo/Nextcloud/Documents/Uni/V/Klapp/')

#print(os.system('date'))
#import os
#os.system('ls -l')

def text(name, line):
    #line = str(dt)+' '+str(numit_f)+' '+str(numit_e)+' '+str(U0)+' '+str(i)+' '+str(n)+' '+str(Temp)+' '+str(ρ)+' '+str(Lf)
    s = '''#!/bin/bash --login
# this line tells that this is a bash script.

# The following commands are arguments to PBS:
#PBS -N '''+name+'''
#PBS -S /bin/bash
#PBS -l select=ncpus=1:mem=500mb,walltime=500:00:00
#PBS -j oe
#PBS -r y


# This line specifies the working directory of the submitted job: / dt, num_it_factor, num_it_exponent, U0, num_processes, num_samples, new, Temp, rho, Lf
cd $PBS_O_WORKDIR

# Needed for python code only:
source /home/jtaraz

mpirun -n $NCPUS python fBm_search_cache.py '''+line
    return s

def file(name, line):
    file1 = open(filename, 'w')
    t = text(name, line)
    file1.write(t)
    file1.close()

def do(name, line):
    file(name, line)
    time.sleep(0.25)
    os.system('qsub '+str(filename))



for j in range(15):
    i = j+10
    do('1.0_'+str(i), str(i)+' 10000 10 1.0')
    do('4.0_'+str(i), str(i)+' 10000 10 4.0')


a = 159805
b = 159849


for i in range(a, b):
	os.system('qdel '+str(i)+'.jules')
