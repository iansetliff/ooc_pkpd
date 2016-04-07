from pysb import *

Model()


# Defining monomers:

Monomer('Glu', ['Y', 'b'], {'Y': ['C', 'NC']})
Monomer('Gly',['b'])
Monomer('Ins',['h'])
# Monomer('Gon',['h'])
# Monomer('GLUT4',['h'])
# Monomer('Lactate',['b'])


Parameter('Vlumen',1800) # Intestinal lumen

# Blood volumes
Parameter('Vliver_b', 500)
Parameter('Vbrain_b', 60)
Parameter('Vsmint_b', 190)
Parameter('Vkidney_b', 100)
Parameter('Vmuscle_b',700)
Parameter('Vadipose_b',250)
Parameter('Vblood',3200)

# Cellular volumes (total - blood)
Parameter('Vliver_c', 1200) 
Parameter('Vbrain_c', 1070)
Parameter('Vsmint_c', 1000) # Need actual value 
Parameter('Vkidney_c', 300) 
Parameter('Vmuscle_c',26000)
Parameter('Vadipose_c',16300)

# Then we initialize the compartments with their respective volume
Compartment('Lumen', None, 3, Vlumen)
Compartment('Liver_b', None, 3, Vliver_b)
Compartment('Brain_b', None, 3, Vbrain_b)
Compartment('Smint_b', None, 3, Vsmint_b)
Compartment('Kidney_b', None, 3, Vkidney_b)
Compartment('Muscle_b', None, 3, Vmuscle_b)
Compartment('Adipose_b', None, 3, Vadipose_b)
Compartment('Liver_c', None, 3, Vliver_c)
Compartment('Brain_c', None, 3, Vbrain_c)
Compartment('Smint_c', None, 3, Vsmint_c)
Compartment('Kidney_c', None, 3, Vkidney_c)
Compartment('Muscle_c', None, 3, Vmuscle_c)
Compartment('Adipose_c', None, 3, Vmuscle_c)
Compartment('Blood', None, 3, Vblood)

# Here we define the flow rates in ml/min of the different compartments
Parameter('Q_lumen', 4) # Need to find actual value 
Parameter('Q_liver', 1275)
Parameter('Q_brain', 600)
Parameter('Q_smint', 500)
Parameter('Q_kidney', 950)
Parameter('Q_muscle', 850)
Parameter('Q_adipose', 250)

# Glucose flowing

Rule('Glu_into_body', Glu(Y='NC', b=None) ** Lumen <> Glu(Y='NC', b = None) ** Smint_b, Q_lumen, Q_lumen)
Rule('Glu_to_blood', Glu(Y='NC', b=None) ** Smint_b <> Glu(Y='NC', b=None) ** Blood, Q_smint, Q_smint)
Rule('Glu_to_liver', Glu(Y='NC', b=None) ** Blood <> Glu(Y='NC', b=None) ** Liver_b, Q_liver, Q_liver)
Rule('Glu_to_kidney', Glu(Y='NC', b=None) ** Blood <> Glu(Y='NC', b=None) ** Kidney_b, Q_kidney, Q_kidney)
Rule('Glu_to_brain', Glu(Y='NC', b=None) ** Blood <> Glu(Y='NC', b=None) ** Brain_b, Q_kidney, Q_kidney)
Rule('Glu_to_muscle', Glu(Y='NC', b = None) ** Blood <> Glu(Y='NC', b=None) ** Muscle_b, Q_muscle, Q_muscle)
Rule('Glu_to_adipose', Glu(Y='NC', b = None) ** Blood <> Glu(Y='NC', b=None) ** Adipose_b, Q_adipose, Q_adipose)

# Basic glucose blood to cellular transport
Parameter('kf1',0.01)     # How do I figure out actual values?
Parameter('kr1',0.0001)   # Do I need reverse reaction? 
Parameter('kf1_1',0.001)  # 
Parameter('kr1_1',0.00001) # 
Rule('Glu_in_liver', Glu(Y='NC', b=None) ** Liver_b <> Glu(Y='NC', b=None) ** Liver_c, kf1, kr1)
Rule('Glu_in_smint', Glu(Y='NC', b=None) ** Smint_b <> Glu(Y='NC', b=None) ** Smint_c, kf1_1, kr1_1)
Rule('Glu_in_kidney', Glu(Y='NC', b=None) ** Kidney_b <> Glu(Y='NC', b=None) ** Kidney_c, kf1_1, kr1_1)
Rule('Glu_in_brain', Glu(Y='NC', b=None) ** Brain_b <> Glu(Y='NC', b=None) ** Brain_c, kf1, kr1)
Rule('Glu_in_muscle', Glu(Y='NC', b=None) ** Muscle_b <> Glu(Y='NC', b=None) ** Muscle_c, kf1, kr1)
Rule('Glu_in_adipose', Glu(Y='NC', b=None) ** Adipose_b <> Glu(Y='NC', b=None) ** Adipose_c, kf1, kr1)

# Insulin in blood dependent on amount of glucose
Parameter('kins',0.0004)
Rule('Ins_prod', Glu(Y='NC', b=None) ** Blood >> Glu(Y='NC', b=None) ** Blood + Ins(h=None) ** Blood, kins)

