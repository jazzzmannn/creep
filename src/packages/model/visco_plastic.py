"""
 Title: Visco-Plastic Model
 Description: For predicting all three stages of creep
 Author: Janzen Choi

"""

# Libraries
from neml import models, elasticity, drivers, surfaces, hardening, visco_flow, general_flow, damage

# Constants
YOUNGS       = 157000.0
POISSONS     = 0.3
S_RATE       = 1.0e-4
E_RATE       = 1.0e-4
HOLD         = 11500.0 * 3600.0
NUM_STEPS    = 501
MIN_DATA     = 50
PARAMS       = ['s0', 'R', 'd', 'n', 'eta', 'A', 'xi', 'phi']
L_BNDS       = [0.0e1, 0.0e1, 0.0e1, 0.0e1, 0.0e1, 0.0e1, 0.0e1, 0.0e1]
U_BNDS       = [1.0e2, 1.0e2, 1.0e1, 1.0e1, 1.0e4, 1.0e10, 1.0e1, 1.0e1]

# The Visco-Plastic model class
class ViscoPlastic:

    # Constructor
    def __init__(self, stresses):
        self.name = 'visco_plastic'
        self.params = PARAMS
        self.l_bnds = L_BNDS
        self.u_bnds = U_BNDS
        self.stresses = stresses

    # Creates the model
    def get_elvpdm_model(self, s0, R, d, n, eta, A, xi, phi):
        elastic_model = elasticity.IsotropicLinearElasticModel(YOUNGS, "youngs", POISSONS, "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(s0, R, d)
        g_power       = visco_flow.GPowerLaw(n, eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        elvp_model    = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        elvpdm_model  = damage.ModularCreepDamageModel_sd(elastic_model, A, xi, phi, damage.VonMisesEffectiveStress(), elvp_model, verbose=False)
        return elvpdm_model
    
    # Gets the predicted curves
    def get_prd_curves(self, s0, R, d, n, eta, A, xi, phi):
        
        # Gets the elastic, visco-plastic, damage model
        elvpdm_model = self.get_elvpdm_model(s0, R, d, n, eta, A, xi, phi)
        
        # Gets the predicted curves
        prd_x_data, prd_y_data = [], []
        for i in range(0,len(self.stresses)):
            
            # Get predictions
            try:
                creep_results = drivers.creep(elvpdm_model, self.stresses[i], S_RATE, HOLD, verbose=False, check_dmg=False, dtol=0.95, nsteps_up=150, nsteps=NUM_STEPS, logspace=False)
            except:
                return [], []
            prd_x_list = list(creep_results['rtime'] / 3600)
            prd_y_list = list(creep_results['rstrain'])
            
            # Make sure predictions contain more than MIN_DATA data points
            if len(prd_x_list) <= MIN_DATA or len(prd_y_list) <= MIN_DATA:
                return [], []
            prd_x_data.append(prd_x_list)
            prd_y_data.append(prd_y_list)

        # Returns it
        return prd_x_data, prd_y_data