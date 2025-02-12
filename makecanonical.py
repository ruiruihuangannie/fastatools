from utils import gff_sub, fna_sub, extract_mapfile

def makecanonical(file, outfile, mapfile):
  fh = open(file, 'r')
  map_lst = extract_mapfile(open(mapfile, 'r'))
  out_fh = open(outfile, 'w')
  if any(ext in file for ext in ['gff', 'gtf']):
    gff_sub(map_lst, fh, out_fh)
  elif any(ext in file for ext in ['fna', 'fa', 'fasta']):
    fna_sub(map_lst, fh, out_fh)
  fh.close()
  out_fh.close()
  return outfile