from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


@shell.define
class MRIPretess(shell.Task["MRIPretess.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.mri_pretess import MRIPretess

    >>> task = MRIPretess()
    >>> task.in_filled = MghGz.mock("wm.mgz")
    >>> task.in_norm = File.mock()
    >>> task.nocorners = True
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_pretess"
    in_filled: MghGz = shell.arg(
        help="filled volume, usually wm.mgz", argstr="{in_filled}", position=-4
    )
    label: ty.Any | None = shell.arg(
        help="label to be picked up, can be a Freesurfer's string like 'wm' or a label value (e.g. 127 for rh or 255 for lh)",
        argstr="{label}",
        position=-3,
        default="wm",
    )
    in_norm: File = shell.arg(
        help="the normalized, brain-extracted T1w image. Usually norm.mgz",
        argstr="{in_norm}",
        position=-2,
    )
    nocorners: bool = shell.arg(
        help="do not remove corner configurations in addition to edge ones.",
        argstr="-nocorners",
    )
    keep: bool = shell.arg(help="keep WM edits", argstr="-keep")
    test: bool = shell.arg(
        help="adds a voxel that should be removed by mri_pretess. The value of the voxel is set to that of an ON-edited WM, so it should be kept with -keep. The output will NOT be saved.",
        argstr="-test",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="the output file after mri_pretess.",
            argstr="{out_file}",
            position=-1,
            path_template="{in_filled}_pretesswm",
        )
