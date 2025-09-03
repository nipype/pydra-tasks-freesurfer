import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "concatenated_file":
        return _list_outputs(concatenated_file=inputs["concatenated_file"])[name]
    return None


def concatenated_file_default(inputs):
    return _gen_filename("concatenated_file", inputs=inputs)


@shell.define
class Concatenate(shell.Task["Concatenate.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.model.concatenate import Concatenate

    >>> task = Concatenate()
    >>> task.in_files = [Nifti1.mock("cont1.nii"), Nifti1.mock("cont2.nii")]
    >>> task.multiply_matrix_file = File.mock()
    >>> task.mask_file = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_concat --o bar.nii --i cont1.nii --i cont2.nii'


    """

    executable = "mri_concat"
    in_files: list[Nifti1] = shell.arg(
        help="Individual volumes to be concatenated", argstr="--i {in_files}..."
    )
    sign: ty.Any = shell.arg(
        help="Take only pos or neg voxles from input, or take abs", argstr="--{sign}"
    )
    stats: ty.Any = shell.arg(
        help="Compute the sum, var, std, max, min or mean of the input volumes",
        argstr="--{stats}",
    )
    paired_stats: ty.Any = shell.arg(
        help="Compute paired sum, avg, or diff", argstr="--paired-{paired_stats}"
    )
    gmean: int = shell.arg(
        help="create matrix to average Ng groups, Nper=Ntot/Ng",
        argstr="--gmean {gmean}",
    )
    mean_div_n: bool = shell.arg(
        help="compute mean/nframes (good for var)", argstr="--mean-div-n"
    )
    multiply_by: float = shell.arg(
        help="Multiply input volume by some amount", argstr="--mul {multiply_by}"
    )
    add_val: float = shell.arg(
        help="Add some amount to the input volume", argstr="--add {add_val}"
    )
    multiply_matrix_file: File = shell.arg(
        help="Multiply input by an ascii matrix in file",
        argstr="--mtx {multiply_matrix_file}",
    )
    combine_: bool = shell.arg(
        help="Combine non-zero values into single frame volume", argstr="--combine"
    )
    keep_dtype: bool = shell.arg(
        help="Keep voxelwise precision type (default is float", argstr="--keep-datatype"
    )
    max_bonfcor: bool = shell.arg(
        help="Compute max and bonferroni correct (assumes -log10(ps))",
        argstr="--max-bonfcor",
    )
    max_index: bool = shell.arg(
        help="Compute the index of max voxel in concatenated volumes",
        argstr="--max-index",
    )
    mask_file: File = shell.arg(
        help="Mask input with a volume", argstr="--mask {mask_file}"
    )
    vote: bool = shell.arg(
        help="Most frequent value at each voxel and fraction of occurrences",
        argstr="--vote",
    )
    sort: bool = shell.arg(
        help="Sort each voxel by ascending frame value", argstr="--sort"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        concatenated_file: Path = shell.outarg(
            help="Output volume",
            argstr="--o {concatenated_file}",
            path_template="concatenated_file",
        )


def _list_outputs(concatenated_file=None):
    outputs = {}

    fname = concatenated_file
    if fname is attrs.NOTHING:
        fname = "concat_output.nii.gz"
    outputs["concatenated_file"] = os.path.join(output_dir, fname)
    return outputs
