import os
import subprocess  # nosec
import requests


def generate_sketch(file_path, search_db, paired_end=False):
    """
    Generate a sketch file from a given downloaded fasta/fastq file.
    Args:
      downloaded_file is a DownloadedFile namedtuple defined in ./download_file.py
    Returns the full path of the sketch file
    """
    # first thing we want to do is query for the k-mer size.
    resp = requests.get('https://homology.kbase.us/namespace/{}/'.format(search_db))
    json_resp = resp.json()
    if json_resp.get('sketchsize'):
        sketchsize = str(json_resp['sketchsize'])
    else:
        sketchsize = '10000'
    if json_resp.get('kmersize'):
        kmersize = str(json_resp['kmersize'][0])
    else:
        kmersize = '19'
    output_name = os.path.basename(file_path + '.msh')
    output_path = os.path.join(os.path.dirname(file_path), output_name)
    args = ['mash', 'sketch', file_path, '-o', output_path, '-k', kmersize, '-s', sketchsize]
    if paired_end:
        # For paired end reads, sketch the reads using -m 2 to improve results by ignoring
        # single-copy k-mers, which are more likely to be erroneous.
        # See docs:
        # http://mash.readthedocs.io/en/latest/tutorials.html#querying-read-sets-against-an-existing-refseq-sketch
        args += ['-m', '2']
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # nosec
    (stdout, stderr) = proc.communicate()
    print('-' * 80)
    print('Sketch generation output:')
    print(stdout)
    print(stderr)
    print('-' * 80)
    if proc.returncode != 0:
        raise Exception("Error generating sketch data.")
    return output_path
