# AB_PSI
## Overview
The **AB_PSI** repository is a comprehensive collection of Python scripts designed for processing nucleotide sequences and implementing cryptographic functionalities using the PyPBC library. This repository serves as a valuable toolkit for bioinformatics applications, particularly in genomic data processing and secure data representation. The primary focus is on sharing genetic data securely through an Attribute-Based Private Set Intersection (AB-PSI) protocol, ensuring that sensitive genomic information remains confidential while allowing for meaningful analysis. The repository includes the following key components:


- **AB-PSI Protocol**: A cryptographic method that allows two parties to compute the intersection of their datasets without revealing any additional information.
- **Counter**: A script that reads nucleotide sequences from a file, filters out invalid characters, and writes valid nucleotides to an output file.
- **Sequence**: A script that processes nucleotide sequences by appending the index of each valid nucleotide and writing the results to a new file.
- **Sequence_Hash**: A script that generates SHA-256 hashes for each valid nucleotide combined with its index, providing a secure representation of the sequence.

## Components

### 1. AB-PSI Protocol
The AB-PSI (Attribute-Based Private Set Intersection) protocol is a cryptographic method that allows two parties to compute the intersection of their datasets without revealing any additional information. This is particularly useful in genomic data sharing, where privacy concerns are paramount.
#### Key Features:
- **Privacy Preservation**: Enables users to share genome sequences without disclosing non-shared parts.
- **Attribute-Based Access Control**: Users can only access data if they possess specific attributes defined by data owners.
- **Secure Data Sharing**: Facilitates safe sharing of genetic data in cloud environments while maintaining confidentiality.
  
### 2. Counter
The **Counter** script processes a file named `raw.txt`, which contains nucleotide sequences consisting of valid nucleotides (A, T, C, G) and potentially invalid characters.

#### Functionality
- **Input**: Reads from `raw.txt`.
- **Output**: Writes valid nucleotides to `output.txt`.
- **Processing Logic**:
  - The script iterates through each line in `raw.txt`.
  - It retains all lines, filtering out invalid characters (specifically `N`).
  - Valid nucleotides are concatenated and written to `output.txt`.

#### Example
If `raw.txt` contains:
```text
ATCGNATCGNNN
```
The output in `output.txt` would be:
```text
ATCGATCG
```

### 3. Sequence
The **Sequence** script enhances the functionality of the Counter by appending the index of each valid nucleotide to its value.

#### Functionality
- **Input**: Reads from `Raw.txt`.
- **Output**: Writes modified sequences to `sequenced.txt`.
- **Processing Logic**:
  - For each valid nucleotide, it appends its index (starting from zero) to the nucleotide itself before writing it to the output file.

#### Example
If `Raw.txt` contains:
```text
ATCGNATCG
```
The output in ``sequenced.txt`` would be:
```text
A0T1C2G3A5T6C7G8
```

### 4. Sequence_Hash
The **Sequence_Hash** script builds upon the Sequence functionality by generating SHA-256 hashes for each valid nucleotide along with its index.

#### Functionality
- **Input**: Reads from `Raw.txt`.
- **Output**: Writes SHA-256 hashes to `sequenced_Hashed.txt`.
- **Processing Logic**:
  - Each valid nucleotide is combined with its index, hashed using SHA-256, and written to the output file.

#### Example
If `Raw.txt` contains:
```text
ATCGNATCG
```
The output in `sequenced_Hashed.txt` would contain lines like:
```text
a3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 # Hash for 'A0'
.
.
.
```


## Implementation Details

### System Architecture
The AB-PSI system consists of several key components:
1. **Central Authority**: Initializes public parameters and manages private keys based on user attributes.
2. **Cloud Service Provider (CSP)**: Provides storage services and facilitates PSI calculations.
3. **Data Owners**: Define access control policies and blind their datasets before outsourcing them to the cloud.
4. **Data Users**: Request access tokens based on their attributes to compute intersections with data owners' datasets.

