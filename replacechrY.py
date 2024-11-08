from tqdm import tqdm

def replacechrY(fn1, fn2, fileout):
  fh1 = open(fn1, 'r')
  fh2 = open(fn2, 'r')
  kept = True
  with open(fileout, 'w') as fout:
    for line in tqdm(fh1.readlines(), desc=f'processing {fn1}'):
      if line.startswith('>'):
        if 'chrY' in line:
          kept = False
        else:
          kept = True
      if kept:
        fout.write(line)
  kept = False
  with open(fileout, 'a') as fout:
    for line in tqdm(fh2.readlines(), desc=f'processing {fn2}'):
      if line.startswith('>'):
        if 'chrY' in line:
          kept = True
        else:
          kept = False
      if kept:
        fout.write(line)
  fh1.close()
  fh2.close()