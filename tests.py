from src import sob
import numpy as np

batch_file_path = "D:/OpenRadioss/win_scripts_mk3/openradioss_run_script_ps.bat"

def generate_multiple_instances():
    # Generate the first StarBox instance and run simulation
    a = sob.StarBox(3,'a',batch_file_path)
    a.generate_input_deck([1,2,3])
    a.run_simulation()

    # Generate the second StarBox instance
    b = sob.StarBox(5,'a',batch_file_path)
    b.generate_input_deck([1,2,3,4,5])
    print(b.problem_id)

def check_mass():
    a = sob.StarBox(3,'a',batch_file_path)
    a.generate_input_deck([1,2,3])
    print(a.model.mass())

    b = sob.StarBox(5,'a',batch_file_path)
    b.generate_input_deck([1,2,3,4,5])
    print(b.model.mass())

    c = sob.StarBox(5,'a',batch_file_path)
    c.generate_input_deck([1,2,3,4,2])
    print(c.model.mass())

def check_multi_input():
    a = sob.get_problem(1,3,'mass',batch_file_path)
    print(a([1,2,3]))
    print(a([1,2,5]))

def check_absorbed_energy():
    # result should be the same, since the design variables don't influence the mass and velocity of the wall
    a = sob.get_problem(1,3,'absorbed_energy',batch_file_path)
    print(a([1,2,3]))
    print(a([1,2,5]))