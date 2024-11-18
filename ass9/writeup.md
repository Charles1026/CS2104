## Question 1

When you apply 2 H gates in a row, it returns the initial qubit |0> as it is the equivalent of applying the identity matrix. Given 
$H = \frac{1}{\sqrt{2}} \begin{bmatrix}1 & 1 \\ 1 & -1 \end{bmatrix}$, 
$HH = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1  \end{bmatrix} = I$, so $HH|0> = I|0> = |0>$.

When you apply a X gate then a H gate to |0>, it returns $HX|0> = \frac{|0> - |1>}{\sqrt{2}}$. This is because X will flip the qubit so |0> becomes |1> and H will put |1> into a superposition of $\frac{|0> - |1>}{\sqrt{2}}$.

## Question 2
In the first circuit, the 2 qubits are independently put into a superposition with H gates. Hence, when evaluated, all 4 states (00, 01, 10, 11) are possible.

In the second circuit, the first qubit is put in a superposition with a H gate and the second is entangled with the first with a CNOT gate. Thus, the second qubit will always mirror the result of the first and thus only 2 states (00, 11) are possible .

Entanglement in qc2 is done via the CNOT gate, which takes in 2 qubits, the control as the first and the target as the second. After applying H gate to the first qubit, we get $|0>H = \frac{|0> + |1>}{\sqrt{2}}$, which combined with the second qubit gives us $H|0> \bigotimes|0> = \frac{|0> + |1>}{\sqrt{2}} \bigotimes|0> = \frac{|00> + |10>}{\sqrt{2}}$. Hence, $CNOT(\frac{|00> + |10>}{\sqrt{2}}) = \frac{|00> + |11>}{\sqrt{2}}$ since |00> in CNOT does not flip the target bit as the control bit is 0 while |10> flips the target bit as the control bit is 1.

## Question 3
In the first circuit, the 2 qubits are entangled exactly like the second circuit of the previous question, resulting in 2 states (00, 11).

In the second circuit, a second H gate is applied to the first qubit after the same gates as the first circuit. This untangles the 2 bits, resulting in 4 states  (00, 01, 10, 11) being possible.

Starting from the result of the first circuit $\frac{|00> + |11>}{\sqrt{2}}$, we apply a H gate to the first qubit which gives us $\frac{|00> + |11>}{\sqrt{2}} = \frac{H|0> \bigotimes |0> + H|1> \bigotimes |1>}{\sqrt{2}} = \frac{1}{\sqrt{2}}(\frac{|0> + |1>}{\sqrt{2}}\bigotimes |0> + \frac{|0> - |1>}{\sqrt{2}}\bigotimes |1>) = \frac{1}{2}(|00> + |10> + |01> + |11>)$, untangling the 2 qubits.