from pysb import *

Model()


# Defining monomers:

Monomer('Glu', ['Y', 'b'], {'Y': ['C', 'NC']})

# TODO  add skeleton muscle, adipose tissue

# Taggart, Starr and Cecie Starr. Biology: The Unity and Diversity of Life. California: Wadsworth, 1989: 398.
Parameter('Vblood', 5000) # all volumes in ml
# http://ispub.com/IJRA/13/1/9978
Parameter('Vliver', 1393)
# https://en.wikipedia.org/wiki/Brain_size
Parameter('Vbrain', 1130)
# Curtis, Helena & N. Sue Barnes. Invitation to Biology. 5th Edition. New York: Worth, 1994: 529.
Parameter('Vstomach', 2000) #2-4L
# http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3071164/
Parameter('Vkidney', 200) #the two kidneys

# NOT SURE WE NEED IT Parameter('Vadipose')

# Then we initialize the compartments with their respective volume
Compartment('Blood', None, 3, Vblood)
Compartment('Liver', None, 3, Vliver)
Compartment('Brain', None, 3, Vbrain)
Compartment('Stomach', None, 3, Vstomach)
Compartment('Kidney', None, 3, Vkidney)

# Here we define the flow rates in ml/min of the different compartments
Parameter('Q_liver', 25.5) # 17/ml/min/kg perfusion rate * 1.5kg (liver mass)http://hypertextbook.com/facts/2004/MaryPennisi.shtml
Parameter('Q_brain', 800)
Parameter('Q_stomach', 166.25) #1.33/ml/min/g rate * 125 g(stomach mass) http://cancerres.aacrjournals.org/content/46/12_Part_1/6299.full.pdf
Parameter('Q_kidney', 500)

# Consumption rate

Parameter('CR', 0.1)

# Glucose flowing

Rule('Glu_to_stomach', Glu(Y='NC', b=None) ** Blood <> Glu(Y='NC', b=None) ** Stomach, Q_stomach, Q_stomach)
Rule('Glu_stomach_liver', Glu(Y='NC', b=None) ** Stomach <> Glu(Y='NC', b=None) ** Liver, Q_liver, Q_liver)
Rule('Glu_to_liver', Glu(Y='NC', b=None) ** Blood <> Glu(Y='NC', b=None) ** Liver, Q_liver, Q_liver)
Rule('Glu_to_kidney', Glu(Y='NC', b=None) ** Blood <> Glu(Y='NC', b=None) ** Kidney, Q_kidney, Q_kidney)
Rule('Glu_to_brain', Glu(Y='NC', b=None) ** Blood <> Glu(Y='NC', b=None) ** Brain, Q_kidney, Q_kidney)

# Glucose consumption

Rule('Glu_consumption', Glu(Y='NC', b=None) ** Brain >> Glu(Y='C', b=None) ** Brain, CR)


# Observables

Observable('Glu_brain', Glu(Y='NC', b=None) ** Brain)
Observable('Glu_liver', Glu(Y='NC', b=None) ** Liver)
Observable('Glu_kidney', Glu(Y='NC', b=None) ** Kidney)
Observable('Glu_stomach', Glu(Y='NC', b=None) ** Stomach)
Observable('Glu_consumed', Glu(Y='C', b=None) ** Brain)


# Initial conditions

Parameter('gatorade', 350)
Initial(Glu(Y='NC', b=None) ** Stomach, gatorade)