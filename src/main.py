"""
 Title: Main file
 Description: Main file for creep prediction
 Author: Janzen Choi

"""

# Libraries
import time
import package.io.excel as excel
import package.io.recorder as recorder
import package.model.visco_plastic as visco_plastic
import package.objective as objective
import package.genetic_algorithm as genetic_algorithm

# Constants
DATA_PATH = './'
DATA_FILE = 'alloy_617'
RECORD_PATH = './results/optimisation/'

# Initialisation
start_time = time.time()
print('Program begun at ' + time.strftime('%H:%M:%S', time.localtime()) + '!')

# Gets the experimental data
xl = excel.Excel(path = DATA_PATH, file = DATA_FILE)
test_names = xl.read_included('test')
exp_x_data = [xl.read_column(column = test_name + '_time', sheet = 'data') for test_name in test_names]
exp_y_data = [xl.read_column(column = test_name + '_strain', sheet = 'data') for test_name in test_names]
exp_stresses = xl.read_included('stress')
print('The experimental data for ' + str(len(test_names)) + ' test(s) has been read!')

# Prepares the optimisation
model = visco_plastic.ViscoPlastic(exp_stresses)
obj = objective.Objective(model, exp_x_data, exp_y_data)
moga = genetic_algorithm.MOGA(obj)
rec = recorder.Recorder(model, obj, moga, path = RECORD_PATH)
print('The optimisation has been prepared')

# Conducts the optimisation
obj.set_recorder(rec)
moga.optimise()
print('The optimisation has concluded!')

# End message
print('Program finished at ' + time.strftime('%H:%M:%S', time.localtime()) + ' in ' + str(round(time.time()-start_time)) + ' seconds!')