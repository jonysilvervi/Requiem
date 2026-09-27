import os
import json
from datetime import datetime


CONFIG_FILE = "scanner_config.json"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def scan_directory(path, ignored):
    result = []

    for root, dirs, files in os.walk(path):

        dirs[:] = [
            d for d in dirs
            if d not in ignored
        ]

        for file in files:
            full_path = os.path.join(root, file)

            result.append(
                full_path.replace("\\", "/")
            )

    return result


def create_report(files):
    report = []

    report.append("# REQUIEM MEMORY CORE SCAN REPORT\n")
    report.append(
        f"Date: {datetime.now()}\n"
    )

    report.append(
        f"Files detected: {len(files)}\n"
    )

    report.append("\n## Files\n")

    for file in files:
        report.append(
            f"- {file}\n"
        )

    return "".join(report)


def main():

    config = load_config()

    project_path = config["project_path"]

    ignored = config["ignore"]

    files = scan_directory(
        project_path,
        ignored
    )

    report = create_report(files)

    output = config["output"]["report_directory"]

    os.makedirs(
        output,
        exist_ok=True
    )

    report_file = os.path.join(
        output,
        config["output"]["report_name"]
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(report)

    print(
        "Memory Core scan completed."
    )


if __name__ == "__main__":
    main()