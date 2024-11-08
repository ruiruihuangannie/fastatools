from sys import exit
from tqdm import tqdm

def field_kv_pairs(string):
  fields = string.rstrip().split(';')
  pairs = dict()
  for field in fields:
    k, v = field.rstrip().split('=')
    pairs[k] = v
  return pairs

def extract_parent_annotation(string):
  kv = field_kv_pairs(string)
  if 'gene_biotype' in kv:
    gb = kv['gene_biotype']
  elif 'gene_type' in kv:
    gb = kv['gene_type']
  elif 'biotype' in kv:
    gb = kv['biotype']
  else:
    exit('Malformed GTF/GFF file: no valid gene type information.')
  return kv['ID'], gb

def extract_child_annotation(string):
  kv = field_kv_pairs(string)
  if 'ID' in kv:
    kid = kv['ID']
  else:
    kid = None
  return kid, kv['Parent']

def gff_sub(mp, fh, out_fh):
  cnt = 0
  for ln in tqdm(fh.readlines(), desc="Processed gff entries"):
    fields = ln.rstrip().split('\t')
    if fields[0] in mp:
      fields[0] = mp[fields[0]]
      cnt += 1
    out_fh.write('\t'.join(fields) + '\n')
  print(f'[Info]: Successfully canonicalized {cnt} entries.')

def fna_sub(mp, fh, out_fh):
  cnt = 0
  for ln in tqdm(fh.readlines(), desc="Processed fna entries"):
    if ln.startswith('>'):
      fields = ln.rstrip().split(' ')
      if fields[0][1:] in mp:
        fields[0] = '>' + mp[fields[0][1:]] + ' ' + ' '.join(fields[1:])
        cnt += 1
        out_fh.write(f'{fields[0]}\n')
      else:
        out_fh.write(ln)
    else:
      out_fh.write(ln)
  print(f'[Info]: Successfully canonicalized {cnt} entries.')

def extract_mapfile(fh):
  mp = dict()
  for line in fh.readlines():
      ln = line.rstrip().split(",")
      assert len(ln) >= 2
      mp[ln[1]] = ln[0]
  fh.close()
  return mp

def load_primary_names(fh):
  ans = list()
  for line in fh.readlines():
    ans.append(line.rstrip())
  fh.close()
  return ans