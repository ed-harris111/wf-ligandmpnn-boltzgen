from typing import Optional

from latch.resources.launch_plan import LaunchPlan
from latch.resources.workflow import workflow
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import (
    LatchAuthor,
    LatchMetadata,
    LatchParameter,
    Params,
    Section,
    Spoiler,
    Text,
)

from wf.task import ligandmpnn_task

flow = [
    Section(
        "Input",
        Params(
            "input_pdb",
        ),
        Text("The input PDB file can contain:"),
        Text(
            "- Protein backbone coordinates: The file should include the 3D coordinates for the main chain atoms (N, Cα, C, O) of each residue in the protein structure."
        ),
        Text(
            "- Ligands or non-protein atoms (if applicable): If your protein interacts with ligands, metals, or other non-protein molecules, include their 3D coordinates in the PDB file. These will be considered during sequence design and side chain packing."
        ),
        Text(
            "- Side chain coordinates (optional): While not required, including existing side chain coordinates can provide additional context for the design process."
        ),
        Text(
            "The PDB file should follow standard PDB format. Ensure that all non-standard residues or ligands are properly defined in the HETATM records. If using modified amino acids, make sure they are correctly specified in the MODRES records."
        ),
        Text(
            "Note: The input PDB represents the backbone scaffold for design. LigandMPNN will generate a new sequence to fit this backbone while considering any included ligands or non-protein atoms."
        ),
    ),
    Section(
        "Output",
        Params("run_name"),
        Text("Directory for outputs"),
        Params("output_directory"),
    ),
    Section(
        "Model Configuration",
        Params(
            "model_type",
            "checkpoint_ligand_mpnn",
            "seed",
            "temperature",
            "number_of_batches",
            "batch_size",
        ),
        Spoiler(
            "LigandMPNN Options",
            Params(
                "ligand_mpnn_use_atom_context",
                "ligand_mpnn_use_side_chain_context",
            ),
        ),
    ),
    Section(
        "Side Chain Packing",
        Params(
            "pack_side_chains",
            "number_of_packs_per_design",
            "pack_with_ligand_context",
        ),
    ),
    Spoiler(
        "Residue Selection",
        Params(
            "fixed_residues",
            "redesigned_residues",
            "chains_to_design",
            "parse_these_chains_only",
        ),
    ),
    Spoiler(
        "Amino Acid Biases and Restrictions",
        Params(
            "bias_AA",
            "bias_AA_jsonl",
            "bias_AA_per_residue_jsonl",
            "omit_AA",
            "omit_AA_jsonl",
            "omit_AA_per_residue_jsonl",
        ),
    ),
    Spoiler(
        "Symmetry and Oligomers",
        Params(
            "symmetry_residues",
            "symmetry_weights",
            "homo_oligomer",
        ),
    ),
    Spoiler(
        "Advanced Options",
        Params(
            "save_stats",
            "parse_atoms_with_zero_occupancy",
        ),
    ),
]

