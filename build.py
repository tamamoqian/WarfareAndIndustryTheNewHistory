#!/usr/bin/env python3

import zipfile
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).parent.resolve()

BUILD_DIR = ROOT / "build"


TARGET_FILES = [
    "assets",
    "lib",
    "res",
    "all-units.template",
    "icon.png",
    "mod-info.txt"
]


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


def load_build_config():

    info = {}

    path = ROOT / "build.conf"

    log(
        f"Reading file: {path}"
    )

    if not path.exists():

        log(
            "build.conf not found, creating default configuration",
            "warning"
        )

        path.write_text(
            "build_name:template\n"
            "build_version:1\n",
            encoding="utf-8"
        )

        log(
            f"Created default configuration: {path}",
            "success"
        )

    for line in path.read_text(
        encoding="utf-8"
    ).splitlines():

        line = line.strip()

        if "=" in line:

            key, value = line.split(
                "=",
                1
            )

            info[key.strip()] = value.strip()



    if "build_name" not in info:

        log(
            "build_name not found in build.conf",
            "warning"
        )

        info["build_name"] = "template"


    if "build_version" not in info:

        log(
            "build_version not found in build.conf",
            "warning"
        )

        info["build_version"] = "1"



    build_name = info["build_name"]
    build_version = info["build_version"]


    # Characters forbidden or problematic in common file systems
    invalid_chars = '<>:"/\\|?*'


    if any(
        char in build_name
        for char in invalid_chars
    ):

        log(
            f"build_name contains invalid filename characters: {build_name}",
            "warning"
        )


    if any(
        char in build_version
        for char in invalid_chars
    ):

        log(
            f"build_version contains invalid filename characters: {build_version}",
            "warning"
        )


    # Windows reserved device names
    reserved_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9"
    }


    if build_name.upper() in reserved_names:

        log(
            f"build_name is a reserved filename: {build_name}",
            "warning"
        )


    if build_version.upper() in reserved_names:

        log(
            f"build_version is a reserved filename: {build_version}",
            "warning"
        )


    # Windows does not allow filenames ending with
    # a space or a period.
    if build_name.endswith(
        (" ", ".")
    ):

        log(
            f"build_name ends with an invalid character: {build_name}",
            "warning"
        )


    if build_version.endswith(
        (" ", ".")
    ):

        log(
            f"build_version ends with an invalid character: {build_version}",
            "warning"
        )


    log(
        "Loaded build configuration:",
        "success"
    )

    print(info)


    return info




def create_zip(name):

    BUILD_DIR.mkdir(
        exist_ok=True
    )


    rwmod_file = BUILD_DIR / (
        name + ".rwmod"
    )


    log(
        f"Creating package: {rwmod_file}"
    )


    if rwmod_file.exists():

        log(
            "Existing package found, replacing it",
            "warning"
        )

        rwmod_file.unlink()



    with zipfile.ZipFile(
        rwmod_file,
        "w",
        zipfile.ZIP_DEFLATED
    ) as z:


        for item in TARGET_FILES:


            src = ROOT / item


            if not src.exists():

                log(
                    f"Skipped missing file: {item}",
                    "warning"
                )

                continue



            log(
                f"Adding: {item}"
            )



            if src.is_dir():


                for f in src.rglob("*"):


                    if f.is_file():

                        z.write(
                            f,
                            f.relative_to(ROOT)
                        )



            else:


                z.write(
                    src,
                    src.name
                )



    log(
        f"Package created successfully: {rwmod_file}",
        "success"
    )




def main():

    log(
        f"Working directory: {ROOT}"
    )


    try:

        config = load_build_config()

        filename = (
            config["build_name"]
            +
            "_"
            +
            config["build_version"]
        )


        create_zip(filename)


    except Exception as e:

        log(
            f"Build failed: {e}",
            "error"
        )

        exit(1)



if __name__ == "__main__":

    main()
