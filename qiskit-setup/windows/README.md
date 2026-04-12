# Windows Qiskit Setup

This guide is for someone setting up Qiskit on a Windows machine.

## Best Choice For This Repository On This Computer

A usable Conda environment already exists here:

- Conda base: `C:\Users\alexw\Qiskit`
- Environment name: `QiskitCode`

Use it with:

```powershell
conda activate QiskitCode
python qiskit-setup/verify_qiskit.py
```

Or without manually activating:

```powershell
conda run -n QiskitCode python qiskit-setup/verify_qiskit.py
```

## Fresh Windows Setup For Someone Else

If you do not already have a Qiskit environment:

1. Install Miniconda or Anaconda.
2. Open PowerShell.
3. From the repository root, run:

```powershell
python qiskit-setup/windows/setup_qiskit_windows.py --env-name qiskit
```

4. Activate the environment:

```powershell
conda activate qiskit
```

5. Verify the installation:

```powershell
python qiskit-setup/verify_qiskit.py
```

## IBM Quantum Cloud Setup

After the local environment works:

1. Sign in to IBM Quantum.
2. Copy your API token.
3. Run:

```powershell
python qiskit-setup/configure_ibm_quantum.py --check
```

4. If your account needs an instance or CRN:

```powershell
python qiskit-setup/configure_ibm_quantum.py --instance "YOUR_INSTANCE" --check
```

5. Confirm cloud access:

```powershell
python qiskit-setup/verify_qiskit.py --check-cloud
```

## Troubleshooting

- If `python` points to the wrong interpreter, use `conda run -n qiskit ...` instead of plain `python`.
- If Conda is not recognized, reopen PowerShell after installing Miniconda or Anaconda.
- If cloud access fails, confirm that your token is valid and that your account has access to the requested instance.
