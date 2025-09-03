from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define
class RelabelHypointensities(shell.Task["RelabelHypointensities.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.relabel_hypointensities import RelabelHypointensities

    >>> task = RelabelHypointensities()
    >>> task.lh_white = Pial.mock("lh.pial")
    >>> task.rh_white = File.mock()
    >>> task.aseg = File.mock()
    >>> task.surf_directory = Directory.mock(".")
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_relabel_hypointensities"
    lh_white: Pial = shell.arg(
        help="Implicit input file must be lh.white", copy_mode="File.CopyMode.copy"
    )
    rh_white: File = shell.arg(
        help="Implicit input file must be rh.white", copy_mode="File.CopyMode.copy"
    )
    aseg: File = shell.arg(help="Input aseg file", argstr="{aseg}", position=-3)
    surf_directory: Directory = shell.arg(
        help="Directory containing lh.white and rh.white",
        argstr="{surf_directory}",
        position=-2,
        default=".",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Output aseg file",
            argstr="{out_file}",
            position=-1,
            path_template="{aseg}.hypos.mgz",
        )
