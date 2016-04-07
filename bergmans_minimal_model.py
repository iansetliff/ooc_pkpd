from pysb import *
from pysb.integrate import odesolve
from pysb.macros import *
import sympy
import numpy
import matplotlib.pyplot as plt
Model()


# Defining monomers:
Monomer('I', ['l'], {'l': ['u', 'b']})
Monomer('ticks')
Monomer('__source__')
Monomer('__sink__')

Parameter('k', 10)
Parameter('kmL', 10)
Parameter('tick', 100)

Observable('Ibound', I(l='b'))
Observable('t_obs', ticks())

Expression('Lig_fun', k*(1+sympy.cos(t_obs/tick)))

Rule('production', None >> ticks(), tick)
Rule('change', I(l='u') <> I(l='b'), Lig_fun, kmL)

Parameter('i_0', 100)
Parameter('ticks_0', 0)
Parameter('__source_0', 1)

Initial(I(l='u'), i_0)
Initial(ticks(), ticks_0)
Initial(__source__(), __source_0)


Monomer('G', ['b']) # Blood glucose concentration
Monomer('X', ['b'])

Parameter('k_1', 2)
Parameter('k_1p', 1)
Parameter('k_2', 3)
Parameter('k_3', 4)

Rule('glu_prod', None >> G(b=None), k_1)
Rule('glu_cons', G(b=None) >> __sink__(), k_1)
Rule('glu_binding', G(b=None) + X(b=None) >> G(b=1) % X(b=1), k_1p)



Parameter('x_0', 10)
Initial(X(b=None), x_0)




tspan = numpy.linspace(0, 50, 500)
y = odesolve(model, tspan)

plt.plot(tspan, y['Ibound'])
plt.show()



#
#
# Parameter('V_G', 5000)
# Parameter('V_rp', 1393)  #check this number
# Parameter('V_liver', 1393)
# Parameter('V_peripheral', 400) #check this number
#
#
# # Then we initialize the compartments with their respective volume
# Compartment('glucose_compartment', None, 3, V_G)
# Compartment('remote_pool', None, 3, V_rp)
# Compartment('liver', None, 3, V_liver)
# Compartment('peripheral', None, 3, V_peripheral)
#
# # Here we define the flow rates in ml/min of the different compartments
# Parameter('Q_G1', 25.5)
# Parameter('Q_G2', 20)
# Parameter('Q_I1', 166.25)
# Parameter('Q_I2', 166.25)
#
# Parameter('k_b', 1)
#
# # Rule('synthesize', G_b(b=None)**Glucose_compartment, k)
# Rule('flow_liver', G(b=None)**liver <> G(b=None)**glucose_compartment, Q_G2, Q_G2)
# Rule('flow_peripheral', G(b=None)**peripheral <> G(b=None)**glucose_compartment, Q_G1, Q_G1)
# Rule('glucose_insulin_peri', G(b=None)**peripheral + I(b=None)**peripheral >> G(b=1)**peripheral % I(b=1)**peripheral, k_b)
# Rule('glucose_insulin_liver', G(b=None)**liver + I(b=None)**liver >> G(b=1)**liver % I(b=1)**liver, k_b)
# Rule('glucose_formation', None >> G(b=None)**liver, k_b)
# Rule('glucose_clearence', G(b=None)**peripheral >> None, k_b)