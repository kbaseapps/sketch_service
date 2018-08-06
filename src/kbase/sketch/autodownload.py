import kbase_workspace_utils as ws


# String patterns for every downloadable workspace type that this service can support
valid_types = {
    'reads_paired': 'PairedEndLibrary-2.0',
    'reads_single': 'SingleEndLibrary-2.0',
    'genome': 'Genome',
    'assembly': 'KBaseGenomeAnnotations.Assembly',
    'assembly_legacy': 'ContigSet'
}


def autodownload(ref, save_dir):
    """
    Autodownload the fasta/fastq file for a Genome, Reads, or Assembly.
    Args:
      ref is a workspace reference ID in the form 'workspace_id/object_id/version'
      save_dir is the path of a directory in which to save the downloaded file
    Returns a tuple of (file_path, paired_end)
      file_path is the string path of the saved file
      paired_end is a boolean indicating if these are paired-end reads
    The generate_sketch function needs to know if it's working with paired-end reads or not
    """
    ws_obj = ws.download_obj(ref=ref)
    ws_type = ws_obj['data'][0]['info'][2]
    if valid_types['reads_paired'] in ws_type:
        paths = ws.download_reads(ref=ref, save_dir=save_dir)
        output_path = paths[0].replace(".paired.fwd.fastq", ".fastq")
        concatenate_files(paths, output_path)
        return (output_path, True)
    elif valid_types['reads_single'] in ws_type:
        paths = ws.download_reads(ref=ref, save_dir=save_dir)
        output_path = paths[0]
        return (output_path, False)
    elif valid_types['genome'] in ws_type:
        assembly_ref = ws.get_assembly_from_genome(ref)
        path = ws.download_assembly(assembly_ref, save_dir)
        return (path, False)
    elif valid_types['assembly'] in ws_type or valid_types['assembly_legacy'] in ws_type:
        path = ws.download_assembly(assembly_ref, save_dir)
        return (path, False)
    else:
        raise UnrecognizedWSType(ws_type)


def concatenate_files(input_paths, output_path):
    """Cat all the contents of the input paths into the output path."""
    with open(output_path, 'wb') as wfile:
        for path in input_paths:
            with open(path, 'rb') as fread:
                for line in fread:
                    wfile.write(line)


class UnrecognizedWSType(Exception):
    """An attempt to use the service on a type that we cannot handle."""

    def __init__(self, typ):
            self.typ = typ

    def __str__(self):
        return ("Unable to handle type: " + self.typ +
                ". Valid types are: " + str(valid_types.values()))
