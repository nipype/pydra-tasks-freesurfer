import attrs
from fileformats.generic import Directory
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import fname_presuffix
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "resampled_file":
        return _get_outfilename(
            in_file=inputs["in_file"], resampled_file=inputs["resampled_file"]
        )
    return None


def resampled_file_default(inputs):
    return _gen_filename("resampled_file", inputs=inputs)


@shell.define
class Resample(shell.Task["Resample.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.resample import Resample

    >>> task = Resample()
    >>> task.in_file = Nifti1.mock("structural.nii")
    >>> task.voxel_size = (2.1, 2.1, 2.1)
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_convert -vs 2.10 2.10 2.10 -i structural.nii -o resampled.nii'


    """

    executable = "mri_convert"
    in_file: Nifti1 = shell.arg(
        help="file to resample", argstr="-i {in_file}", position=-2
    )
    voxel_size: ty.Any = shell.arg(
        help="triplet of output voxel sizes",
        argstr="-vs {voxel_size[0]:.2} {voxel_size[1]:.2} {voxel_size[2]:.2}",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        resampled_file: Path = shell.outarg(
            help="output filename",
            argstr="-o {resampled_file}",
            position=-1,
            path_template="resampled_file",
        )


def _get_outfilename(in_file=None, resampled_file=None):
    if resampled_file is not attrs.NOTHING:
        outfile = resampled_file
    else:
        outfile = fname_presuffix(in_file, newpath=output_dir, suffix="_resample")
    return outfile
