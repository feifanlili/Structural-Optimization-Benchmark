class OptiProblem():
    def __init__(self, dimension, output_data, batch_file_path) -> None:
        self.dimension = dimension
        self.output_data = output_data
        self.batch_file_path = batch_file_path

        # the attributes need to be overwritten in teh subclass
        self.problem_id = None
        self.variable_ranges = None # constraints of the problem
        self.input_file_name = None # input deck name
        self.output_file_name = None # output result name

class StarBox(OptiProblem):
    def __init__(self, dimension, output_data, batch_file_path) -> None:
        super().__init__(dimension, output_data, batch_file_path)

        # 1 -> square
        # 2 -> rectangular
        # 3 -> rectangular with varying thickness
        # 4 -> star shape
        # 5 -> star shape with varying thickness
        variable_ranges = {
            1: [(60, 120)],
            2: [(60, 120), (60, 120)],
            3: [(60, 120), (60, 120), (0.7, 3)],
            4: [(60, 120), (60, 120), (0, 30), (0, 30)],
            5: [(60, 120), (60, 120), (0, 30), (0, 30), (0.7, 3)]
        }
        self.variable_range = variable_ranges[self.dimension]
        self.input_file_name = 'combine.k'
        self.output_file_name = 'combineT01.csv'

class ThreePointBending(OptiProblem):
    def __init__(self, dimension, output_data, batch_file_path) -> None:
        super().__init__(dimension, output_data, batch_file_path)
        # 1 -> all 5 shell thickness vary with same value. 
        # 2 -> only first and the last shell thickness vary, other fixed with middle value. 
        # 3 -> the first, middle, and last shell thickness vary. 
        # 4 -> expect for middle shell, the other 4 shell thickness vary.
        # 5 -> all three shell thickness vary.
        variable_ranges = {
            1: [(0.5, 3)],
            2: [(0.5, 3)]*2,
            3: [(0.5, 3)]*3,
            4: [(0.5, 3)]*4,
            5: [(0.5, 3)]*5
        }
        self.variable_range = variable_ranges[self.dimension]
        self.input_file_name = 'ThreePointBending_0000.rad'
        self.output_file_name = 'ThreePointBendingT01.csv'

class CrashTube(OptiProblem):
    def __init__(self, dimension, output_data, batch_file_path) -> None:
        super().__init__(dimension, output_data, batch_file_path)
        # 2 -> three positions and depths vary together with same value. 
        # 3 -> all three trigger positions fixed, the three trigger depth vary. 
        # 4 -> except for middle trigger position and depth, other 4 vary ().
        # 5 -> except for middle trigger depth, other 5 vary. 
        # 6 -> all three positions and depths vary.
        variable_ranges = {
            2: [(-10, 10), (-4, 4)],
            3: [(-4, 4)]*3,
            4: [(-10, 10), (-4, 4), (-10, 10), (-4, 4)],
            5: [(-4, 4), (-4, 4), (-4, 4), (-10, 10), (-10, 10)],
            6: [(-4, 4), (-4, 4), (-4, 4), (-10, 10), (-10, 10), (-10, 10)]
        }
        self.variable_range = variable_ranges[self.dimension]
        self.input_file_name = 'combine.k'
        self.output_file_name = 'combineT01.csv'

