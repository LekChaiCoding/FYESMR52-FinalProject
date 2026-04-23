from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

print("starting...")

try:
    sim = AerSimulator()
    shots = 2000

    code = QuantumRegister(4, 'code')
    anc = QuantumRegister(1, 'anc')
    c = ClassicalRegister(1, 'c')
    qc0 = QuantumCircuit(code, anc, c)

    qc0.h(anc[0])
    qc0.cx(anc[0], code[0])
    qc0.cx(anc[0], code[1])
    qc0.cx(anc[0], code[2])
    qc0.cx(anc[0], code[3])
    qc0.h(anc[0])
    qc0.measure(anc[0], c[0])

    counts0 = sim.run(qc0, shots=shots).result().get_counts()
    success_0 = counts0.get('0', 0)
    print(f"|0bar> success rate: {success_0/shots:.2%}  (theory: 50%)")
    print(f"Raw counts: {counts0}")

    code2 = QuantumRegister(4, 'code')
    anc2 = QuantumRegister(2, 'anc')
    c2 = ClassicalRegister(2, 'c')
    qcplus = QuantumCircuit(code2, anc2, c2)

    qcplus.h(code2[0])
    qcplus.h(code2[1])
    qcplus.h(code2[2])
    qcplus.h(code2[3])

    qcplus.h(anc2[0])
    qcplus.cz(anc2[0], code2[0])
    qcplus.cz(anc2[0], code2[1])
    qcplus.h(anc2[0])
    qcplus.measure(anc2[0], c2[0])

    qcplus.h(anc2[1])
    qcplus.cz(anc2[1], code2[2])
    qcplus.cz(anc2[1], code2[3])
    qcplus.h(anc2[1])
    qcplus.measure(anc2[1], c2[1])

    countsplus = sim.run(qcplus, shots=shots).result().get_counts()
    success_plus = countsplus.get('00', 0)
    print(f"\n|+bar> success rate: {success_plus/shots:.2%}  (theory: 25%)")
    print(f"Raw counts: {countsplus}")

except Exception as e:
    print(f"ERROR: {e}")




    