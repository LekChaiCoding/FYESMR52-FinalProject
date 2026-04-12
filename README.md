# FYESMR52-FinalProject

This project studies the `[4,1,2]` quantum error-detecting code and explores broader quantum error correction ideas with Qiskit.

## What This Repository Is For

The goal of this repository is to keep the project setup simple enough that:

- you can run the Qiskit-based work on this computer without hunting for the right Python environment, and
- other people can set up their own Qiskit environment on Windows or macOS with clear instructions.

## Qiskit Setup

All setup material now lives in `qiskit-setup/`.

- Start here: `qiskit-setup/README.md`
- Windows guide: `qiskit-setup/windows/README.md`
- macOS guide: `qiskit-setup/mac/README.md`
- Verify a setup: `qiskit-setup/verify_qiskit.py`
- Save IBM Quantum cloud credentials: `qiskit-setup/configure_ibm_quantum.py`

## Environment Found On This Computer

A working Conda-based Qiskit environment was found on this machine:

- Conda base: `C:\Users\alexw\Qiskit`
- Recommended environment: `QiskitCode`

This environment successfully runs:

- `qiskit`
- `qiskit-ibm-runtime`

Recommended commands on this computer:

```powershell
conda activate QiskitCode
python qiskit-setup/verify_qiskit.py
python qiskit-setup/verify_qiskit.py --check-cloud
```

If you want to avoid manual activation, this also works:

```powershell
conda run -n QiskitCode python qiskit-setup/verify_qiskit.py
```

## IBM Quantum Cloud

If you want to access IBM Quantum cloud resources instead of only local simulators:

1. Create or sign in to your IBM Quantum account.
2. Copy your API token.
3. Run `python qiskit-setup/configure_ibm_quantum.py`.
4. Verify the connection with `python qiskit-setup/verify_qiskit.py --check-cloud`.
