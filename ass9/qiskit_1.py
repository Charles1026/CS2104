from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram

"""Two H gates and H on |1⟩"""
# two H gates in series with measurement
qc1 = QuantumCircuit(1, 1)
qc1.h(0)          # First H
qc1.h(0)          # Second H
qc1.measure(0, 0)  # After second H

# H on |1⟩ with measurement
qc2 = QuantumCircuit(1, 1)
qc2.x(0)          # Flip to |1⟩
qc2.h(0)          # Apply H
qc2.measure(0, 0)  # After H

print("Double H circuit:")
print(qc1.draw())
print("\nH on |1⟩ circuit:")
print(qc2.draw())

simulator = AerSimulator()
result1 = simulator.run(qc1, shots=1000).result()
result2 = simulator.run(qc2, shots=1000).result()

print("Double H results:", result1.get_counts())
print("H on |1⟩ results:", result2.get_counts())
