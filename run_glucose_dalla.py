import matplotlib.pyplot as plt
import numpy as np
from glucose_dalla import model
from pysb.integrate import odesolve

tspan = np.linspace(0,420,420)

y = odesolve(model, tspan)

# plt.plot(tspan, y['__s5'])
# plt.show()
#
# for i in range(len(model.species)):
#     plt.plot(tspan, y['__s%d' % i]/1.88)
# plt.show()

plt.plot(tspan, y['I_p_obs']/0.05, label="Plasma Insulin")
plt.ylim(0, 300)
plt.legend(loc=0)
plt.show()


# plt.plot(tspan, y['G_p_obs']/1.88, label="Plasma Glucose")
# plt.ylim(0, 200)
# plt.legend(loc=0)
# plt.show()