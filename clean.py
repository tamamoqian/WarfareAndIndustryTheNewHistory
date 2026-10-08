#!/usr/bin/env python3

import shutil
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).parent.resolve()

BUILD_DIR = ROOT / "build"



# ANSI colors

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"



def log(message, level="info"):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    prefix = f"[{timestamp}]"


    if level == "error":

        print(
            f"{RED}{prefix} {message}{RESET}"
        )


    elif level == "success":

        print(
            f"{GREEN}{prefix} {message}{RESET}"
        )


    elif level == "warning":

        print(
            f"{YELLOW}{prefix} {message}{RESET}"
        )


    else:

        print(
            f"{prefix} {message}"
        )



def clean_build():


    log(
        f"Working directory: {ROOT}"
    )


    log(
        f"Checking build directory: {BUILD_DIR}"
    )


    if not BUILD_DIR.exists():


        log(
            "Build directory does not exist",
            "warning"
        )

        return



    try:


        shutil.rmtree(
            BUILD_DIR
        )


        log(
            "Build directory deleted successfully",
            "success"
        )


    except Exception as e:


        log(
            f"Failed to delete build directory: {e}",
            "error"
        )

        raise



def main():


    try:

        clean_build()


    except Exception:

        exit(1)



if __name__ == "__main__":

    main()
