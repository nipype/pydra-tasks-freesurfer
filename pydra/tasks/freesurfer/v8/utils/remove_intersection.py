from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define
class RemoveIntersection(shell.Task["RemoveIntersection.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.remove_intersection import RemoveIntersection

    >>> task = RemoveIntersection()
    >>> task.in_file = Pial.mock("lh.pial")
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_remove_intersection"
    in_file: Pial = shell.arg(
        help="Input file for RemoveIntersection",
        argstr="{in_file}",
        position=-2,
        copy_mode="File.CopyMode.copy",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Output file for RemoveIntersection",
            argstr="{out_file}",
            position=-1,
            path_template="{in_file}",
        )
