from __future__ import annotations

import argparse
import sys


def print_header(title: str) -> None:
    print(f"\n=== {title} ===")


def verify_local_stack() -> int:
    print_header("Local Qiskit Stack")

    try:
        import qiskit
        from qiskit import QuantumCircuit, transpile
        from qiskit_aer import AerSimulator
    except Exception as exc:  # pragma: no cover - script-level troubleshooting
        print("Qiskit import failed.")
        print(f"Reason: {exc}")
        print("Tip: activate your Qiskit environment first, then rerun this script.")
        return 1

    print(f"qiskit version: {qiskit.__version__}")

    try:
        import qiskit_aer

        print(f"qiskit-aer version: {qiskit_aer.__version__}")
    except Exception as exc:  # pragma: no cover - script-level troubleshooting
        print("qiskit-aer import failed.")
        print(f"Reason: {exc}")
        return 1

    try:
        import qiskit_ibm_runtime

        print(f"qiskit-ibm-runtime version: {qiskit_ibm_runtime.__version__}")
    except Exception as exc:  # pragma: no cover - script-level troubleshooting
        print("qiskit-ibm-runtime import failed.")
        print(f"Reason: {exc}")
        print("Local simulation may still work, but cloud access will not.")
        return 1

    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])

    simulator = AerSimulator()
    compiled = transpile(circuit, simulator)
    result = simulator.run(compiled, shots=256).result()
    counts = dict(sorted(result.get_counts().items()))

    print("Local simulator test passed.")
    print(f"Bell-state sample counts: {counts}")
    return 0


def verify_cloud_access() -> int:
    print_header("IBM Quantum Cloud")

    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
    except Exception as exc:  # pragma: no cover - script-level troubleshooting
        print("Cloud verification could not start.")
        print(f"Reason: {exc}")
        return 1

    try:
        service = QiskitRuntimeService()
        backends = service.backends()
        backend_names = sorted(backend.name for backend in backends)
    except Exception as exc:  # pragma: no cover - script-level troubleshooting
        print("No working IBM Quantum cloud account was found.")
        print(f"Reason: {exc}")
        print("Run qiskit-setup/configure_ibm_quantum.py and try again.")
        return 1

    preview = ", ".join(backend_names[:5]) if backend_names else "No backends returned"
    print("Cloud account check passed.")
    print(f"Backends found: {len(backend_names)}")
    print(f"Sample backends: {preview}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify local Qiskit packages and optional IBM Quantum cloud access."
    )
    parser.add_argument(
        "--check-cloud",
        action="store_true",
        help="Also verify that an IBM Quantum account is configured and reachable.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    exit_code = verify_local_stack()
    if exit_code != 0:
        return exit_code

    if args.check_cloud:
        return verify_cloud_access()

    print("\nVerification complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
