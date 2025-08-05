from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pathlib._local import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define
class Normalize(shell.Task["Normalize.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib._local import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.normalize import Normalize

    >>> task = Normalize()
    >>> task.inputs.in_file = MghGz.mock("T1.mgz")
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.segmentation = File.mock()
    >>> task.inputs.transform = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_normalize"
    in_file: MghGz = shell.arg(
        help="The input file for Normalize", argstr="{in_file}", position=-2
    )
    gradient: int = shell.arg(
        help="use max intensity/mm gradient g (default=1)", argstr="-g {gradient}"
    )
    mask: File = shell.arg(
        help="The input mask file for Normalize", argstr="-mask {mask}"
    )
    segmentation: File = shell.arg(
        help="The input segmentation for Normalize", argstr="-aseg {segmentation}"
    )
    transform: File = shell.arg(help="Transform file from the header of the input file")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="The output file for Normalize",
            argstr="{out_file}",
            position=-1,
            path_template="{in_file}_norm",
        )
