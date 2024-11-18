from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram

"""Two qubit experiments with measurements"""
# Two qubits and two classical bits for measurement
qc1 = QuantumCircuit(2, 2)
# Independent H gates
qc1.h(0)
qc1.h(1)
qc1.measure([0,1], [0,1])  # State after H gates

# Entanglement circuit
qc2 = QuantumCircuit(2, 2)
qc2.h(0)                   # H on first qubit
qc2.cx(0, 1)              # CNOT to entangle
qc2.measure([0,1], [0,1])  # State after entanglement

print("Independent H gates:")
print(qc1.draw())
print("\nEntanglement circuit:")
print(qc2.draw())

simulator = AerSimulator()
result1 = simulator.run(qc1, shots=1000).result()
result2 = simulator.run(qc2, shots=1000).result()

print("Independent qubits results:", result1.get_counts())
print("Entangled qubits results:", result2.get_counts())
