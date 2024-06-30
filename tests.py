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
    # the second result should be larger than the first one, because the thickness (the third variable) is larger
    a = sob.get_problem(1,3,'mass',batch_file_path)
    print(a([1,2,3]))
    print(a([1,2,5]))

def check_absorbed_energy():
    # result should be the same, since the design variables don't influence the mass and velocity of the wall
    a = sob.get_problem(1,3,'absorbed_energy',batch_file_path)
    print(a([1,2,3]))
    print(a([1,2,5]))

def check_intrusion():
    # intrusion 2 should be smaller than intrusion 1, since the second model has larger thickness 
    # Result: 
    # Intrusion1: 49.340218 
    # Intrusion2: 31.747295
    a = sob.get_problem(1,3,'intrusion',batch_file_path)
    intrusion1 = a([1,2,3])
    intrusion2 = a([1,2,5])
    print("Intrusion 1:"+str(intrusion1))
    print("Intrusion 2:"+str(intrusion2))

def check_crashtube_mesh_generation():
    # check the parameters added for trigger generation (see py_mesh.input)
    a = sob.get_problem(3,2,'mass',batch_file_path)
    a([1,2])
    b = sob.get_problem(3,3,'mass',batch_file_path)
    b([1,2,3])
    c = sob.get_problem(3,4,'mass',batch_file_path)
    c([1,2,3,4])
    c = sob.get_problem(3,5,'mass',batch_file_path)
    c([1,2,3,4,5])
    d = sob.get_problem(3,6,'mass',batch_file_path)
    d([1,2,3,4,5,-2])