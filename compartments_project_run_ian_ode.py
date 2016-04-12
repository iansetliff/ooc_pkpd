# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 18:16:02 2016

@author: Ian
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 18:05:12 2016

@author: Ian
"""

import compartments_project as na
# from glucosis_metabolism import model
from pysb.integrate import odesolve
import numpy
import matplotlib.pyplot as plt

from pysb import *
from pysb.util import *
from pysb.macros import *
from pysb.bng import *
from pysb.tools import *
from pysb.bng import run_ssa
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from time import time

na.model.monomers
na.model.parameters
na.model.observables
na.model.initial_conditions
na.model.rules
tspan=2000

t0=time()
y = odesolve(na.model, tspan)
t1=time()
print('ODE Solve: %.2g sec' % (t1-t0))

# Use a nice grid to plot 5 figures
gs = gridspec.GridSpec(5,1,width_ratios=[1],height_ratios=[1,1,1,1,1])

ax1 = plt.subplot(gs[0])
plt.plot(tspan, y['Glu_brain'], label='glu_brain', color='r')
plt.legend('',frameon=False) # remove legend
plt.xlim([0,tspan])        # set x lim
#plt.xlabel('')               # remove x ticks
#plt.yticks([])               # remove y lim
plt.xticks([])
plt.ylabel("mL")
#plt.text(t_end+20,0.5,'glu_brain')      

ax2 = plt.subplot(gs[1])
plt.plot(tspan, y['Glu_liver'], label='glu_liver', color='b')
plt.legend('',frameon=False) # remove legend
plt.xlim([0,t_end])        # set x lim
#plt.xlabel("time")               # remove x ticks
#plt.yticks([])               # remove y lim
plt.ylabel("mL")
plt.xticks([])
#plt.text(t_end+20,0.3,'glu_liver')      

ax3 = plt.subplot(gs[2])
plt.plot(tspan, y['Glu_kidney'], label='glu_kidney', color='g')
plt.legend('',frameon=False) # remove legend
plt.xlim([0,t_end])        # set x lim
#plt.xlabel("time")               # remove x ticks
#plt.yticks([])               # remove y lim
plt.ylabel('mL')
plt.xticks([])
#plt.text(t_end+20,0.3,'glu_kidney')      

ax4 = plt.subplot(gs[3])
plt.plot(tspan, y['Glu_stomach'], label='glu_stomach', color='k')
plt.legend('',frameon=False) # remove legend
plt.xlim([0,t_end])        # set x lim
#plt.xlabel("time")               # remove x ticks
#plt.yticks([])               # remove y lim
plt.ylabel("mL")
#plt.xticks([])
#plt.text(t_end+20,0.2,'glu_stomach')   

ax5 = plt.subplot(gs[4])
plt.plot(tspan, y['Glu_consumed'], label='glu_consumed', color='k')
plt.legend('',frameon=False) # remove legend
plt.xlim([0,t_end])        # set x lim
plt.xlabel("time")               # remove x ticks
#plt.yticks([])               # remove y lim
plt.ylabel("mL")
#plt.xticks([])
#plt.text(t_end+20,0.2,'glu_consumed')    



plt.show()