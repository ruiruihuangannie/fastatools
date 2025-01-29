from utils import extract_parent_annotation, extract_child_annotation
from tqdm import tqdm

def gffdiscard(infile, outfile, discard_VDJ, discard_rDNA, discard_chrY):
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
    if discard_VDJ:
      mid += 'VDJ-'
    if discard_rDNA:
      mid += 'rDNA-'
    if discard_chrY:
      mid += 'chrY-'
    mid += 'discarded'
    out_fn = nm[0] + '_' + mid + '.' + nm[1]
  out_fh = open(out_fn, 'w')

  for line in tqdm(in_fh.readlines(), desc="Processed gff entries"):
    fields = line.rstrip().split('\t')
    if len(fields) < 9:
      continue

    f_type, f_annot = fields[2], fields[8]

    if discard_chrY and fields[0] == 'chrY':
      continue

    if discard_VDJ and f_type in ['gene', 'pseudogene']:
      g_id, g_type = extract_parent_annotation(f_annot)
      if g_type in ["V_segment", "D_segment", "J_segment", "J_segment_pseudogene", "V_segment_pseudogene",
                    "IG_C_gene","IG_C_pseudogene","IG_D_gene","IG_J_gene","IG_J_pseudogene","IG_pseudogene","IG_V_gene","IG_V_pseudogene","TR_C_gene","TR_D_gene","TR_J_gene","TR_J_pseudogene","TR_V_gene","TR_V_pseudogene"]:
        g_lst.append(g_id)
        continue
    elif discard_VDJ and f_type in ['V_gene_segment', 'D_gene_segment', 'J_gene_segment', 'transcript', 'CDS', 'exon']:
      t_id, t_parent = extract_child_annotation(f_annot)
      if t_parent in g_lst and t_id:
        vdj_lst.append(t_id)
        continue
      elif t_parent in vdj_lst:
        exon_lst.append(t_id)
        continue

    if discard_rDNA and f_type == 'gene':
      g_id, g_type = extract_parent_annotation(f_annot)
      if g_type == 'rRNA':
        g_lst.append(g_id)
        continue
    elif discard_rDNA and f_type in ["rRNA", "transcript", 'exon']:
      t_id, t_parent = extract_child_annotation(f_annot)
      if t_parent in g_lst and t_id:
        rDNA_lst.append(t_id)
        continue
      elif t_parent in rDNA_lst:
        exon_lst.append(t_id)
        continue
    out_fh.write(line)
  in_fh.close()
  out_fh.close()