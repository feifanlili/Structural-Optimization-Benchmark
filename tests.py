from src import sob
import numpy as np

batch_file_path = "D:/OpenRadioss/win_scripts_mk3/openradioss_run_script_ps.bat"

def generate_multiple_instances():
    # Generate the first StarBox instance
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