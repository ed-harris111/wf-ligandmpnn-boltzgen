import subprocess
import sys
from pathlib import Path
from typing import Optional

from latch.executions import rename_current_execution
from latch.functions.messages import message
from latch.resources.tasks import small_gpu_task
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile
from latch.types.directory import LatchDir

sys.stdout.reconfigure(line_buffering=True)



@small_gpu_task(cache=True)
def boltzgen_task(
    run_name: str,
    input_yaml_dir: LatchDir,
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

    command = [
        "/root/miniconda/envs/mlfold/bin/boltzgen", "run",
        str(Path(input_yaml_dir) / "1g13prot.yaml"),
        "--output",
        str(local_output_dir), 
        "--steps", "design",
        "--num_designs", "2",
        ]

  
    print(f"Running command: {' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("FAILED")
        print(e.stdout)
        print(e.stderr)
        message(
            "error",
            {
                "title": "BoltzGen failed",
                "body": f"Return code {e.returncode}\n{e.stderr}",
            },
        )
        sys.exit(1)
    print("-" * 60)
    print("Returning results")

    return LatchOutputDir(str("/root/outputs"), output_directory.remote_path)
