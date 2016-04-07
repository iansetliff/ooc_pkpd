from compartments_project_modified import model
# from glucosis_metabolism import model
from pysb.integrate import odesolve
import numpy
import matplotlib.pyplot as plt


tspan = numpy.linspace(0, 500, 100000)

y = odesolve(model, tspan)

# plt.plot(tspan, y['Glu_blood'], label='glu_blood')
# plt.plot(tspan, y['Glu_liver'], label='glu_liver')
# plt.plot(tspan, y['Glu_pancreas'], label='glu_pancreas')
# plt.plot(tspan, y['Gly_liver'], label='gly_liver')
# plt.plot(tspan, y['insulin_liver'], label='insulin_liver')
# plt.plot(tspan, y['glucagon_liver'], label='glucagon_liver')

plt.plot(tspan, y['Glu_blood'], label='glu_blood')
plt.plot(tspan, y['Glu_brain_b'], label='glu_brain_b')
plt.plot(tspan, y['Glu_liver_b'], label='glu_liver_b')
plt.plot(tspan, y['Glu_kidney_b'], label='glu_kidney_b')
plt.plot(tspan, y['Glu_smint_b'], label='glu_smint_b')
plt.plot(tspan, y['Glu_muscle_b'], label='glu_muscle_b')
plt.plot(tspan, y['Glu_adipose_b'], label='glu_adipose_b')
plt.plot(tspan, y['Glu_brain_c'], label='glu_brain_c')
plt.plot(tspan, y['Glu_liver_c'], label='glu_liver_c')
plt.plot(tspan, y['Glu_kidney_c'], label='glu_kidney_c')
plt.plot(tspan, y['Glu_smint_c'], label='glu_smint_c')
plt.plot(tspan, y['Glu_muscle_c'], label='glu_muscle_c')
plt.plot(tspan, y['Glu_adipose_c'], label='glu_adipose_c')
# plt.plot(tspan, y['Glu_consumed'], label='glu_consumed')
plt.xlabel('time (min)')
plt.ylabel('Glucose (g)')
plt.legend()
plt.show()