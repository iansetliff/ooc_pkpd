from pysb import *

Model()


# Defining monomers:

Monomer('Glucose', ['Y', 'b'], {'Y': ['Glu', 'Gly']})
Monomer('insu_blocker', ['b'])
Monomer('gluco_prod', ['b'])
Monomer('insulin', ['b'])
Monomer('glucagon', ['b'])


# Taggart, Starr and Cecie Starr. Biology: The Unity and Diversity of Life. California: Wadsworth, 1989: 398.
Parameter('Vblood', 5000) # all volumes in ml
# http://ispub.com/IJRA/13/1/9978
Parameter('Vliver', 1393)
# https://en.wikipedia.org/wiki/Brain_size
Parameter('Vpancreas', 72.4)

Parameter('Vstomach', 2000) #2-4L


# NOT SURE WE NEED IT Parameter('Vadipose')

# Then we initialize the compartments with their respective volume
Compartment('Blood', None, 3, Vblood)
Compartment('Liver', None, 3, Vliver)
Compartment('Pancreas', None, 3, Vpancreas)
Compartment('Stomach', None, 3, Vstomach)


# Here we define the flow rates in ml/min of the different compartments
Parameter('Q_liver', 25.5) # 17/ml/min/kg perfusion rate * 1.5kg (liver mass)http://hypertextbook.com/facts/2004/MaryPennisi.shtml
Parameter('Q_pancreas', 20) #http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1411372/?page=3
Parameter('Q_stomach', 166.25) #1.33/ml/min/g rate * 125 g(stomach mass) http://cancerres.aacrjournals.org/content/46/12_Part_1/6299.full.pdf

# Kinetic parameters
Parameter('kf1', 20)
Parameter('kr1', 10)
Parameter('kcat', 5)

# Consumption rate

Parameter('CR', 0.1)

# Glucose flowing

Rule('Glu_to_stomach', Glucose(Y='Glu', b=None) ** Stomach <> Glucose(Y='Glu', b=None) ** Blood, Q_stomach, Q_stomach)
Rule('Glu_to_liver', Glucose(Y='Glu', b=None) ** Blood <> Glucose(Y='Glu', b=None) ** Liver, Q_liver, Q_liver)
Rule('Glu_to_pancreas', Glucose(Y='Glu', b=None) ** Blood <> Glucose(Y='Glu', b=None) ** Pancreas, Q_pancreas, Q_pancreas)
Rule('insulin_to_blood', insulin(b=None) ** Pancreas <> insulin(b=None) ** Liver, Q_pancreas, Q_pancreas)
Rule('glucagon_to_blood', glucagon(b=None) ** Pancreas <> glucagon(b=None) ** Liver, Q_pancreas, Q_pancreas)
Rule('Gly_to_blood', Glucose(Y='Gly', b=None) ** Liver <> Glucose(Y='Glu', b=None) ** Blood, Q_liver, Q_liver)

# Glucose consumption


Rule('glu_ins_blo', Glucose(Y='Glu', b=None)**Pancreas + insu_blocker(b=None)**Pancreas <> Glucose(Y='Glu', b=1)**Pancreas % insu_blocker(b=1)**Pancreas, kf1, kr1)
Rule('ins_blo_ins', insu_blocker(b=None)**Pancreas + insulin(b=None)**Pancreas <> insu_blocker(b=1)**Pancreas % insulin(b=1)**Pancreas, kf1, kr1)
Rule('ins_glu', insulin(b=None)**Liver + Glucose(Y='Glu', b=None)**Liver <> insulin(b=1)**Liver %  Glucose(Y='Glu', b=1)**Liver, kf1, kr1)
Rule('glu_to_gly', insulin(b=1)**Liver % Glucose(Y='Glu', b=1)**Liver >> Glucose(Y='Gly', b=None)**Liver, kcat)


Rule('glu_gluco_prod', Glucose(Y='Glu', b=None)**Pancreas + gluco_prod(b=None)**Pancreas <> Glucose(Y='Glu', b=1)**Pancreas % gluco_prod(b=1)**Pancreas, kf1, kr1)
Rule('gluco_prod_gluca', gluco_prod(b=None)**Pancreas + glucagon(b=None)**Pancreas >> glucagon(b=None)**Pancreas, kcat)
Rule('gluca_glu', glucagon(b=None)**Liver +  Glucose(Y='Gly', b=None)**Liver <> glucagon(b=1)**Liver %  Glucose(Y='Gly', b=1)**Liver, kf1, kr1)
Rule('gly_to_glu', glucagon(b=1)**Liver %  Glucose(Y='Gly', b=1)**Liver >> Glucose(Y='Glu', b=None)**Liver, kcat)

# Observables

Observable('Glu_blood', Glucose(Y='Glu', b=None) ** Blood)
Observable('Glu_liver', Glucose(Y='Glu', b=None) ** Liver)
Observable('Glu_pancreas', Glucose(Y='Glu', b=None) ** Pancreas)
Observable('Gly_liver', Glucose(Y='Gly', b=None) ** Liver)
Observable('insulin_liver', insulin(b=None) ** Liver)
Observable('glucagon_liver', insulin(b=None) ** Liver)

# Observable('Glu_consumed', Glu(Y='C', b=None) ** Brain)


# Initial conditions

Parameter('gatorade', 350)
Parameter('insu_0', 50)
Parameter('gluca_0', 5)

Initial(Glucose(Y='Glu', b=None) ** Stomach, gatorade)
Initial(insulin(b=None) ** Pancreas, insu_0)
Initial(glucagon(b=None)**Pancreas, gluca_0)