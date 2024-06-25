from .problems import *

def get_problem(model_type, dimension, output_data, batch_file_path):
    '''
    Generates a problem instance based on the specified model type and configuration.

    Parameters:
    ----------
    model_type : int
        Specifies the type of model to be used. The options are:
        - 1: Crash star box model - Design variables determine the shape and thickness of the star box (up to 5 variables).
        - 2: Three point bending model - Design variables determine the thickness of the reinforcement inner shell (up to 5 variables).
        - 3: Crash tube model - Design variables determine the positions and depths of the three triggers (up to 6 variables).

    dimension : int
        Defines the specific configuration of the model. The allowable ranges and configurations are as follows:
        - For model_type = 1 (Crash star box model):
            - 1: Square
            - 2: Rectangular
            - 3: Rectangular with varying thickness
            - 4: Star shape
            - 5: Star shape with varying thickness
        
        - For model_type = 2 (Three point bending model):
            - 1: All 5 shell thicknesses vary with the same value.
            - 2: Only the first and last shell thicknesses vary; others are fixed at a middle value.
            - 3: The first, middle, and last shell thicknesses vary.
            - 4: All shell thicknesses except the middle vary.
            - 5: All shell thicknesses vary.

        - For model_type = 3 (Crash tube model):
            - 2: Three positions and depths vary together with the same value.
            - 3: All three trigger positions are fixed; the three trigger depths vary.
            - 4: All vary except for the middle trigger position and depth.
            - 5: All vary except for the middle trigger depth.
            - 6: All three positions and depths vary.

    output_data : str
        Specifies the type of output data required. The options are:
        - 'mass'
        - 'absorbed_energy'
        - 'intrusion' (Requires running a simulation; 'mass' and 'absorbed_energy' do not require FEM simulation.)

    batch_file_path : str
        Path to the OpenRadioss batch file.
    '''
    if model_type==1:
        problem_instance = StarBox(dimension, output_data, batch_file_path)
        return problem_instance
    elif model_type==2:
        problem_instance = ThreePointBending(dimension, output_data, batch_file_path)
        return problem_instance
    elif model_type==3:
        problem_instance = CrashTube(dimension, output_data, batch_file_path)
        return problem_instance
    else:
        raise ValueError('Invalid model type')


