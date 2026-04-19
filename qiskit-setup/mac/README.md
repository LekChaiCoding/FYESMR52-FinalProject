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

For most people using this project, the expected setup is **IBM Quantum Platform**.
That means:

- use your IBM Quantum Platform API token
- keep the default channel behavior from `configure_ibm_quantum.py`
- you usually do **not** need a CRN or instance

1. Sign in to IBM Quantum Platform.
2. Copy your API token from your IBM Quantum account.
3. Run:

```bash
python qiskit-setup/configure_ibm_quantum.py --check
```

4. Confirm cloud access:

```bash
python qiskit-setup/verify_qiskit.py --check-cloud
```

## If Someone Is Using IBM Cloud Instead

Some users may be working from IBM Cloud rather than IBM Quantum Platform. In that case:

- they may need an IBM Cloud API key instead of a plain Quantum Platform token
- they may also need an `instance` value, usually the full Quantum service `CRN`

Use:

```bash
python qiskit-setup/configure_ibm_quantum.py --instance "YOUR_INSTANCE" --check
```

Then verify:

```bash
python qiskit-setup/verify_qiskit.py --check-cloud
```

## Troubleshooting

- If `python3` is not available, try `python3.12` or `python3.11`.
- If package installation fails, upgrade `pip` and rerun the setup script.
- If cloud access fails, confirm whether the user is on IBM Quantum Platform or IBM Cloud, because those credentials are not always interchangeable.
