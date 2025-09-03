from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define
class RemoveNeck(shell.Task["RemoveNeck.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.remove_neck import RemoveNeck

    >>> task = RemoveNeck()
    >>> task.in_file = MghGz.mock("norm.mgz")
    >>> task.transform = File.mock()
    >>> task.template = TextMatrix.mock("trans.mat")
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_remove_neck norm.mgz trans.mat trans.mat norm_noneck.mgz'


    """

    executable = "mri_remove_neck"
    in_file: MghGz = shell.arg(
        help="Input file for RemoveNeck", argstr="{in_file}", position=-4
    )
    transform: File = shell.arg(
        help="Input transform file for RemoveNeck", argstr="{transform}", position=-3
    )
    template: TextMatrix = shell.arg(
        help="Input template file for RemoveNeck", argstr="{template}", position=-2
    )
    radius: int = shell.arg(help="Radius", argstr="-radius {radius}")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Output file for RemoveNeck",
            argstr="{out_file}",
            position=-1,
            path_template="{in_file}_noneck",
        )