metadata = LatchMetadata(
    display_name="LigandMPNN",
    author=LatchAuthor(
        name="Justas Dauparas et al.",
    ),
    repository="https://github.com/latchbio-workflows/wf-latchbio-ligandmpnn",
    license="MIT",
    tags=["Protein Engineering"],
    parameters={
        "run_name": LatchParameter(
            display_name="Run Name",
            description="Name of run",
            batch_table_column=True,
        ),
        "input_pdb": LatchParameter(
            display_name="Input PDB",
            description="Input PDB file",
            batch_table_column=True,
        ),
        "output_directory": LatchParameter(
            display_name="Output Directory",
            description="Directory to write output files",
            batch_table_column=True,
        ),
        "model_type": LatchParameter(
            display_name="Model Type",
            description="Type of model to use (e.g., 'ligand_mpnn')",
        ),
        "seed": LatchParameter(
            display_name="Seed",
            description="Random seed (default: 111)",
        ),
        "temperature": LatchParameter(
            display_name="Temperature",
            description="Temperature for sampling (default: 0.1)",
        ),
        "number_of_batches": LatchParameter(
            display_name="Number of Batches",
            description="Number of batches to run",
        ),
        "batch_size": LatchParameter(
            display_name="Batch Size",
            description="Number of sequences per batch",
        ),
        "checkpoint_ligand_mpnn": LatchParameter(
            display_name="LigandMPNN Checkpoint",
            description="Path to LigandMPNN checkpoint file",
        ),
        "ligand_mpnn_use_atom_context": LatchParameter(
            display_name="Use Atom Context",
            description="Use atom context in LigandMPNN (0 or 1)",
        ),
        "ligand_mpnn_use_side_chain_context": LatchParameter(
            display_name="Use Side Chain Context",
            description="Use side chain context in LigandMPNN (0 or 1)",
        ),
        "pack_side_chains": LatchParameter(
            display_name="Pack Side Chains",
            description="Perform side chain packing (0 or 1)",
        ),
        "number_of_packs_per_design": LatchParameter(
            display_name="Number of Packs per Design",
            description="Number of side chain packing samples (0 for single fast sample, >0 for multiple samples)",
        ),
        "pack_with_ligand_context": LatchParameter(
            display_name="Pack with Ligand Context",
            description="Consider ligand/DNA atoms during side chain packing (0 or 1)",
        ),
        "fixed_residues": LatchParameter(
            display_name="Fixed Residues",
            description="Residues to keep fixed during design (e.g., 'C1 C2 C3 C4 C5')",
        ),
        "redesigned_residues": LatchParameter(
            display_name="Redesigned Residues",
            description="Residues to redesign (e.g., 'C1 C2 C3 C4 C5')",
        ),
        "chains_to_design": LatchParameter(
            display_name="Chains to Design",
            description="Specify which chains to design (e.g., 'A,B,C')",
        ),
        "bias_AA": LatchParameter(
            display_name="Global AA Bias",
            description="Global amino acid bias (e.g., 'W:3.0,P:3.0,C:3.0,A:-3.0')",
        ),
        "bias_AA_jsonl": LatchParameter(
            display_name="Per-residue AA Bias JSONL",
            description="JSONL file specifying per-residue amino acid biases",
        ),
        "omit_AA": LatchParameter(
            display_name="Global AA Omission",
            description="Amino acids to omit globally (e.g., 'CDFGHILMNPQRSTVWY')",
        ),
        "omit_AA_jsonl": LatchParameter(
            display_name="Per-residue AA Omission JSONL",
            description="JSONL file specifying per-residue amino acid omissions",
        ),
        "save_stats": LatchParameter(
            display_name="Save Statistics",
            description="Save sequence design statistics (0 or 1)",
        ),
        "parse_these_chains_only": LatchParameter(
            display_name="Parse These Chains Only",
            description="Only parse and design specified chains (e.g., 'A,B,C')",
        ),
        "symmetry_residues": LatchParameter(
            display_name="Symmetry Residues",
            description="Residues to be designed with symmetry (e.g., 'C1,C2,C3|C4,C5|C6,C7')",
        ),
        "symmetry_weights": LatchParameter(
            display_name="Symmetry Weights",
            description="Weights for symmetry residues (e.g., '0.33,0.33,0.33|0.5,0.5|0.5,0.5')",
        ),
        "homo_oligomer": LatchParameter(
            display_name="Homo-oligomer",
            description="Design homo-oligomer sequences (0 or 1)",
        ),
        "bias_AA_per_residue_jsonl": LatchParameter(
            display_name="Bias AA Per Residue JSONL",
            description="JSONL file specifying amino acid biases per residue",
        ),
        "omit_AA_per_residue_jsonl": LatchParameter(
            display_name="Omit AA Per Residue JSONL",
            description="JSONL file specifying amino acids to omit per residue",
        ),
        "parse_atoms_with_zero_occupancy": LatchParameter(
            display_name="Parse Atoms with Zero Occupancy",
            description="Parse atoms in the PDB files with zero occupancy (0 or 1)",
        ),
    },
    flow=flow,
)