### Phases of Operation
1. **Setup Phase**: The central authority generates public parameters and private keys.
2. **Key Generation Phase**: Data users request private keys based on their attributes.
3. **Blinding Phase**: Data owners blind their datasets according to access policies before outsourcing.
4. **PSI Calculation Phase**: Tokens are generated and exchanged between users and the CSP to compute shared genome sequences securely.

## Challenges in Implementation

### Installation of PyPBC Library
Installing the PyPBC library can be challenging due to various factors such as compatibility issues with different Python versions and insufficient documentation. Below are detailed steps for installation on Ubuntu 20.04:

1. **Update System Packages**:
   ```bash
   sudo apt update && sudo apt-get update && sudo apt upgrade && sudo apt-get upgrade
   ```
2. **Install Required Dependencies**:
   ```bash
   sudo apt-get install m4 flex bison
   ```
3. **Download GMP Library**:
- Visit [ftp.gnu.org/gnu/gmp/](https://ftp.gnu.org/gnu/gmp/) and download ``gmp-6.2.1.tar.lz``.
- Extract the downloaded file in your desired directory.
- Navigate to that directory and run:
   ```bash
   sudo ./configure
   sudo apt install make
   sudo make
   sudo make check
   sudo make install
   ```
4. **Download PBC Library**:
- Visit [PBC GitHub Repository](https://github.com/debatem1/pypbc/tree/master) and download it.
- Extract it in your desired directory.
- Navigate to that directory and run:
   ```bash
   ./configure
   make
   make check
   sudo make install
   ```
5. **Update Library Paths**:
   ```bash
   sudo gedit /etc/ld.so.conf.d/newlib.conf  # Add usr/local/lib in the editor.
   sudo ldconfig
   ```
6. **Install Python Dependencies**:
   ```bash
   sudo apt install python3-pip git
   git clone https://github.com/debatem1/pypbc.git
   cd pypbc
   sudo python3 setup.py install
   sudo rp3 install pypbc
   ```
### Debugging Complexity
Due to large numbers in cyclic groups, debugging can be difficult, especially when tracking operations like bilinear mappings in the Pairing class.

### Common Bugs in Code
One common bug that may cause trouble in the code is found in the `apply()` function of the Pairing class. This function performs a bilinear mapping from two cyclic groups of prime order to another cyclic group. The order of arguments in this function is crucial; specifically, the output will always be an element of the first argument’s cyclic group. Thus, (Pairing.apply(G1,G2) ≠ Pairing.apply(G2,G1)).

### Element Inversion Issues
Properly obtaining inverses in cyclic groups requires specific methods rather than simple exponentiation. The division operator is not defined over Elements; instead, used the function ``__ifloordiv__()`` from the Element class. Also the "one()" function of the Element class in the PyPBC library gives us the multiplication neutral element.

## Usage
To utilize the scripts in this repository:
1. Ensure all dependencies are installed as per the installation guide.
2. Place your nucleotide sequence files (raw.txt, etc.) in the appropriate directory specified in each script.
3. Run the desired script using Python:
   ```bash
   python3 <script_name>.py  # Replace <script_name> with Counter, Sequence, or Sequence_Hash.
   ```
4. Run the AB_PSI script using Python:
   ```bash
   python3 AB_PSI.py
   ```

## Author Information
This repository is maintained by [FarnoodID](https://github.com/FarnoodID). Contributions are welcomed! Feel free to raise issues or submit pull requests if you encounter challenges or have suggestions for improvements.

## Conclusion
In this project, we utilize the AB-PSI scheme to compute shared genome sequences securely outsourced in the cloud. The design allows data owners to maintain control over subscription calculations through access control policies while ensuring efficiency in terms of security and execution.
This repository offers valuable resources for researchers and developers interested in secure genomic data processing using advanced cryptographic techniques.

