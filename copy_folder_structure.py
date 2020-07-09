import os
import argparse

if __name__ == '__main__':
    """This function helps us in copy a directory structure to another directory.
    """

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Copy The Folder Structure')
    
    parser.add_argument('--input', required=True,
                        help='Input Directory Path')
    parser.add_argument('--output', required=True,
                        help='Output Directory Path')
    
    args = parser.parse_args()
    
    # saves the command line arguments to the variable
    input_path = args.input
    output_path = args.output

    # walk through the input path directory
    for dirpath, dirnames, filenames in os.walk(input_path):

        # replace the parent path with the output directory path
        structure = os.path.join(output_path, dirpath[len(input_path):])
        if not os.path.isdir(structure):
            os.mkdir(structure)
        else:
            print("Folder does already exits!") 
