from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SETUP_DIR = SCRIPT_DIR.parent
REQUIREMENTS_FILE = SETUP_DIR / "requirements-qiskit.txt"
VERIFY_SCRIPT = SETUP_DIR / "verify_qiskit.py"


def run_command(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, text=True, capture_output=True)


def get_conda_command() -> str | None:
    return shutil.which("conda")


def list_conda_envs(conda_cmd: str) -> list[str]:
    result = run_command([conda_cmd, "env", "list", "--json"])
    payload = json.loads(result.stdout)
    env_paths = payload.get("envs", [])
    return [Path(path).name for path in env_paths]


def create_env(conda_cmd: str, env_name: str, python_version: str) -> None:
    print(f"Creating Conda environment '{env_name}' with Python {python_version}...")
    subprocess.run(
        [conda_cmd, "create", "-y", "-n", env_name, f"python={python_version}"],
        check=True,
    )


def install_packages(conda_cmd: str, env_name: str) -> None:
    print("Installing Qiskit packages...")
    subprocess.run(
        [
            conda_cmd,
            "run",
            "-n",
            env_name,
            "python",
            "-m",
            "pip",
            "install",
            "-r",
            str(REQUIREMENTS_FILE),
        ],
        check=True,
    )


def verify_env(conda_cmd: str, env_name: str) -> None:
    print("Running Qiskit verification...")
    subprocess.run(
        [
            conda_cmd,
            "run",
            "-n",
            env_name,
            "python",
            str(VERIFY_SCRIPT),
        ],
        check=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create or reuse a Windows Conda-based Qiskit environment."
    )
    parser.add_argument(
        "--env-name",
        default="qiskit",
        help="Conda environment name to create or reuse.",
    )
    parser.add_argument(
        "--python-version",
        default="3.12",
        help="Python version to use for a newly created environment.",
    )
    parser.add_argument(
        "--use-existing-only",
        action="store_true",
        help="Fail instead of creating the environment if it does not already exist.",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Do not run the post-install Qiskit verification script.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    conda_cmd = get_conda_command()

    if not conda_cmd:
        print("Conda was not found on PATH.")
        print("Install Miniconda or Anaconda first, then rerun this script.")
        return 1

    try:
        env_names = list_conda_envs(conda_cmd)
    except Exception as exc:  # pragma: no cover - script-level troubleshooting
        print("Could not list Conda environments.")
        print(f"Reason: {exc}")
        return 1

    env_exists = args.env_name in env_names

    if env_exists:
        print(f"Found existing environment: {args.env_name}")
    elif args.use_existing_only:
        print(f"Environment '{args.env_name}' does not exist.")
        return 1
    else:
        try:
            create_env(conda_cmd, args.env_name, args.python_version)
            install_packages(conda_cmd, args.env_name)
        except subprocess.CalledProcessError as exc:  # pragma: no cover
            print("Environment creation failed.")
            print(f"Command: {' '.join(exc.cmd)}")
            return exc.returncode or 1

    print("\nRecommended commands:")
    print(f"  conda activate {args.env_name}")
    print("  python qiskit-setup/verify_qiskit.py")
    print("  python qiskit-setup/configure_ibm_quantum.py --check")

    if args.skip_verify:
        return 0

    try:
        verify_env(conda_cmd, args.env_name)
    except subprocess.CalledProcessError as exc:  # pragma: no cover
        print("The environment exists, but verification failed.")
        return exc.returncode or 1

    print("\nWindows Qiskit environment is ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
