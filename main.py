from src import sob
import numpy as np

def main():
    linux_system = False
    if linux_system:
        batch_file_path = "/media/feifan/TSHIBA/12_GitHub/OpenRadioss/linux_scripts_mk3/openradioss_run_script_ps.sh"
    else:
        batch_file_path = "D:/OpenRadioss/win_scripts_mk3/openradioss_run_script_ps.bat"

    a = sob.get_problem(1,3,'mass',batch_file_path)
    print(a([1,2,3]))
    print(a([1,2,5]))
    
    


if __name__ == '__main__':
    main()
