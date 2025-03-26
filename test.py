import subprocess
import csv
import random

def generate_dimacs(num_vertices, num_edges):
    """Generate a random DIMACS graph as a string."""
    dimacs = []
    dimacs.append(f"p sp {num_vertices} {num_edges}")
    for _ in range(num_edges):
        u = random.randint(1, num_vertices)
        v = random.randint(1, num_vertices)
        w = random.randint(1, 100)  # Random weight between 1 and 100
        dimacs.append(f"a {u} {v} {w}")
    return "\n".join(dimacs)

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
    num_vertices = 100  # Number of vertices in the graph
    num_edges = 500  # Number of edges in the graph
    source = 1  # Source vertex
    destination = 50  # Destination vertex

    # Generate a random DIMACS graph
    dimacs_input = generate_dimacs(num_vertices, num_edges)

    # Open a CSV file to write the results
    with open("analysis.csv", mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["k", "Result", "Execution Time (s)", "Insert Operations", "DeleteMin Operations", "DecreaseKey Operations"])

        # Test for k values from 1 to 20
        for k in range(1, 21):
            print(f"Running test for k={k}...")
            try:
                output = run_test(k, dimacs_input, source, destination)
                result, execution_time, insert_ops, deletemin_ops, decreasekey_ops = parse_output(output)
                csv_writer.writerow([k, result, execution_time, insert_ops, deletemin_ops, decreasekey_ops])
            except Exception as e:
                print(f"Error for k={k}: {e}")