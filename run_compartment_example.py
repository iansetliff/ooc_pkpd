from compartments_project import model
# from glucosis_metabolism import model
from pysb.integrate import odesolve
import numpy
import matplotlib.pyplot as plt


tspan = numpy.linspace(0, 50, 1000)

y = odesolve(model, tspan)

# plt.plot(tspan, y['Glu_blood'], label='glu_blood')
# plt.plot(tspan, y['Glu_liver'], label='glu_liver')
# plt.plot(tspan, y['Glu_pancreas'], label='glu_pancreas')
# plt.plot(tspan, y['Gly_liver'], label='gly_liver')
# plt.plot(tspan, y['insulin_liver'], label='insulin_liver')
# plt.plot(tspan, y['glucagon_liver'], label='glucagon_liver')


plt.plot(tspan, y['Glu_brain'], label='glu_brain')
plt.plot(tspan, y['Glu_liver'], label='glu_liver')
plt.plot(tspan, y['Glu_kidney'], label='glu_kidney')
plt.plot(tspan, y['Glu_stomach'], label='glu_stomach')
plt.plot(tspan, y['Glu_consumed'], label='glu_consumed')
plt.xlabel('time')
plt.ylabel('mL')
plt.legend()
plt.show()