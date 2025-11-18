import subprocess
import sys
from pathlib import Path
from typing import Optional

from latch.executions import rename_current_execution
from latch.functions.messages import message
from latch.resources.tasks import large_gpu_task, small_gpu_task
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile

sys.stdout.reconfigure(line_buffering=True)


@small_gpu_task(cache=True)
def ligandmpnn_task(
    run_name: str,
    input_pdb: LatchFile,
    output_directory: LatchOutputDir = LatchOutputDir("latch:///LigandMPNN"),
    model_type: str = "ligand_mpnn",
    seed: int = 111,
    temperature: float = 0.1,
    number_of_batches: int = 1,
    batch_size: int = 1,
    checkpoint_ligand_mpnn: Optional[str] = None,
    ligand_mpnn_use_atom_context: int = 1,
    ligand_mpnn_use_side_chain_context: int = 0,
    pack_side_chains: int = 0,
    number_of_packs_per_design: int = 0,
    pack_with_ligand_context: int = 1,
    fixed_residues: Optional[str] = None,
    redesigned_residues: Optional[str] = None,
    chains_to_design: Optional[str] = None,
    bias_AA: Optional[str] = None,
    bias_AA_jsonl: Optional[LatchFile] = None,
    omit_AA: Optional[str] = None,
    omit_AA_jsonl: Optional[LatchFile] = None,
    save_stats: int = 0,
    parse_these_chains_only: Optional[str] = None,
    symmetry_residues: Optional[str] = None,
    symmetry_weights: Optional[str] = None,
    homo_oligomer: int = 0,
    bias_AA_per_residue_jsonl: Optional[LatchFile] = None,
    omit_AA_per_residue_jsonl: Optional[LatchFile] = None,
    parse_atoms_with_zero_occupancy: int = 0,
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
    print("Running LigandMPNN")
    ligandmpnn_dir = Path("/tmp/docker-build/work/LigandMPNN")

    command = [
        "python",
        f"{ligandmpnn_dir}/run.py",
        "--model_type",
        model_type,
        "--seed",
        str(seed),
        "--pdb_path",
        str(input_pdb.local_path),
        "--out_folder",
        str(local_output_dir),
        "--number_of_batches",
        str(number_of_batches),
        "--batch_size",
        str(batch_size),
        "--temperature",
        str(temperature),
    ]

    # Tahir: ToDo - Make this nicer

    if checkpoint_ligand_mpnn:
        command.extend(["--checkpoint_ligand_mpnn", checkpoint_ligand_mpnn])
    if ligand_mpnn_use_atom_context == 0:
        command.extend(
            ["--ligand_mpnn_use_atom_context", str(ligand_mpnn_use_atom_context)]
        )
    if ligand_mpnn_use_side_chain_context == 1:
        command.extend(
            [
                "--ligand_mpnn_use_side_chain_context",
                str(ligand_mpnn_use_side_chain_context),
            ]
        )
    if pack_side_chains == 1:
        command.extend(["--pack_side_chains", str(pack_side_chains)])
    if number_of_packs_per_design > 0:
        command.extend(
            ["--number_of_packs_per_design", str(number_of_packs_per_design)]
        )
    if pack_with_ligand_context == 1:
        command.extend(["--pack_with_ligand_context", "1"])
    if fixed_residues:
        command.extend(["--fixed_residues", fixed_residues])
    if redesigned_residues:
        command.extend(["--redesigned_residues", redesigned_residues])
    if chains_to_design:
        command.extend(["--chains_to_design", chains_to_design])
    if bias_AA:
        command.extend(["--bias_AA", bias_AA])
    if bias_AA_jsonl:
        command.extend(["--bias_AA_jsonl", str(bias_AA_jsonl.local_path)])
    if omit_AA:
        command.extend(["--omit_AA", omit_AA])
    if omit_AA_jsonl:
        command.extend(["--omit_AA_jsonl", str(omit_AA_jsonl.local_path)])
    if symmetry_residues:
        command.extend(["--symmetry_residues", symmetry_residues])
    if symmetry_weights:
        command.extend(["--symmetry_weights", symmetry_weights])
    if homo_oligomer == 1:
        command.extend(["--homo_oligomer", str(homo_oligomer)])
    if bias_AA_per_residue_jsonl:
        command.extend(
            ["--bias_AA_per_residue_jsonl", str(bias_AA_per_residue_jsonl.local_path)]
        )
    if omit_AA_per_residue_jsonl:
        command.extend(
            ["--omit_AA_per_residue_jsonl", str(omit_AA_per_residue_jsonl.local_path)]
        )
    if parse_atoms_with_zero_occupancy == 1:
        command.extend(
            ["--parse_atoms_with_zero_occupancy", str(parse_atoms_with_zero_occupancy)]
        )
    if save_stats == 1:
        command.extend(["--save_stats", str(save_stats)])
    if parse_these_chains_only:
        command.extend(["--parse_these_chains_only", parse_these_chains_only])

    print(f"Running command: {' '.join(command)}")

    try:
        subprocess.run(command, check=True, cwd=ligandmpnn_dir)
        print("Done")
    except Exception as e:
        print("FAILED")
        message("error", {"title": "LigandMPNN failed", "body": f"{e}"})
        sys.exit(1)

    print("-" * 60)
    print("Returning results")
    return LatchOutputDir(str("/root/outputs"), output_directory.remote_path)
