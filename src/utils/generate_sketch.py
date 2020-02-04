import os
import subprocess  # nosec
import requests

from src.config import load_config


def generate_sketch(file_path, search_db, paired_end=False):
    """
    Generate a sketch file from a given downloaded fasta/fastq file.
    Args:
      downloaded_file is a DownloadedFile namedtuple defined in ./download_file.py
    Returns the full path of the sketch file
    """
    config = load_config()
    # Fetch the k-mer size
    url = f"{config['homology_url']}/namespace/{search_db}"
    resp = requests.get(url)
    json_resp = resp.json()
    sketch_size = str(json_resp.get('sketchsize', 10000))
    kmer_size = str(json_resp.get('kmersize', 19))
    output_name = os.path.basename(file_path + '.msh')
    output_path = os.path.join(os.path.dirname(file_path), output_name)
    args = ['mash', 'sketch', file_path, '-o', output_path, '-k', kmer_size, '-s', sketch_size]
    print(f"Generating sketch with command: {' '.join(args)}")
    if paired_end:
        # For paired end reads, sketch the reads using -m 2 to improve results by ignoring
        # single-copy k-mers, which are more likely to be erroneous.
        # See docs:
        # http://mash.readthedocs.io/en/latest/tutorials.html#querying-read-sets-against-an-existing-refseq-sketch
        args += ['-m', '2']
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # nosec
    (stdout, stderr) = proc.communicate()
    print('-' * 80)
    print('mash output:')
    print(stdout)
    print(stderr)
    print('-' * 80)
    if proc.returncode != 0:
        raise Exception(f"Error generating sketch data: {stderr}")
    return output_path
