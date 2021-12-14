import subprocess

from .panel import append_to_output_panel

def run_process(command, cwd, output_panel):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
        bufsize=1
    )

    out = process.stdout
    if out:
        for line in iter(out.readline, b""):
            append_to_output_panel(output_panel, line)
