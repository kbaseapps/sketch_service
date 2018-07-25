import subprocess
from collections import namedtuple

SketchResult = namedtuple('SketchResult', ['path', 'file_name'])


def generate_sketch(downloaded_file):
    """
    Generate a sketch file from a given downloaded fasta/fastq file.
    Args:
      downloaded_file is a DownloadedFile namedtuple defined in ./download_file.py
    Returns a SketchResult namedtuple (see the definition above)
    """
    output_name = downloaded_file.file_name + '.msh'
    output_path = downloaded_file.file_path + '.msh'
    args = ['mash', 'sketch', downloaded_file.file_path, '-o', output_path, '-k', "31"]
    proc = subprocess.Popen(args)
    # TODO error cases
    proc.wait()
    sketch_result = SketchResult(path=output_path, file_name=output_name)
    return sketch_result
