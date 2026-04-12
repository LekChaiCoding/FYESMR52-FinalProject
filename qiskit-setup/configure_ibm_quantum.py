from __future__ import annotations

import argparse
import getpass
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Save IBM Quantum credentials for qiskit-ibm-runtime."
    )
    parser.add_argument(
        "--token",
        help="IBM Quantum or IBM Cloud API token. If omitted, you will be prompted.",
    )
    parser.add_argument(
        "--channel",
        choices=["ibm_quantum_platform", "ibm_cloud", "local"],
        default="ibm_quantum_platform",
        help="Runtime channel to save.",
    )
    parser.add_argument(
        "--instance",
        help="Optional instance, service name, or CRN if your account requires one.",
    )
    parser.add_argument(
        "--url",
        help="Optional custom API URL. Leave blank to use the package default.",
    )
    parser.add_argument(
        "--name",
        default="default",
        help="Saved account name.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite an existing saved account with the same name.",
    )
    parser.add_argument(
        "--set-as-default",
        action="store_true",
        help="Mark this saved account as the default runtime account.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Try a quick connection check after saving the account.",
    )
    return parser.parse_args()


def prompt_for_token(token: str | None) -> str:
    if token:
        return token.strip()

    entered = getpass.getpass("Paste your IBM Quantum token and press Enter: ").strip()
    if not entered:
        raise ValueError("A token is required.")
    return entered


def main() -> int:
    args = parse_args()

    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
    except Exception as exc:  # pragma: no cover - script-level troubleshooting
        print("qiskit-ibm-runtime is not available in this environment.")
        print(f"Reason: {exc}")
        return 1

    try:
        token = prompt_for_token(args.token)
    except ValueError as exc:
        print(str(exc))
        return 1

    save_kwargs = {
        "token": token,
        "channel": args.channel,
        "overwrite": args.overwrite,
        "name": args.name,
    }

    if args.instance:
        save_kwargs["instance"] = args.instance
    if args.url:
        save_kwargs["url"] = args.url
    if args.set_as_default:
        save_kwargs["set_as_default"] = True

    try:
        QiskitRuntimeService.save_account(**save_kwargs)
    except Exception as exc:  # pragma: no cover - script-level troubleshooting
        print("Account could not be saved.")
        print(f"Reason: {exc}")
        return 1

    print("IBM Quantum account details were saved successfully.")
    print(f"Saved account name: {args.name}")
    print(f"Saved channel: {args.channel}")

    if not args.check:
        print("Next step: run python qiskit-setup/verify_qiskit.py --check-cloud")
        return 0

    try:
        service = QiskitRuntimeService(name=args.name)
        backend_count = len(service.backends())
    except Exception as exc:  # pragma: no cover - script-level troubleshooting
        print("The account was saved, but the follow-up cloud check failed.")
        print(f"Reason: {exc}")
        return 1

    print(f"Cloud check passed. Backends visible: {backend_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
