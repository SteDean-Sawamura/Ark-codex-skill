#!/usr/bin/env python3
"""Create 打开桌宠 / 启动托盘 shortcuts on the Desktop and Start Menu."""

import argparse
import subprocess
import sys
from pathlib import Path


def ps_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def shortcut_ps(ws, folder_expr, name, target, args, cwd):
    return (
        "$s = $ws.CreateShortcut((Join-Path ("
        + folder_expr
        + ") "
        + ps_quote(name + ".lnk")
        + ")); "
        "$s.TargetPath = " + ps_quote(str(target)) + "; "
        "$s.Arguments = " + ps_quote('"' + str(args) + '"') + "; "
        "$s.WorkingDirectory = " + ps_quote(str(cwd)) + "; "
        "$s.Save(); Write-Output $s.FullName; "
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="deskpet project directory")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    pythonw = project / ".venv" / "Scripts" / "pythonw.exe"
    main_py = project / "main.py"
    launcher_py = project / "codex_pet_launcher.pyw"
    if not pythonw.is_file() or not main_py.is_file() or not launcher_py.is_file():
        sys.exit("project .venv or app files not found at " + str(project))

    desktop = "([Environment]::GetFolderPath('Desktop'))"
    programs = "([Environment]::GetFolderPath('Programs'))"
    command = (
        "$oldD = Join-Path ([Environment]::GetFolderPath('Desktop')) "
        "'\u542f\u52a8\u76d1\u542c\u5668.lnk'; "
        "if (Test-Path $oldD) { Remove-Item $oldD -Force }; "
        "$oldP = Join-Path ([Environment]::GetFolderPath('Programs')) "
        "'\u542f\u52a8\u76d1\u542c\u5668.lnk'; "
        "if (Test-Path $oldP) { Remove-Item $oldP -Force }; "
        "$ws = New-Object -ComObject WScript.Shell; "
    )
    command += shortcut_ps(
        "$ws", desktop, "打开桌宠", pythonw, main_py, project
    )
    command += shortcut_ps(
        "$ws", programs, "打开桌宠", pythonw, main_py, project
    )
    command += shortcut_ps(
        "$ws", desktop, "启动托盘", pythonw, launcher_py, project
    )
    command += shortcut_ps(
        "$ws", programs, "启动托盘", pythonw, launcher_py, project
    )

    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
    )
    if result.returncode != 0:
        sys.exit(
            "shortcut creation failed: "
            + result.stderr.decode("utf-8", "replace")
        )
    print("shortcuts created")


if __name__ == "__main__":
    main()
