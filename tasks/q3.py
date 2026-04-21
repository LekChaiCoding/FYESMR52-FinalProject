import sys
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np

try:
    sim = AerSimulator()
    shots = 2000

    # adding the 4 physical qubits 
    code = QuantumRegister(4, 'code')
    #ancilla qubit for stabilizer
    anc = QuantumRegister(1, 'anc')
    #measurement results
    c_anc = ClassicalRegister(1, 'c_anc')
    c_code = ClassicalRegister(4, 'c_code')
    #building the circuits
    qc0 = QuantumCircuit(code, anc, c_anc, c_code)

    #measure the stabilizer
    qc0.h(anc[0])
    #entangles for parity information
    qc0.cx(anc[0], code[0])
    qc0.cx(anc[0], code[1])
    qc0.cx(anc[0], code[2])
    qc0.cx(anc[0], code[3])
    qc0.h(anc[0])
    #measure ancilla to get eigenvalue of +-1
    qc0.measure(anc[0], c_anc[0])
    #measure all 4 physical qubits
    qc0.measure(code[0], c_code[0])
    qc0.measure(code[1], c_code[1])
    qc0.measure(code[2], c_code[2])
    qc0.measure(code[3], c_code[3])

    #runs the circuit
    counts0 = sim.run(qc0, shots=shots).result().get_counts()

    #loop thru outcomes
    #last bit will be ancilla, and first 4 bits will be code qubits
    z_bar_vals = []
    for bitstring, count in counts0.items():
        bits = bitstring.replace(' ', '')
        anc_bit = bits[-1]
        code_bits = bits[:-1]
        
        #only select for those which return '0' --> +1 stabilizer
        if anc_bit == '0':                               
            z = [1 - 2*int(b) for b in code_bits]
            #'0'-> +1 and 1 -> -1
            z_bar = z[2] * z[3]
            #adding more data
            z_bar_vals.extend([z_bar] * count)
    #calculating z bar
    z_bar_mean = np.mean(z_bar_vals)
    #outputs results
    print(f"|0bar> <Z_bar> = {z_bar_mean:.4f} (Shots kept: {len(z_bar_vals)})")

    #2 ancillas for 2 stabilizers
    code2 = QuantumRegister(4, 'code')
    anc2 = QuantumRegister(2, 'anc')
    c_anc2 = ClassicalRegister(2, 'c_anc')
    c_code2 = ClassicalRegister(4, 'c_code')
   
    qcplus = QuantumCircuit(code2, anc2, c_anc2, c_code2)

    #prepare |+>
    qcplus.h(code2[0])
    qcplus.h(code2[1])
    qcplus.h(code2[2])
    qcplus.h(code2[3])
    
    # Stabilizer Z1Z2
    qcplus.h(anc2[0])
    qcplus.cz(anc2[0], code2[0])
    qcplus.cz(anc2[0], code2[1])
    qcplus.h(anc2[0])
    qcplus.measure(anc2[0], c_anc2[0])
    
    # stabilizer Z3Z4
    qcplus.h(anc2[1])
    qcplus.cz(anc2[1], code2[2])
    qcplus.cz(anc2[1], code2[3])
    qcplus.h(anc2[1])
    qcplus.measure(anc2[1], c_anc2[1])

    qcplus.measure(code2[0], c_code2[0])
    qcplus.measure(code2[1], c_code2[1])
    qcplus.measure(code2[2], c_code2[2])
    qcplus.measure(code2[3], c_code2[3])

    countsplus = sim.run(qcplus, shots=shots).result().get_counts()

    x_bar_vals = []
    
    for bitstring, count in countsplus.items():
        bits = bitstring.replace(' ', '')
        #ancillas are the last 2 bits
        anc_bits = bits[-2:]
        code_bits = bits[:-2]

        #both stabilizers need to be +1
        if anc_bits == '00':                             
            x = [1 - 2*int(b) for b in code_bits]
            x_bar = x[0] * x[1] * x[2] * x[3]
            x_bar_vals.extend([x_bar] * count)

    #calculating mean
    x_bar_mean = np.mean(x_bar_vals)
    print(f"|+bar> <X_bar> = {x_bar_mean:.4f} (Shots kept: {len(x_bar_vals)})")

except Exception as e:
    print(f"ERROR: {e}", flush=True)
