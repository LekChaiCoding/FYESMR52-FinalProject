from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np

sim = AerSimulator()
shots = 4000

#MX(prep) → [MX + MZ](M=1 cycle) → MZ(final)

code    = QuantumRegister(4, 'code')
anc_px  = QuantumRegister(1, 'anc_px')
anc_cx  = QuantumRegister(1, 'anc_cx') 
anc_cz  = QuantumRegister(2, 'anc_cz')   

c_px    = ClassicalRegister(1, 'c_px')  
c_cx    = ClassicalRegister(1, 'c_cx') 
c_cz    = ClassicalRegister(2, 'c_cz') 
c_code  = ClassicalRegister(4, 'c_code') # final readout

qc0 = QuantumCircuit(code, anc_px, anc_cx, anc_cz, c_px, c_cx, c_cz, c_code)

#MX = measure X1X2X3X4
qc0.h(anc_px[0])
qc0.cx(anc_px[0], code[0])
qc0.cx(anc_px[0], code[1])
qc0.cx(anc_px[0], code[2])
qc0.cx(anc_px[0], code[3])
qc0.h(anc_px[0])
qc0.measure(anc_px[0], c_px[0])

# M=1 CYCLE: MX (X1X2X3X4)
qc0.reset(anc_cx[0])
qc0.h(anc_cx[0])
qc0.cx(anc_cx[0], code[0])
qc0.cx(anc_cx[0], code[1])
qc0.cx(anc_cx[0], code[2])
qc0.cx(anc_cx[0], code[3])
qc0.h(anc_cx[0])
qc0.measure(anc_cx[0], c_cx[0])


qc0.reset(anc_cz[0])
qc0.cx(code[0], anc_cz[0])  
qc0.cx(code[1], anc_cz[0])
qc0.measure(anc_cz[0], c_cz[0])

# z3z4
qc0.reset(anc_cz[1])
qc0.cx(code[2], anc_cz[1])
qc0.cx(code[3], anc_cz[1])
qc0.measure(anc_cz[1], c_cz[1])

qc0.measure(code[0], c_code[0])
qc0.measure(code[1], c_code[1])
qc0.measure(code[2], c_code[2])
qc0.measure(code[3], c_code[3])

counts0 = sim.run(qc0, shots=shots).result().get_counts()

z_bar_vals = []
for bitstring, count in counts0.items():
    bits = bitstring.replace(' ', '')

    #separating the prep MX, cycle MX, cycle MZ
    #then read out z3z4, z1z2 and the qubit readout
    px_bit   = bits[-1]        
    cx_bit   = bits[-2]        
    cz_bits  = bits[-4:-2]     
    code_bits = bits[:-4]      

  
    z = [1 - 2*int(b) for b in reversed(code_bits)]  
    final_z12 = z[0] * z[1]   # z1z2 from final readout
    final_z34 = z[2] * z[3]   # Z3Z4

#post selection
    if (px_bit == '0' and cx_bit == '0' and cz_bits == '00'
            and final_z12 == 1 and final_z34 == 1):
        z_bar = z[1] * z[2]   # Z_bar = Z2Z3
        z_bar_vals.extend([z_bar] * count)

z_bar_mean = np.mean(z_bar_vals)
print(f"|0bar> M=1  <Z_bar> = {z_bar_mean:.4f}  (Shots kept: {len(z_bar_vals)})")



code2   = QuantumRegister(4, 'code')
anc_pz2 = QuantumRegister(2, 'anc_pz')   
anc_cz2 = QuantumRegister(2, 'anc_cz')  
anc_cx2 = QuantumRegister(1, 'anc_cx')  

c_pz2   = ClassicalRegister(2, 'c_pz')
c_cz2   = ClassicalRegister(2, 'c_cz')
c_cx2   = ClassicalRegister(1, 'c_cx')
c_code2 = ClassicalRegister(4, 'c_code')

qcplus = QuantumCircuit(code2, anc_pz2, anc_cz2, anc_cx2,
                        c_pz2, c_cz2, c_cx2, c_code2)

for i in range(4):
    qcplus.h(code2[i])

qcplus.h(anc_pz2[0])
qcplus.cz(anc_pz2[0], code2[0])
qcplus.cz(anc_pz2[0], code2[1])
qcplus.h(anc_pz2[0])
qcplus.measure(anc_pz2[0], c_pz2[0])

qcplus.h(anc_pz2[1])
qcplus.cz(anc_pz2[1], code2[2])
qcplus.cz(anc_pz2[1], code2[3])
qcplus.h(anc_pz2[1])
qcplus.measure(anc_pz2[1], c_pz2[1])

qcplus.reset(anc_cz2[0])
qcplus.h(anc_cz2[0])
qcplus.cz(anc_cz2[0], code2[0])
qcplus.cz(anc_cz2[0], code2[1])
qcplus.h(anc_cz2[0])
qcplus.measure(anc_cz2[0], c_cz2[0])

qcplus.reset(anc_cz2[1])
qcplus.h(anc_cz2[1])
qcplus.cz(anc_cz2[1], code2[2])
qcplus.cz(anc_cz2[1], code2[3])
qcplus.h(anc_cz2[1])
qcplus.measure(anc_cz2[1], c_cz2[1])

qcplus.reset(anc_cx2[0])
qcplus.h(anc_cx2[0])
qcplus.cx(anc_cx2[0], code2[0])
qcplus.cx(anc_cx2[0], code2[1])
qcplus.cx(anc_cx2[0], code2[2])
qcplus.cx(anc_cx2[0], code2[3])
qcplus.h(anc_cx2[0])
qcplus.measure(anc_cx2[0], c_cx2[0])

for i in range(4):
    qcplus.h(code2[i])
qcplus.measure(code2[0], c_code2[0])
qcplus.measure(code2[1], c_code2[1])
qcplus.measure(code2[2], c_code2[2])
qcplus.measure(code2[3], c_code2[3])

countsplus = sim.run(qcplus, shots=shots).result().get_counts()

x_bar_vals = []
for bitstring, count in countsplus.items():
    bits = bitstring.replace(' ', '')

    pz_bits  = bits[-2:]  
    cz_bits  = bits[-4:-2]     
    cx_bit   = bits[-5]    
    code_bits = bits[:-5]   

    x = [1 - 2*int(b) for b in reversed(code_bits)] 


    final_xxxx = x[0] * x[1] * x[2] * x[3]

    if (pz_bits == '00' and cz_bits == '00' and cx_bit == '0'
            and final_xxxx == 1):
        x_bar = x[0] * x[1] 
        x_bar_vals.extend([x_bar] * count)

x_bar_mean = np.mean(x_bar_vals)
print(f"|+bar> M=1  <X_bar> = {x_bar_mean:.4f}  (Shots kept: {len(x_bar_vals)})")