@workflow(metadata)
def ligandmpnn_workflow(
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
    """
    LigandMPNN: Deep learning-based protein sequence design method that allows explicit modeling of small molecule, nucleotide, metal, and other atomic contexts.

    <p align="center">
        <img src="https://cbirt.net/wp-content/uploads/2024/01/LigandMPNN.webp" width="800px"/>
    </p>

    <html>
    <p align="center">
    <img src="https://user-images.githubusercontent.com/31255434/182289305-4cc620e3-86ae-480f-9b61-6ca83283caa5.jpg" alt="Latch Verified" width="100">
    </p>

    <p align="center">
    <strong>
    Latch Verified
    </strong>
    </p>

    # LigandMPNN

    LigandMPNN is a deep learning-based protein sequence design method that explicitly models all non-protein components of biomolecular systems. It allows for the design of proteins in the context of small molecules, nucleotides, metals, and other atomic contexts, which is critical for enzyme design and the creation of small molecule binders and sensors.

    ### Key Features

    - Explicitly models non-protein atoms and molecules
    - Outperforms Rosetta and ProteinMPNN in native backbone sequence recovery for residues interacting with:
        - Small molecules (63.3% vs. 50.4% & 50.5%)
        - Nucleotides (50.5% vs. 35.2% & 34.0%)
        - Metals (77.5% vs. 36.0% & 40.6%)
    - Generates both sequences and sidechain conformations
    - Enables detailed evaluation of binding interactions
    - Supports design of symmetric and multi-state proteins
    - High-speed and lightweight (0.9 seconds on a single CPU for 100 residues)

    ### Model Architecture and Functioning

    LigandMPNN builds upon the ProteinMPNN architecture, generalizing it to incorporate non-protein atoms. The model operates on three different graphs:

    - Protein-only graph:
        - Nodes: Protein residues
        - Edges: Based on Cα-Cα distances (25 nearest neighbors)
        - Edge features: Pairwise distances between N, Cα, C, O, and virtual Cβ atoms

    - Intra-ligand graph:
        - Nodes: Ligand atoms (25 closest to each protein residue)
        - Node features: One-hot encoded chemical element types
        - Edges: Fully connected
        - Edge features: Distances between atoms

    - Protein-ligand graph:
        - Nodes: Protein residues and ligand atoms
        - Edges: Between each protein residue and its 25 closest ligand atoms
        - Edge features: Distances between protein atoms (N, Cα, C, O, virtual Cβ) and ligand atoms


    The model consists of three main components:

    - Protein backbone encoder:
        - Three encoder layers with 128 hidden dimensions
        - Processes protein-only graph to obtain intermediate node/edge representations

    - Protein-ligand encoder:
        - Two message-passing blocks
        - Updates ligand graph representations
        - Updates protein-ligand graph representations
        - Combines output with protein encoder node representations

    - Decoder:
        - Uses random autoregressive decoding scheme
        - Generates amino acid sequences
        - Predicts sidechain conformations (torsion angles)


    Sidechain packing:
    - Predicts four side-chain torsion angles (chi1, chi2, chi3, chi4) for each residue
    - Uses a mixture of three circular normal distributions per chi angle
    - Autoregressively decodes chi angles in order (chi1, chi2, chi3, chi4)

    Training:
    - Augmented dataset by using 2-4% of protein residue side-chain atoms as context ligand atoms
    - Enables direct input of side-chain atom coordinates to stabilize functional sites

    The LigandMPNN neural network has 2.62 million parameters, compared to ProteinMPNN's 1.66 million parameters. Despite the increased complexity, it maintains high speed and lightweight operation, scaling linearly with respect to protein length.

    ### Applications

    - Enzyme design
    - Protein-DNA/RNA binder design
    - Protein-small molecule binder design
    - Protein-metal binder design

    ### Performance

    Experimental characterization demonstrates that LigandMPNN can generate small molecule and DNA-binding proteins with high affinity and specificity.

    ### Credits

    Atomic context-conditioned protein sequence design using LigandMPNN
    Justas Dauparas, Gyu Rie Lee, Robert Pecoraro, Linna An, Ivan Anishchenko, Cameron Glasscock, D. Baker
    bioRxiv 2023.12.22.573103; doi: https://doi.org/10.1101/2023.12.22.573103

    """
    return ligandmpnn_task(
        run_name=run_name,
        input_pdb=input_pdb,
        output_directory=output_directory,
        model_type=model_type,
        seed=seed,
        temperature=temperature,
        number_of_batches=number_of_batches,
        batch_size=batch_size,
        checkpoint_ligand_mpnn=checkpoint_ligand_mpnn,
        ligand_mpnn_use_atom_context=ligand_mpnn_use_atom_context,
        ligand_mpnn_use_side_chain_context=ligand_mpnn_use_side_chain_context,
        pack_side_chains=pack_side_chains,
        number_of_packs_per_design=number_of_packs_per_design,
        pack_with_ligand_context=pack_with_ligand_context,
        fixed_residues=fixed_residues,
        redesigned_residues=redesigned_residues,
        chains_to_design=chains_to_design,
        bias_AA=bias_AA,
        bias_AA_jsonl=bias_AA_jsonl,
        omit_AA=omit_AA,
        omit_AA_jsonl=omit_AA_jsonl,
        save_stats=save_stats,
        parse_these_chains_only=parse_these_chains_only,
        symmetry_residues=symmetry_residues,
        symmetry_weights=symmetry_weights,
        homo_oligomer=homo_oligomer,
        bias_AA_per_residue_jsonl=bias_AA_per_residue_jsonl,
        omit_AA_per_residue_jsonl=omit_AA_per_residue_jsonl,
        parse_atoms_with_zero_occupancy=parse_atoms_with_zero_occupancy,
    )


LaunchPlan(
    ligandmpnn_workflow,
    "New Sequence with Single Side Chain",
    {
        "run_name": "sequence_single_side_chain",
        "input_pdb": LatchFile(
            "s3://latch-public/proteinengineering/ligandmpnn/1BC8.pdb"
        ),
        "pack_side_chains": 1,
        "pack_with_ligand_context": 1,
    },
)
