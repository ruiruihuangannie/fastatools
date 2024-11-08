# fastatools

A toolset for processing FASTA/GTF/GFF files.
## Installation

```bash
  git clone https://github.com/ruiruihuangannie/fastatools
  export PATH="$PATH:/YOUR-PATH/fastatools"
```
    
## Usage

`fastatools [-h] {makecanonical,keepprimary,gffextract,gffdiscard,rDNAaddparent,replacechrY} ...`

### positional arguments:  
    makecanonical       Make FASTA/GTF/GFF canonical.  
    keepprimary         Keep primary assemblies in FASTA/GTF/GFF.  
    gffextract          Extract specified regions from GTF/GFF file.  
    gffdiscard          Discard specified regions from GTF/GFF file.  
    rDNAaddparent       Extract rDNA arrays from GTF/GFF file.  
    replacechrY         Combine two GTF/GFF files.  
