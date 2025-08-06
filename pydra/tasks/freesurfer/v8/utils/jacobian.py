from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define
class Jacobian(shell.Task["Jacobian.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.jacobian import Jacobian

    >>> task = Jacobian()
    >>> task.inputs.in_origsurf = Pial.mock("lh.pial")
    >>> task.inputs.in_mappedsurf = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_jacobian"
    in_origsurf: Pial = shell.arg(
        help="Original surface", argstr="{in_origsurf}", position=-3
    )
    in_mappedsurf: File = shell.arg(
        help="Mapped surface", argstr="{in_mappedsurf}", position=-2
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Output Jacobian of the surface mapping",
            argstr="{out_file}",
            position=-1,
            path_template="{in_origsurf}.jacobian",
        )
