from pysb import *
import sympy

Model()


Monomer('G_p')
Monomer('G_t')
Monomer('I_p')
Monomer('I_l')
Monomer('X')
Monomer('Y')

#############  Some parameters

Parameter('b', 0.82)  # dimensionless
Parameter('D', 78000)  # Check out
Parameter('d', 0.01)  # dimensionless

Expression('aa', 2.5/((1-b)*D))
Expression('cc', 2.5/(d*D))

############# Glucose in plasma

# Rate of Appearance

Monomer('Q_sto1')
Monomer('Q_sto2')
Monomer('Q_gut')

Parameter('k_gri', 0.058)  # min^-1
Parameter('k_min', 0.008)  # min^-1
Parameter('k_max', 0.0558)  # min^-1
Parameter('k_abs', 0.057)  # min^-1

Observable('Q_sto1_obs', Q_sto1())
Observable('Q_sto2_obs', Q_sto2())
Expression('Q_sto', Q_sto1_obs + Q_sto2_obs)

Expression('k_empt', k_min + ((k_max-k_min)/2)*(sympy.tanh(aa*(Q_sto-b*D)) - sympy.tanh(cc*(Q_sto-d*D)) + 2))  # min^-1


Rule('qsto1_to_qsto2', Q_sto1() >> Q_sto2(), k_gri)
Rule('deg_qgut', Q_gut() >> None, k_abs)
Rule('qsto2_to_qgut', Q_sto2() >> Q_gut(), k_empt)

Observable('Q_gut_obs', Q_gut())

Parameter('f', 0.9)
Parameter('BW', 78)  # kg

Expression('Ra_exp', (f * k_abs / BW) * Q_gut_obs)

Rule('Ra', None >> G_p(), Ra_exp)

# Endogenous glucose production

Monomer('I_1')
Monomer('I_d')
Monomer('I_po')

Parameter('k_p1', 2.7)  # mg/kg/min
Parameter('k_p2', 0.0021)  # min^-1
Parameter('k_p3', 0.009)  # mg/kg/min per pmol/l
Parameter('k_p4', 0.0618)  # mg/kg/min per pmol/kg
Parameter('k_1', 0.065)  # min^-1
Parameter('k_2', 0.079)  # min^-2
Parameter('k_i', 0.0079)  # min^-1
Parameter('V_I', 0.05)  # l/kg

Observable('I_d_obs', I_d())
Observable('I_po_obs', I_po())
Observable('I_p_obs', I_p())

Expression('egp_partial', k_p1 - k_p3*I_d_obs - k_p4*I_po_obs)

Rule('egp_part1', None >> G_p(), egp_partial)
Rule('egp_part2', G_p() >> None, k_p2)
Rule('flow_Gt_to_Gp', G_t() >> G_p, k_2)
Rule('flow_Gp_to_Gt', G_p() >> G_t(), k_1)

Expression('rate_I_1', k_i*I_p_obs/V_I)

Rule('prod_I_1', None >> I_1(), rate_I_1)
Rule('I_1_to_I_d', I_1() >> I_d, k_i)
Rule('I_d_deg', I_d() >> None, k_i)

# Glucose utilization

Parameter('U_ii', -1)  # mg/kg/min

Rule('ins_ind_deg', None >> G_p(), U_ii)

############


############ Glucose in tissue

Parameter('part', 0.2)
Parameter('V_m0', 2.5)  # mg/kg/min
Parameter('V_mx', 0.047)  # mg/kg/min per pmol/l
Parameter('K_m0', 225.59)  # mg/kg)



Observable('X_obs', X())
Expression('V_mmax', (1-part)*(V_m0 + V_mx*X_obs))

Observable('G_t_obs', G_t())
Expression('U_id', -(V_mmax*G_t_obs)/(K_m0 + G_t_obs))

Rule('ins_dep_deg', None >> G_t(), U_id)

# Expression('G_t_free0',
#            (G_t_0 + X_t_0 - Km2) / 2 +
#            ((S2_tot + E1_tot - Km2) ** 2 + 4 * Km2) ** 0.5 / 2)


############

############ Insulin subsystem

Parameter('m_1', 0.19)  # min^-1
Parameter('m_2', 0.484)  # min^-1
Parameter('m_4', 0.194)  # min^-1
Parameter('m_5', 0.0304)  # min*kg/pmol
Parameter('m_6', 0.6471)  # dimensionless
Parameter('gamma1', 0.5)  # min^-1
Parameter('K', 2.3)  # pmol/k per mg/dl
Parameter('V_G', 1.88)  # dl/kg
Parameter('S_b', 1.8)
Parameter('p_2U', 0.0331)  # min^-1
Parameter('I_b', 25)
Parameter('alpha', 0.050)  # min^-1
Parameter('beta', 0.11)  # pmol/kg/min per (mg/dl)
Parameter('G_b', 95)


Rule('flow_Il_to_Ip', I_l() >> I_p(), m_1)
Rule('flow_Ip_to_Il', I_p() >> I_l(), m_2)
Rule('flow_Ipo_to_Il', I_po() >> I_l, gamma1)

Expression('HE', (-m_5*gamma1*I_po_obs) + m_6)
Expression('m_3', (HE*m_1)/(1-HE))
Rule('Il_deg', I_l() >> None, m_3)

Rule('Ip_deg', I_p() >> None, m_4)

Observable('G_p_obs', G_p())
Expression('egp_Y_partial', k_p1 - k_p2*G_p_obs - k_p3*I_d_obs)

Observable('Y_obs', Y())
Expression('S_po', Y_obs + (K*(egp_Y_partial + Ra_exp + U_ii - k_1*G_p_obs + k_2*G_t_obs)/V_G) + S_b)
Rule('I_po_prod', None >> I_po(), S_po)

Expression('K_kp4', K*k_p4)
Rule('I_po_deg', I_po() >> None, K_kp4)

Rule('X_deg', X() >> None, p_2U)

Expression('prod_deg', p_2U*((I_p_obs/V_I) - I_b))
Rule('X_prod_deg', None >> X(), prod_deg)

Rule('Y_deg', Y() >> None, alpha)

Expression('Y_prod_rate', alpha*beta*((G_p_obs/V_G) - G_b))
Rule('Y_production', None >> Y(), Y_prod_rate)
###########


# Initial conditions

Parameter('G_p_0', 178)
Parameter('G_t_0', 135)
Parameter('I_l_0', 4.5)
Parameter('I_p_0', 1.25)
Parameter('Q_sto1_0', 78000)
Parameter('I_1_0', 25)
Parameter('I_d_0', 25)
Parameter('I_po_0', 3.6)

Initial(G_p(), G_p_0)
Initial(G_t(), G_t_0)
Initial(I_l(), I_l_0)
Initial(I_p(), I_p_0)
Initial(Q_sto1(), Q_sto1_0)
Initial(I_1(), I_1_0)
Initial(I_d(), I_d_0)
Initial(I_po(), I_po_0)
