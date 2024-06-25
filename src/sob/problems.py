import os
from .solver import run_radioss
from .mesh import StarBoxMesh
from .fem import StarBoxModel

class OptiProblem():
    '''
    The abstract of the structural optimization problem, with three subclass (three problem type)
    The instance is initialized by problem dimension, output data type, and the batch file path of the solver OpenRadioss. 
    The core idea is to generate a specific type of instance, input the variable array then output the evaluation of the desired data type like mass, intrusion, etc.
    The input variables should be in an universal search space, default (-5,5). For the evaluation those variables will be mapped to the real FEM problem space.
    '''
    def __init__(self, dimension, output_data, batch_file_path) -> None:
        self.dimension = dimension
        self.output_data = output_data
        self.batch_file_path = batch_file_path

        # the attributes need to be overwritten in teh subclass
        self.problem_id = None
        self.variable_ranges = None # constraints of the problem
        self.input_file_name = None # input deck name
        self.output_file_name = None # output result name

        self.search_space = (-5.0, 5.0)

    def _validate_variable_array(self, variable_array):
        """
        Validate the variable array against the search space.

        Parameters:
            variable_array (list): The array of variables to be validated.

        Raises:
            ValueError: If the size of the variable array does not match the problem dimension or if any variable is out of range.
        """
        if self.variable_ranges is None:
            raise ValueError("variable_ranges must be provided or defined in the subclass.")
        
        if len(variable_array) != self.dimension:
            raise ValueError('The size of variable array does not match the problem dimension')

        for i, (value, (lower, upper)) in enumerate(zip(variable_array, [self.search_space]*self.dimension)):
            if not (lower <= value <= upper):
                raise ValueError(f"Value at position {i} in variable_array is out of range: {value}. " f"Allowed range is [{lower}, {upper}].")
    
    def linear_maping_variable(self, search_space_variable, problem_space_range:tuple):
        """
        Map a variable from the search space to the problem space for use in FEM simulation.

        Parameters:
            search_space_variable (float): Variable in the search space (for optimization).
            problem_space_range (tuple): Range of variables in the problem space (for FEM simulation).

        Returns:
            float: Variable mapped to the problem space.
        """
        lower = problem_space_range[0]
        upper = problem_space_range[1]
        scale = (upper-lower)/(self.search_space[1]-self.search_space[0])
        problem_space_variable = lower + (search_space_variable-self.search_space[0])*scale
        return problem_space_variable

    def generate_input_deck(self, variable_array):
        self._validate_variable_array(variable_array)

        fem_space_variable_array = [] # to get the variables in the FEM space
        for i, var in enumerate(variable_array):
            mapped_var = self.linear_maping_variable(var, self.variable_ranges[i])
            fem_space_variable_array.append(mapped_var)

        original_dir = os.getcwd()
        dir_name = f'{self.__class__.__name__.lower()}_deck{self.problem_id}'
        working_dir = os.path.join(os.getcwd(), dir_name)
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
        os.chdir(working_dir)
        self._write_input_file(fem_space_variable_array)
        os.chdir(original_dir)
        

    def _write_input_file(self, fem_space_variable_array):
        raise NotImplementedError("Subclasses must implement _write_input_file method")
    
    def run_simulation(self):
        if self.input_file_name is None:
            raise ValueError("input_file_name must be provided or defined in the subclass.")

        dir_name = f'{self.__class__.__name__.lower()}_deck{self.problem_id}'
        working_dir = os.path.join(os.getcwd(), dir_name)
        input_file_path = os.path.join(working_dir, self.input_file_name)
        run_radioss(input_file_path, self.batch_file_path)

    def __call__(self, variable_array):
        pass
        


class StarBox(OptiProblem):
    instance_counter = 1
    def __init__(self, dimension, output_data, batch_file_path) -> None:
        super().__init__(dimension, output_data, batch_file_path)
        # 1 -> square
        # 2 -> rectangular
        # 3 -> rectangular with varying thickness
        # 4 -> star shape
        # 5 -> star shape with varying thickness
        variable_ranges_map = {
            1: [(60, 120)],
            2: [(60, 120), (60, 120)],
            3: [(60, 120), (60, 120), (0.7, 3)],
            4: [(60, 120), (60, 120), (0, 30), (0, 30)],
            5: [(60, 120), (60, 120), (0, 30), (0, 30), (0.7, 3)]
        }
        self.variable_ranges = variable_ranges_map[self.dimension]
        self.input_file_name = 'combine.k'
        self.output_file_name = 'combineT01.csv'

        self.problem_id = StarBox.instance_counter
        StarBox.instance_counter+=1

    def _write_input_file(self, fem_space_variable_array):
        mesh = StarBoxMesh(fem_space_variable_array) 
        model = StarBoxModel(mesh)
        model.write_input_files()
    

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

