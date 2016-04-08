from compartments_project_modified import model
# from glucosis_metabolism import model
from pysb.integrate import odesolve
import numpy
import matplotlib.pyplot as plt
from colour import Color
import matplotlib.cm as cm


red = Color("red")
colors = list(red.range_to(Color("green"),10))


tspan = numpy.linspace(0, 500, 100000)

y = odesolve(model, tspan)

x = numpy.arange(len(model.observables))
ys = [i+x+(i*x)**2 for i in range(10)]

colors = cm.rainbow(numpy.linspace(0, 1, len(ys)))

for i,c in zip(model.observables, colors):
    print i.name
    plt.plot(tspan, y[i.name], label=i.name, color=c)
plt.legend(loc=0)
plt.show()

# plt.plot(tspan, y['Glu_blood'], label='glu_blood')
# plt.plot(tspan, y['Glu_brain_b'], label='glu_brain_b')
# plt.plot(tspan, y['Glu_liver_b'], label='glu_liver_b')
# plt.plot(tspan, y['Glu_kidney_b'], label='glu_kidney_b')
# plt.plot(tspan, y['Glu_smint_b'], label='glu_smint_b')
# plt.plot(tspan, y['Glu_muscle_b'], label='glu_muscle_b')
# plt.plot(tspan, y['Glu_adipose_b'], label='glu_adipose_b')
# plt.plot(tspan, y['Glu_brain_c'], label='glu_brain_c')
# plt.plot(tspan, y['Glu_liver_c'], label='glu_liver_c')
# plt.plot(tspan, y['Glu_kidney_c'], label='glu_kidney_c')
# plt.plot(tspan, y['Glu_smint_c'], label='glu_smint_c')
# plt.plot(tspan, y['Glu_muscle_c'], label='glu_muscle_c')
# plt.plot(tspan, y['Glu_adipose_c'], label='glu_adipose_c')
# # plt.plot(tspan, y['Glu_consumed'], label='glu_consumed')
# plt.xlabel('time (min)')
# plt.ylabel('Glucose (g)')
# plt.legend()
# plt.show()