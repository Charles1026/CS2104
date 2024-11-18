from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

"""Setup: Single H gate with measurement"""
# We need one classical bit to store the measurement
qc = QuantumCircuit(1, 1)

# Initial state measurement
qc.h(0)          # Apply H gate
qc.measure(0, 0)  # Measure after H

print("Circuit:")
print(qc.draw())

simulator = AerSimulator()
result = simulator.run(qc, shots=1000).result()
counts = result.get_counts()

print("Results (first bit: after H):", counts)
