from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SETUP_DIR = SCRIPT_DIR.parent
REQUIREMENTS_FILE = SETUP_DIR / "requirements-qiskit.txt"
VERIFY_SCRIPT = SETUP_DIR / "verify_qiskit.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a macOS virtual environment for Qiskit."
    )
    parser.add_argument(
        "--python-command",
        default="python3",
        help="Python executable to use, for example python3 or python3.12.",
    )
    parser.add_argument(
        "--venv-path",
        default=str(Path.cwd() / ".venv-qiskit"),
        help="Where to create the virtual environment.",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Do not run the post-install Qiskit verification script.",
    )
    return parser.parse_args()


def ensure_python_exists(python_command: str) -> bool:
    return shutil.which(python_command) is not None


def run_checked(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main() -> int:
    args = parse_args()
    venv_path = Path(args.venv_path).resolve()
    venv_python = venv_path / "bin" / "python"

    if not ensure_python_exists(args.python_command):
        print(f"Could not find '{args.python_command}'.")
        print("Install Python 3.11 or 3.12 first, then rerun this script.")
        return 1

    if not venv_path.exists():
        print(f"Creating virtual environment at: {venv_path}")
        try:
            run_checked([args.python_command, "-m", "venv", str(venv_path)])
        except subprocess.CalledProcessError as exc:  # pragma: no cover
            print("Virtual environment creation failed.")
            return exc.returncode or 1
    else:
        print(f"Using existing virtual environment: {venv_path}")

    try:
        print("Upgrading pip...")
        run_checked([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])

        print("Installing Qiskit packages...")
        run_checked([str(venv_python), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)])
    except subprocess.CalledProcessError as exc:  # pragma: no cover
        print("Package installation failed.")
        return exc.returncode or 1

    print("\nRecommended commands:")
    print(f"  source \"{venv_path}/bin/activate\"")
    print("  python qiskit-setup/verify_qiskit.py")
    print("  python qiskit-setup/configure_ibm_quantum.py --check")

    if args.skip_verify:
        return 0

    try:
        run_checked([str(venv_python), str(VERIFY_SCRIPT)])
    except subprocess.CalledProcessError as exc:  # pragma: no cover
        print("The environment was created, but verification failed.")
        return exc.returncode or 1

    print("\nmacOS Qiskit environment is ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
