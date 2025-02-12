from utils import load_primary_names
from tqdm import tqdm

def keepprimary(file, outfile, keyword, lst, out_lst_names):
  fh = open(file, 'r')
  out_fh = open(outfile, 'w')
  if not out_lst_names:
    out_lst_names = file.rstrip().split('.')[0] + '_primary.txt'
  deleted = 0
  if any(ext in file for ext in ['gff', 'gtf']):
    primaries = load_primary_names(open(lst, 'r'))
    for line in tqdm(fh.readlines(), desc="Processed gtf/gff entries"):
      chr = line.rstrip().split('\t')[0]
      if chr in primaries:
        out_fh.write(line)
      else:
        deleted += 1
  elif any(ext in file for ext in ['fna', 'fa', 'fasta']):
    out_lst_fh = open(out_lst_names, 'w')
    kept = False
    for line in tqdm(fh.readlines(), desc="Processed fna entries"):
      if line.startswith('>'):
        chr = line[1:].rstrip().split(' ')[0]
        if any(key in line for key in keyword):
          kept = True
          out_lst_fh.write(f'{chr}\n')
        else:
          kept = False
          deleted += 1
      if kept:
        out_fh.write(line)
    out_lst_fh.close()
  print(f'[Info]: {deleted} entries not on the primary assembly of {file}')
  fh.close()
  out_fh.close()
  return outfile