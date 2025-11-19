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

from wf.task import boltzgen_task

flow = [
    Section(
        "Input",
        Params(
            "input_yaml",
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
]

metadata = LatchMetadata(
    display_name="BoltzGen",
    author=LatchAuthor(
        name="TEMP AUTHOR",
    ),
    repository="",
    license="MIT",
    tags=["Protein Engineering"],
    parameters={
        "run_name": LatchParameter(
            display_name="Run Name",
            description="Name of run",
            batch_table_column=True,
        ),
        "input_yaml": LatchParameter(
            display_name="Input yaml",
            description="Input yaml file",
            batch_table_column=True,
        ),
        "output_directory": LatchParameter(
            display_name="Output Directory",
            description="Directory to write output files",
            batch_table_column=True,
        ),
    },
    flow=flow,
)


@workflow(metadata)
def boltzgen_workflow(
    run_name: str,
    input_yaml: LatchFile,
    output_directory: LatchOutputDir = LatchOutputDir("latch:///LigandMPNN"),
) -> LatchOutputDir:
   
    return boltzgen_task(
        run_name=run_name,
        input_yaml=input_yaml,
        output_directory=output_directory,
    )