# Insulin flowing
Rule('Ins_to_blood', Ins(h=None) ** Blood <> Ins(h=None) ** Smint_b, Q_smint, Q_smint)
Rule('Ins_to_liver', Ins(h=None) ** Blood <> Ins(h=None) ** Liver_b, Q_liver, Q_liver)
Rule('Ins_to_kidney',Ins(h=None) ** Blood <> Ins(h=None) ** Kidney_b, Q_kidney, Q_kidney)
Rule('Ins_to_brain', Ins(h=None) ** Blood <> Ins(h=None) ** Brain_b, Q_kidney, Q_kidney)
Rule('Ins_to_muscle', Ins(h=None) ** Blood <> Ins(h=None) ** Muscle_b, Q_muscle, Q_muscle)
Rule('Ins_to_adipose', Ins(h=None) ** Blood <> Ins(h=None) ** Adipose_b, Q_adipose, Q_adipose)

# Insulin regulated glucose uptake
Parameter('kf2',0.04)
Parameter('kr2',0.004)
Rule('Glu_in_liver_ins', Glu(Y='NC', b=None) ** Liver_b + Ins(h=None) ** Liver_b <> Glu(Y='NC', b=None) ** Liver_c, kf2, kr2)
Rule('Glu_in_smint_ins', Glu(Y='NC', b=None) ** Smint_b + Ins(h=None) ** Smint_b <> Glu(Y='NC', b=None) ** Smint_c, kf2, kr2)
Rule('Glu_in_kidney_ins', Glu(Y='NC', b=None) ** Kidney_b + Ins(h=None) ** Kidney_b <> Glu(Y='NC', b=None) ** Kidney_c, kf2, kr2)
Rule('Glu_in_muscle_ins', Glu(Y='NC', b=None) ** Muscle_b + Ins(h=None) ** Muscle_b <> Glu(Y='NC', b=None) ** Muscle_c, kf2, kr2)
Rule('Glu_in_adipose_ins', Glu(Y='NC', b=None) ** Adipose_b + Ins(h=None) ** Adipose_b <> Glu(Y='NC', b=None) ** Adipose_c, kf2, kr2)

# Glucose consumption

Parameter('CR_brain',0.08333) # g/min = 120 g/day 
Parameter('CR',0.07)

Rule('Glu_consumption_brain', Glu(Y='NC', b=None) ** Brain_c >> Glu(Y='C', b=None) ** Brain_c, CR_brain)
Rule('Glu_consumption_liver', Glu(Y='NC', b=None) ** Liver_c >> Glu(Y='C', b=None) ** Liver_c, CR)
Rule('Glu_consumption_smint', Glu(Y='NC', b=None) ** Smint_c >> Glu(Y='C', b=None) ** Smint_c, CR)
Rule('Glu_consumption_kidney', Glu(Y='NC', b=None) ** Kidney_c >> Glu(Y='C', b=None) ** Kidney_c, CR)
Rule('Glu_consumption_muscle', Glu(Y='NC', b=None) ** Muscle_c >> Glu(Y='C', b=None) ** Muscle_c, CR)
Rule('Glu_consumption_adipose', Glu(Y='NC', b=None) ** Adipose_c >> Glu(Y='C', b=None) ** Adipose_c, CR)
# Rule('Gly_production_liver', Glu(Y='NC',b=None) ** Liver >> Gly(b=None) ** Liver, GR)
# Rule('Gly_production_muscle', Glu(Y='NC',b=None) ** Muscle >> Gly(b=None) ** Muscle, GR)


# Observables

Observable('Glu_blood', Glu(Y='NC', b=None) ** Blood)
Observable('Glu_brain_b', Glu(Y='NC', b=None) ** Brain_b)
Observable('Glu_liver_b', Glu(Y='NC', b=None) ** Liver_b)
Observable('Glu_kidney_b', Glu(Y='NC', b=None) ** Kidney_b)
Observable('Glu_smint_b', Glu(Y='NC', b=None) ** Smint_b)
Observable('Glu_muscle_b', Glu(Y='NC', b=None) ** Muscle_b)
Observable('Glu_adipose_b', Glu(Y='NC', b=None) ** Adipose_b)
Observable('Glu_brain_c', Glu(Y='NC', b=None) ** Brain_c)
Observable('Glu_liver_c', Glu(Y='NC', b=None) ** Liver_c)
Observable('Glu_kidney_c', Glu(Y='NC', b=None) ** Kidney_c)
Observable('Glu_smint_c', Glu(Y='NC', b=None) ** Smint_c)
Observable('Glu_muscle_c', Glu(Y='NC', b=None) ** Muscle_c)
Observable('Glu_adipose_c', Glu(Y='NC', b=None) ** Adipose_c)
Observable('Glu_brain_con', Glu(Y='C', b=None) ** Brain_c)
Observable('Glu_liver_con', Glu(Y='C', b=None) ** Liver_c)
Observable('Glu_kidney_con', Glu(Y='C', b=None) ** Kidney_c)
Observable('Glu_smint_con', Glu(Y='C', b=None) ** Smint_c)
Observable('Glu_muscle_con', Glu(Y='C', b=None) ** Muscle_c)
Observable('Glu_adipose_con', Glu(Y='C', b=None) ** Adipose_c)
# Observable('Gly_liver', Gly(b=None) ** Liver)
# Observable('Gly_muscle', Gly(b=None) ** Muscle)


# Initial conditions

Parameter('gatorade', 35)
Initial(Glu(Y='NC', b=None) ** Lumen, gatorade)
Parameter('ins',0.1)
Initial(Ins(h=None) ** Blood,ins)