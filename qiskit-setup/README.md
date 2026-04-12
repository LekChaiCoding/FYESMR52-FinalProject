# Qiskit Setup Guide

This folder helps two different groups of people:

- people working on this project on **this computer**, where a Qiskit Conda environment already exists, and
- people setting up **their own** Qiskit environment on Windows or macOS.

## Best Option On This Computer

The Qiskit environment already found and verified on this machine is:

- Conda base: `C:\Users\alexw\Qiskit`
- Environment name: `QiskitCode`

Use it like this:

```powershell
conda activate QiskitCode
python qiskit-setup/verify_qiskit.py
```

If you do not want to manually activate Conda first:

```powershell
conda run -n QiskitCode python qiskit-setup/verify_qiskit.py
```

## Files In This Folder

- `requirements-qiskit.txt`: the core packages for a fresh Qiskit setup
- `verify_qiskit.py`: checks that Qiskit, Aer, and optional cloud access are working
- `configure_ibm_quantum.py`: saves IBM Quantum credentials for `qiskit-ibm-runtime`
- `windows/setup_qiskit_windows.py`: creates or reuses a Windows Conda-based Qiskit environment
- `windows/README.md`: Windows instructions
- `mac/setup_qiskit_mac.py`: creates a macOS virtual environment and installs Qiskit
- `mac/README.md`: macOS instructions

## IBM Quantum Cloud Setup

To use real IBM Quantum cloud resources instead of only local simulators:

1. Create or sign in to your IBM Quantum account.
2. Copy your API token.
3. Activate your Qiskit environment.
4. Run:

```bash
python qiskit-setup/configure_ibm_quantum.py --check
```

5. If your account also requires an instance or CRN, rerun with:

```bash
python qiskit-setup/configure_ibm_quantum.py --instance "YOUR_INSTANCE" --check
```

6. Confirm everything works:

```bash
python qiskit-setup/verify_qiskit.py --check-cloud
```

## Which OS Guide To Follow

- If you are on Windows, use `qiskit-setup/windows/README.md`
- If you are on macOS, use `qiskit-setup/mac/README.md`
