# LigandMPNN: Deep learning-based protein sequence design method that allows explicit modeling of small molecule, nucleotide, metal, and other atomic contexts.

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
