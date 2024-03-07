import os
import sys

# Define the name of the C code file
c_code_file = "*.c"
GREEN  = '\33[32m'
RED = '\033[31m'
RESET = '\033[0m'
CYAN = '\033[36m'
# Windows needs the -g flag, macos does not
math_lib_flag = sys.platform.startswith('win32') ? '-g' : ''
# Find the path to the tests directory
tests_dir = os.path.join(os.path.dirname(__file__), "tests")
os.chdir(os.path.dirname(__file__))



# Compile the C code
compile_status = os.system(f"gcc -std=c99 -Wall -Werror -pedantic-errors -lm {c_code_file} {math_lib_flag} -o c_code")
if compile_status != 0:
    print("Compilation failed")
    exit()
        
# Loop through all the input files in the tests directory
for input_file in os.listdir(tests_dir):
    if input_file.endswith("_in.txt"):
        test_name = input_file[:-7]
        expected_output_file = test_name + "_out.txt"
        output_file = test_name + "_prog_out.txt"
        input_path = os.path.join(tests_dir, input_file)
        expected_output_path = os.path.join(tests_dir, expected_output_file)
        output_path = os.path.join(tests_dir, output_file)
        

        # Run the C code with the input file and save the output to a file
        command = f"c_code < {input_path} > {output_path}"
        run_status = os.system(command)
        if run_status != 0:
            print(f"{test_name} {RED}failed{RESET}: C code crashed")
            continue
        
        # Compare the expected output and the actual output
        try:
            with open(expected_output_path, "r") as expected_file, open(output_path, "r") as output_file:
                expected_output = expected_file.read()
                actual_output = output_file.read()
                if expected_output == actual_output:
                    print(f"{test_name}{GREEN} passed{RESET}")
                else:
                    print(f"{test_name} {RED}failed{RESET}: expected {expected_output} but got {actual_output}")
        except FileNotFoundError:
            print(f"{test_name} {RED}failed{RESET}: output file not found")
        except:
            print(f"{test_name} {RED}failed{RESET}: something went wrong")

print(CYAN + "** DONE **" +RESET)
