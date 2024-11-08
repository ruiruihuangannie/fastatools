from utils import extract_parent_annotation, extract_child_annotation
from tqdm import tqdm

def gffextract(infile, outfile, extract_VDJ, extract_rDNA, extract_chrY):
  """
  Process the GFF file and extract VDJ, rDNA, and/or chrY regions based on user selection.
  The file is processed once, and the relevant regions are written to the output.
  """
  g_lst, vdj_lst, exon_lst = list(), list(), list()
  rDNA_lst = list()
  in_fh = open(infile, 'r')
  if not outfile:
    nm = infile.rstrip().split('.')
    mid = ''
    if extract_VDJ:
      mid += 'VDJ-'
    if extract_rDNA:
      mid += 'rDNA-'
    if extract_chrY:
      mid += 'chrY-'
    mid += 'only'
    out_fn = nm[0] + '_' + mid + '.' + nm[1]
  out_fh = open(out_fn, 'w')

  for line in tqdm(in_fh.readlines(), desc="Processed gff entries"):
    kept = False
    fields = line.rstrip().split('\t')
    if len(fields) < 9:
      continue

    f_type, f_annot = fields[2], fields[8]

    # Extract chrY-related entries
    if extract_chrY and fields[0] == 'chrY':
      out_fh.write(line)
      continue

    # Extract VDJ-related entries
    if extract_VDJ and f_type in ['gene', 'pseudogene']:
      g_id, g_type = extract_parent_annotation(f_annot)
      if g_type in ["V_segment", "D_segment", "J_segment", "J_segment_pseudogene", "V_segment_pseudogene",
                    "TR_D_gene","TR_J_gene","TR_J_pseudogene","TR_V_gene","TR_V_pseudogene",
                    "IG_D_gene","IG_J_gene","IG_J_pseudogene","IG_V_gene","IG_V_pseudogene"]:
        g_lst.append(g_id)
        kept = True
    elif extract_VDJ and f_type in ['V_gene_segment', 'D_gene_segment', 'J_gene_segment', 'exon']:
      t_id, t_parent = extract_child_annotation(f_annot)
      if t_parent in g_lst:
        vdj_lst.append(t_id)
        kept = True
      elif t_parent in vdj_lst:
        exon_lst.append(t_id)
        kept = True

    # Extract rDNA-related entries
    if extract_rDNA and f_type == 'gene':
      g_id, g_type = extract_parent_annotation(f_annot)
      if g_type == 'rRNA':
        g_lst.append(g_id)
        kept = True
    elif extract_rDNA and f_type in ["rRNA", "transcript"]:
      t_id, t_parent = extract_child_annotation(f_annot)
      if t_parent in g_lst and t_id:
        rDNA_lst.append(t_id)
        kept = True
      elif t_parent in rDNA_lst:
        exon_lst.append(t_id)
        kept = True
    # Write the line if it matched any of the criteria
    if kept:
        out_fh.write(line)
  in_fh.close()
  out_fh.close()
