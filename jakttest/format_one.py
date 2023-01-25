import argparse
import os
import subprocess
import sys
from pathlib import Path


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Run a single test")
    parser.add_argument("temp_dir", help="Temporary directory to use")
    parser.add_argument("test_file", help="The test file to run")
    parser.add_argument(
        "--jakt-binary", help="The path to the jakt binary", default="build/bin/jakt"
    )
    args = parser.parse_args()

    # Since we're running the output binary from a different
    # working directory, we need the full path of the binary.
    temp_dir = Path(args.temp_dir).resolve()
    test_file = Path(args.test_file).resolve()
    jakt_binary = Path(args.jakt_binary).resolve()

    # clear the temp directory
    for f in os.listdir(temp_dir):
        os.remove(temp_dir / f)

    with open(temp_dir / "runtest.out", "w") as stdout, open(
        temp_dir / "runtest.err", "w"
    ) as stderr:
        try:
            subprocess.run(
                [jakt_binary, "-f", test_file],
                check=True,
                stdout=stdout,
                stderr=stderr,
                cwd=test_file.parent,
            )
        except subprocess.CalledProcessError:
            sys.exit(1)


if __name__ == "__main__":
    main()
