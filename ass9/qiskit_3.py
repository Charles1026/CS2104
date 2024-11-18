from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram

# Bell state without extra H
qc1 = QuantumCircuit(2, 2)
qc1.h(0)          
qc1.cx(0, 1)  
qc1.measure([0,1], [0,1])
print("Bell state without extra H:")
print(qc1.draw())

# Bell state with extra H
qc2 = QuantumCircuit(2, 2)
qc2.h(0)  
qc2.cx(0, 1)  
qc2.h(0)      # Extra H gate
qc2.measure([0,1], [0,1])
print("Bell state with extra H:")
print(qc2.draw())

simulator = AerSimulator()
result1 = simulator.run(qc1, shots=1000).result()
result2 = simulator.run(qc2, shots=1000).result()

print("Bell state without extra H:", result1.get_counts())
print("Bell state with extra H:", result2.get_counts())
