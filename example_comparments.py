from pysb import *

Model()

# Defining the monomers of the PK/PD model. For this specific example we are defining:
# 5-FU: C_FU, it has a binding site 'b' to bind to DPD
# Uracil: C_U, it has a binding site 'b' to bind to DPD
# dihydropyrimidine dehydrogenase: DPD, it has a binding site 's' where either 5-FU or Uracil can bind, this is for
# the competitive inhibition
# Metabolized 5-FU: P, this is the metabolized 5-FU

Monomer('C_FU', ['b'])
Monomer('C_U', ['b'])
Monomer('DPD', ['s'])
Monomer('P')

# Here we define the volume of the four 3d compartments as parameters
Parameter('Vreservoir', 1)
Parameter('Vliver', 1)
Parameter('Vtumor', 1)
Parameter('Vmarrow', 1)

# Then we initialize the compartments with their respective volume
Compartment('Reservoir', None, 3, Vreservoir)
Compartment('Liver', None, 3, Vliver)
Compartment('Tumor', None, 3, Vtumor)
Compartment('Marrow', None, 3, Vmarrow)

# Here we define the flow rates of the different compartments
Parameter('Q_liver', 1)
Parameter('Q_tumor', 1)
Parameter('Q_marrow', 1)

# Kinetic parameters for the competitive inhibition of Uracil for the DPD enzyme

Parameter('kf1', 1)
Parameter('kr1', 1)
Parameter('kf2', 1)
Parameter('kr2', 1)
Parameter('kcat', 1)

# Rules for theChemical reactions and flows between the comparments
# According to Sung et al 2010, DOI: 10.1039/b917763a, the in flow and out flow rates are the same.

########## Liver ############

# FU: This rules defines the reversible flow from C_FU from the reservoir to the Liver and vice versa.

Rule('C_FU_to_liver', C_FU(b=None) ** Reservoir <> C_FU(b=None) ** Liver, Q_liver, Q_liver)

# Uracil: This rules defines the reversible flow from C_U from the reservoir to the Liver and vice versa.

Rule('C_U_to_liver', C_U(b=None) ** Reservoir <> C_U(b=None) ** Liver, Q_liver, Q_liver)

# Competitive inhibition of Uracil for DPD (Enzyme that metabolizes 5-FU)
# Competitive inhibition: EI + S <> E + S + I <> ES + I >> E + P + I
# where E is the enzyme which in our case is DPD, I is the inhibitor which in our case Uracil, S is the substract which
# in our case is 5-FU, and P is the product which in our case is the metabolized 5-FU, the reaction only happens in
# The liver.
# The symbol "%" means that two monomers are bound together, and the symbol "**" is a tag to the compartment

Rule('ReversibleBinding1', DPD(s=1) ** Liver % C_U(b=1) ** Liver + C_FU(b=None) ** Liver <> DPD(s=None) ** Liver +
     C_U(b=None) ** Liver + C_FU(b=None) ** Liver, kf1, kr1)
Rule('ReversibleBinding2', DPD(s=None) ** Liver + C_U(b=None) ** Liver + C_FU(b=None) ** Liver <>
     DPD(s=1) ** Liver % C_FU(b=1) ** Liver + C_U(b=None) ** Liver, kf2, kr2)
Rule('Production', DPD(s=1) % C_FU(b=1) >> DPD(s=None) + P(), kcat)

########## Tumor ############

# FU: This rules defines the reversible flow from C_FU from the reservoir to the Tumor and vice versa.

Rule('C_FU_to_tumor', C_FU(b=None) ** Reservoir <> C_FU(b=None) ** Tumor, Q_tumor, Q_tumor)

# Uracil: This rules defines the reversible flow from C_U from the reservoir to the Tumor and vice versa.

Rule('C_U_to_tumor', C_U(b=None) ** Reservoir <> C_U(b=None) ** Tumor, Q_tumor, Q_tumor)

########## Marrow ############

# FU: This rules defines the reversible flow from C_FU from the reservoir to the Marrow and vice versa.

Rule('C_FU_to_marrow', C_FU(b=None) ** Reservoir <> C_FU(b=None) ** Marrow, Q_marrow, Q_marrow)

# Uracil: This rules defines the reversible flow from C_U from the reservoir to the Marrow and vice versa.

Rule('C_U_to_marrow', C_U(b=None) ** Reservoir <> C_U(b=None) ** Marrow, Q_marrow, Q_marrow)

# Initial conditions

Parameter('C_FU_0', 1000)
Parameter('C_U_0', 100)
Parameter('DPD_0', 10)

Initial(C_FU(b=None) ** Reservoir, C_FU_0)
Initial(C_U(b=None) ** Reservoir, C_U_0)
Initial(DPD(s=None) ** Liver, DPD_0)
