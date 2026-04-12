# macOS Qiskit Setup

This guide is for someone setting up Qiskit on a Mac.

## Fresh macOS Setup

1. Make sure Python 3.11 or 3.12 is installed.
2. Open Terminal.
3. From the repository root, run:

```bash
python3 qiskit-setup/mac/setup_qiskit_mac.py
```

4. Activate the virtual environment:

```bash
source .venv-qiskit/bin/activate
```

5. Verify the installation:

```bash
python qiskit-setup/verify_qiskit.py
```

## IBM Quantum Cloud Setup

After the local environment works:

1. Sign in to IBM Quantum.
2. Copy your API token.
3. Run:

```bash
python qiskit-setup/configure_ibm_quantum.py --check
```

4. If your account needs an instance or CRN:

```bash
python qiskit-setup/configure_ibm_quantum.py --instance "YOUR_INSTANCE" --check
```

5. Confirm cloud access:

```bash
python qiskit-setup/verify_qiskit.py --check-cloud
```

## Troubleshooting

- If `python3` is not available, try `python3.12` or `python3.11`.
- If package installation fails, upgrade `pip` and rerun the setup script.
- If cloud access fails, confirm that the saved token matches the account you expect to use.
