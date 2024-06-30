from src import sob
import numpy as np
import pandas as pd

'''
Once the optimization problem instance has been generate, the model is determined (mesh and fem data loaded) only when the variable array has been input.
'''

def main():
    linux_system = False
    if linux_system:
        batch_file_path = "/media/feifan/TSHIBA/12_GitHub/OpenRadioss/linux_scripts_mk3/openradioss_run_script_ps.sh"
    else:
        batch_file_path = "D:/OpenRadioss/win_scripts_mk3/openradioss_run_script_ps.bat"

    a = sob.get_problem(3,2,'mass',batch_file_path)
    a([1,2])
    b = sob.get_problem(3,3,'mass',batch_file_path)
    b([1,2,3])
    c = sob.get_problem(3,4,'intrusion',batch_file_path)
    c([1,2,3,4])
    c = sob.get_problem(3,5,'mass',batch_file_path)
    c([1,2,3,4,5])
    d = sob.get_problem(3,6,'mass',batch_file_path)
    d([1,2,3,4,5,-2])

if __name__ == '__main__':
    main()
