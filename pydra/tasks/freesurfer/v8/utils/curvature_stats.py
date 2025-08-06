from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name in ["surface", "curvfile1", "curvfile2"]:
        prefix = os.path.basename(value).split(".")[1]
        return argstr.format(**{name: prefix})

    return argstr.format(**inputs)


@shell.define
class CurvatureStats(shell.Task["CurvatureStats.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.curvature_stats import CurvatureStats

    >>> task = CurvatureStats()
    >>> task.inputs.surface = File.mock()
    >>> task.inputs.curvfile1 = File.mock()
    >>> task.inputs.curvfile2 = Pial.mock("lh.pial")
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.out_file = "lh.curv.stats"
    >>> task.inputs.min_max = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_curvature_stats"
    surface: File = shell.arg(
        help="Specify surface file for CurvatureStats", argstr="-F {surface}"
    )
    curvfile1: File = shell.arg(
        help="Input file for CurvatureStats", argstr="{curvfile1}", position=-2
    )
    curvfile2: Pial = shell.arg(
        help="Input file for CurvatureStats", argstr="{curvfile2}", position=-1
    )
    hemisphere: ty.Any = shell.arg(
        help="Hemisphere being processed", argstr="{hemisphere}", position=-3
    )
    subject_id: ty.Any | None = shell.arg(
        help="Subject being processed",
        argstr="{subject_id}",
        position=-4,
        default="subject_id",
    )
    min_max: bool = shell.arg(
        help="Output min / max information for the processed curvature.", argstr="-m"
    )
    values: bool = shell.arg(
        help="Triggers a series of derived curvature values", argstr="-G"
    )
    write: bool = shell.arg(
        help="Write curvature files", argstr="--writeCurvatureFiles"
    )
    copy_inputs: bool = shell.arg(
        help="If running as a node, set this to True. This will copy the input files to the node  directory."
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Output curvature stats file",
            argstr="-o {out_file}",
            path_template="{hemisphere}.curv.stats",
        )
