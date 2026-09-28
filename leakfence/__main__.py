from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .scanner import scan_directory


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan a repository for likely hard-coded secrets."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Repository directory to scan (default: current directory)",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    print(f"LeakFence scanning: {root}")
    findings = scan_directory(root)

    if findings:
        print(f"\n❌ {len(findings)} potential secret(s) detected\n")
        for finding in findings:
            print(f"  File : {finding.path}")
            print(f"  Line : {finding.line}")
            print(f"  Type : {finding.secret_type}")
            print()
        print("CI pipeline blocked: remove the hard-coded secret and use environment variables or a secret manager.")
        return 1

    print("✅ No potential hard-coded secrets detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
