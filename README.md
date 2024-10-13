# AB_PSI
## Overview
The **AB_PSI** repository is a comprehensive collection of Python scripts designed for processing nucleotide sequences and implementing cryptographic functionalities using the PyPBC library. This repository serves as a valuable toolkit for bioinformatics applications, particularly in genomic data processing and secure data representation. The repository includes the following key components:

- **Counter**: A script that reads nucleotide sequences from a file, filters out invalid characters, and writes valid nucleotides to an output file.
- **Sequence**: A script that processes nucleotide sequences by appending the index of each valid nucleotide and writing the results to a new file.
- **Sequence_Hash**: A script that generates SHA-256 hashes for each valid nucleotide combined with its index, providing a secure representation of the sequence.
- **PyPBC Installation Guide**: Instructions and challenges related to installing the PyPBC library for pairing-based cryptography.

## Components

### 1. Counter
The **Counter** script processes a file named `raw.txt`, which contains nucleotide sequences consisting of valid nucleotides (A, T, C, G) and potentially invalid characters.

#### Functionality
- **Input**: Reads from `raw.txt`.
- **Output**: Writes valid nucleotides to `24.txt`.
- **Processing Logic**:
  - The script iterates through each line in `raw.txt`.
  - It retains all lines, filtering out invalid characters (specifically `N`).
  - Valid nucleotides are concatenated and written to `24.txt`.

#### Example
If `raw.txt` contains:
```text
ATCGNATCGNNN
```
The output in `24.txt` would be:
```text
ATCGATCG
```

### 2. Sequence
The **Sequence** script enhances the functionality of the Counter by appending the index of each valid nucleotide to its value.

#### Functionality
- **Input**: Reads from `Raw.txt`.
- **Output**: Writes modified sequences to `sequenced.txt`.
- **Processing Logic**:
  - For each valid nucleotide, it appends its index (starting from zero) to the nucleotide itself before writing it to the output file.

#### Example
If `Raw.txt` contains:
```text
A0T1C2G3A5T6C7
```
The output in ``sequenced.txt`` would be:
```text
A0T1C2G3A5T6C7
```

### 3. Sequence_Hash
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
The output in `sequenced_Hashed.py` would contain lines like:
```text
a3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 # Hash for 'A0'
.
.
.
```

### 4. PyPBC Installation Challenges

Installing the PyPBC library can be challenging due to various factors such as compatibility issues and insufficient documentation. Below are detailed steps and challenges faced during installation on Ubuntu 20.04.

#### Installation Steps on Ubuntu 20.04

To install PyPBC, follow these steps in your terminal with admin (sudo) access:

1. **Update System Packages**
   ```bash
   sudo apt update
   sudo apt-get update
   sudo apt upgrade
   sudo apt-get upgrade
   ```
2. Install Required Dependencies
```bash
sudo apt-get install m4 flex bison
```
3. Download GMP Library
- Visit ftp.gnu.org/gnu/gmp/ and download ``gmp-6.2.1.tar.lz``.
- Extract the downloaded file in your desired directory.
- Navigate to that directory and run:
```bash
sudo ./configure
sudo apt install make
sudo make
sudo make check
sudo make install
```
4. Download PBC Library
- Visit PBC GitHub Repository and download the INSTALL file.
- Extract it in your desired directory.
- Navigate to that directory and run:
```bash
./configure
make
make check
sudo make install
```
5. Update Library Paths
```bash
sudo gedit /etc/ld.so.conf.d/newlib.conf  # Add usr/local/lib in the editor.
sudo ldconfig
```
6. Install Python Dependencies
```bash
sudo apt install python3-pip git
git clone https://github.com/debatem1/pypbc.git
cd pypbc
sudo python3 setup.py install
```
## Challenges Faced
- **Debugging Complexity**: Due to large numbers in cyclic groups, debugging can be difficult, especially when tracking operations like bilinear mappings in the Pairing class.
- **Element Inversion Issues**: Properly obtaining inverses in cyclic groups requires specific methods rather than simple exponentiation. The division operator is not defined over Elements; instead, use the function ``__ifloordiv__()`` from the Element class.
## Usage
To utilize the scripts in this repository:
1. Ensure all dependencies are installed as per the installation guide.
2. Place your nucleotide sequence files (raw.txt, etc.) in the appropriate directory specified in each script.
3. Run the desired script using Python:
```bash
python3 <script_name>.py  # Replace <script_name> with Counter, Sequence, or Sequence_Hash.
```
Author Information
This repository is maintained by [FarnoodID](https://github.com/FarnoodID). Contributions are welcomed! Feel free to raise issues or submit pull requests if you encounter challenges or have suggestions for improvements.
## Conclusion
The AB_PSI repository serves as a robust toolkit for processing nucleotide sequences while also providing insights into cryptographic implementations using PyPBC. Whether you're working on genomic data analysis or exploring secure data representations, this repository offers valuable resources and functionalities
