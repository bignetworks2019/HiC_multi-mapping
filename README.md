# HiC_multi-mapping - Process multi mapping reads in HiC analysis
This repository provides scripts to process the multi mapping reads.

## Procedure
### Step 1
Run the [mHiC Tool](https://github.com/keleslab/mHiC) upto step 3 of their process.

### Step 2
Generate enzyme cutting sites file using [HiCUP Digester](https://www.bioinformatics.babraham.ac.uk/projects/hicup/read_the_docs/html/index.html). Sample file [Digest_hg18_HindIII.txt](sample-data/Digest_hg18_HindIII.txt) is provided.

Sample command to generate the digest file using HiCUP Digester.

```shell script
hicup_digester --genome hg18 --re1 A^AGCTT,HindIII *.fa
```

### Step 3
Run the script [multi-mapping-mHiC.py](src/multi-mapping-mHiC.py).

**Arguments**
```
input        (--input)  : Path to the *.validPairs file generated in step 1.
fragmentFile (--frag)   : Path to the enzyme cut site file generated in step 2
output       (--output) : Path to the output file
```

**Usage**
```shell script
python multi-mapping-mHiC.py --input hESC_r1.validPairs --frag Digest_hg18_HindIII.txt --output hESC_r1.output
```

### Step 4
Replaced the *.validPairs file generate in step 1 by the output file generated in Step 3 and continue the mHiC process only upto Step 4 of their process. Step 5 and 6 are not needed. Use the output file generated in mHiC process step 4 *.binPairCount.uni for further analysis.

 