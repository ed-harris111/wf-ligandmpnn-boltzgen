import subprocess
import sys
from pathlib import Path
from typing import Optional

from latch.executions import rename_current_execution
from latch.functions.messages import message
from latch.resources.tasks import small_gpu_task
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile

sys.stdout.reconfigure(line_buffering=True)



@small_gpu_task(cache=True)
def boltzgen_task(
    run_name: str,
    input_yaml: LatchFile,
    output_directory: LatchOutputDir = LatchOutputDir("latch:///BoltzGen"),
) -> LatchOutputDir:
    rename_current_execution(str(run_name))

    print("-" * 60)
    print("Creating local directories")
    local_output_dir = Path(f"/root/outputs/{run_name}")
    local_output_dir.mkdir(parents=True, exist_ok=True)

    print("-" * 60)
    subprocess.run(["nvidia-smi"], check=True)
    subprocess.run(["nvcc", "--version"], check=True)

    print("-" * 60)
    print("Running BoltzGen")
    boltzgen_dir = Path("/tmp/docker-build/work/boltgen")

    command = [
        "boltzgen", "run",
        input_yaml.local_path,
        "--output",
        str(local_output_dir), 
        "--steps", "design",
        "--num_designs", "2",
        ]

  
    print(f"Running command: {' '.join(command)}")

    try:
        subprocess.run(command, check=True, cwd=boltzgen_dir)
        print("Done")
    except Exception as e:
        print("FAILED")
        message("error", {"title": "LigandMPNN failed", "body": f"{e}"})
        sys.exit(1)

    print("-" * 60)
    print("Returning results")
    return LatchOutputDir(str("/root/outputs"), output_directory.remote_path)
