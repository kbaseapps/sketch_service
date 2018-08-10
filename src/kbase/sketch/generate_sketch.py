import os
import subprocess


def generate_sketch(file_path, paired_end=False):
    """
    Generate a sketch file from a given downloaded fasta/fastq file.
    Args:
      downloaded_file is a DownloadedFile namedtuple defined in ./download_file.py
    Returns the full path of the sketch file
    """
    output_name = os.path.basename(file_path + '.msh')
    output_path = os.path.join(os.path.dirname(file_path), output_name)
    args = ['mash', 'sketch', file_path, '-o', output_path, '-k', '19', '-s', '10000']
    if paired_end:
        # For paired end reads, sketch the reads using -m 2 to improve results by ignoring
        # single-copy k-mers, which are more likely to be erroneous.
        # See docs:
        # http://mash.readthedocs.io/en/latest/tutorials.html#querying-read-sets-against-an-existing-refseq-sketch
        args += ['-m', '2']
    proc = subprocess.Popen(args)
    # TODO error cases
    proc.wait()
    return output_path
