from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "l_files" and len(value) == 1:
        value.append("identity.nofile")

    return argstr.format(**inputs)


def l_files_formatter(field, inputs):
    return _format_arg("l_files", field, inputs, argstr="-l {l_files}")


@shell.define
class CARegister(shell.Task["CARegister.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.ca_register import CARegister

    >>> task = CARegister()
    >>> task.in_file = MghGz.mock("norm.mgz")
    >>> task.template = File.mock()
    >>> task.mask = File.mock()
    >>> task.transform = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_ca_register"
    in_file: MghGz = shell.arg(
        help="The input volume for CARegister", argstr="{in_file}", position=-3
    )
    template: File = shell.arg(
        help="The template file in gca format", argstr="{template}", position=-2
    )
    mask: File = shell.arg(
        help="Specifies volume to use as mask", argstr="-mask {mask}"
    )
    invert_and_save: bool = shell.arg(
        help="Invert and save the .m3z multi-dimensional talaraich transform to x, y, and z .mgz files",
        argstr="-invert-and-save",
        position=-4,
    )
    no_big_ventricles: bool = shell.arg(
        help="No big ventricles", argstr="-nobigventricles"
    )
    transform: File = shell.arg(
        help="Specifies transform in lta format", argstr="-T {transform}"
    )
    align: ty.Any = shell.arg(
        help="Specifies when to perform alignment", argstr="-align-{align}"
    )
    levels: int = shell.arg(
        help="defines how many surrounding voxels will be used in interpolations, default is 6",
        argstr="-levels {levels}",
    )
    A: int = shell.arg(
        help="undocumented flag used in longitudinal processing", argstr="-A {A}"
    )
    l_files: list[File] = shell.arg(
        help="undocumented flag used in longitudinal processing",
        formatter="l_files_formatter",
    )
    num_threads: int = shell.arg(help="allows for specifying more threads")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="The output volume for CARegister",
            argstr="{out_file}",
            position=-1,
            path_template="out_file",
        )
