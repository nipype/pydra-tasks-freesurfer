from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define
class EMRegister(shell.Task["EMRegister.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.registration.em_register import EMRegister

    >>> task = EMRegister()
    >>> task.in_file = MghGz.mock("norm.mgz")
    >>> task.template = File.mock()
    >>> task.out_file = "norm_transform.lta"
    >>> task.mask = File.mock()
    >>> task.nbrspacing = 9
    >>> task.transform = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_em_register"
    in_file: MghGz = shell.arg(help="in brain volume", argstr="{in_file}", position=-3)
    template: File = shell.arg(help="template gca", argstr="{template}", position=-2)
    skull: bool = shell.arg(
        help="align to atlas containing skull (uns=5)", argstr="-skull"
    )
    mask: File = shell.arg(help="use volume as a mask", argstr="-mask {mask}")
    nbrspacing: int = shell.arg(
        help="align to atlas containing skull setting unknown_nbr_spacing = nbrspacing",
        argstr="-uns {nbrspacing}",
    )
    transform: File = shell.arg(
        help="Previously computed transform", argstr="-t {transform}"
    )
    num_threads: int = shell.arg(help="allows for specifying more threads")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="output transform",
            argstr="{out_file}",
            position=-1,
            path_template="{in_file}_transform.lta",
        )
