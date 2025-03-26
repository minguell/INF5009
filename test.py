import subprocess
import csv
import time

def read_dimacs(file_path):
    """Read a DIMACS graph from a file."""
    with open(file_path, "r") as file:
        return file.read()

def run_test(k, dimacs_input, source, destination):
    """Run dijkstra.py with the given k and DIMACS input."""
    process = subprocess.Popen(
        ["python", "dijkstra.py", str(source), str(destination), str(k)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=dimacs_input)
    if process.returncode != 0:
        raise RuntimeError(f"Error running dijkstra.py: {stderr}")
    return stdout

def parse_output(output):
    """Parse the output of dijkstra.py to extract metrics."""
    lines = output.strip().split("\n")
    result = lines[0].split(": ")[1]
    execution_time = float(lines[1].split(": ")[1].split()[0])
    insert_operations = int(lines[2].split(": ")[1])
    deletemin_operations = int(lines[3].split(": ")[1])
    decreasekey_operations = int(lines[4].split(": ")[1])
    return result, execution_time, insert_operations, deletemin_operations, decreasekey_operations

if __name__ == "__main__":
    graph_file = "USA-road-d.NY.gr"  # Path to the DIMACS graph file
    source = 1  # Source vertex
    num_tests = 30  # Number of tests to run

    # Read the DIMACS graph from the file
    dimacs_input = read_dimacs(graph_file)

    # Open a CSV file to write the results
    with open("analysis.csv", mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["k", "Destination", "Result", "Execution Time (s)", "Insert Operations", "DeleteMin Operations", "DecreaseKey Operations"])

        # Test for k values from 1 to num_tests
        for k in range(1, num_tests + 1):
            destination = k  # Set destination to the current value of k
            print(f"Running test for k={k}, destination={destination}...")
            try:
                # Measure execution time with high precision
                start_time = time.perf_counter()
                output = run_test(k, dimacs_input, source, destination)
                end_time = time.perf_counter()
                execution_time = end_time - start_time

                # Parse the output and write to CSV
                result, _, insert_ops, deletemin_ops, decreasekey_ops = parse_output(output)
                csv_writer.writerow([k, destination, result, f"{execution_time:.6f}", insert_ops, deletemin_ops, decreasekey_ops])
            except Exception as e:
                print(f"Error for k={k}, destination={destination}: {e}")