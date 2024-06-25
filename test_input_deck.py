from src import sob

batch_file_path = "D:/OpenRadioss/win_scripts_mk3/openradioss_run_script_ps.bat"

# Generate the first StarBox instance
a = sob.StarBox(3,'a',batch_file_path)
a.generate_input_deck([1,2,3])
# a.run_simulation()

# Generate the second StarBox instance
b = sob.StarBox(2,'a',batch_file_path)
b.generate_input_deck([2,3])
print(b.problem_id)