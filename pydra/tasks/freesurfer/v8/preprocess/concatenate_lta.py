from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Lta
import logging
from pathlib import Path
from pathlib._local import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "out_type":
        value = {"VOX2VOX": 0, "RAS2RAS": 1}[value]

    return argstr.format(**inputs)


def out_type_formatter(field, inputs):
    return _format_arg("out_type", field, inputs, argstr="-out_type {out_type}")


@shell.define
class ConcatenateLTA(shell.Task["ConcatenateLTA.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Lta
    >>> from pathlib._local import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.concatenate_lta import ConcatenateLTA

    >>> task = ConcatenateLTA()
    >>> task.inputs.in_lta1 = Lta.mock("lta1.lta")
    >>> task.inputs.tal_source_file = File.mock()
    >>> task.inputs.tal_template_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    >>> task = ConcatenateLTA()
    >>> task.inputs.in_lta1 = Lta.mock()
    >>> task.inputs.in_lta2 = "identity.nofile"
    >>> task.inputs.out_file = "inv1.lta"
    >>> task.inputs.tal_source_file = File.mock()
    >>> task.inputs.tal_template_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_concatenate_lta -invert1 lta1.lta identity.nofile inv1.lta'


    >>> task = ConcatenateLTA()
    >>> task.inputs.in_lta1 = Lta.mock()
    >>> task.inputs.out_type = "RAS2RAS"
    >>> task.inputs.tal_source_file = File.mock()
    >>> task.inputs.tal_template_file = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_concatenate_lta -invert1 -out_type 1 lta1.lta identity.nofile inv1.lta'


    """

    executable = "mri_concatenate_lta"
    in_lta1: Lta = shell.arg(
        help="maps some src1 to dst1", argstr="{in_lta1}", position=-3
    )
    in_lta2: ty.Any = shell.arg(
        help="maps dst1(src2) to dst2", argstr="{in_lta2}", position=-2
    )
    invert_1: bool = shell.arg(
        help="invert in_lta1 before applying it", argstr="-invert1"
    )
    invert_2: bool = shell.arg(
        help="invert in_lta2 before applying it", argstr="-invert2"
    )
    invert_out: bool = shell.arg(help="invert output LTA", argstr="-invertout")
    out_type: ty.Any = shell.arg(
        help="set final LTA type", formatter="out_type_formatter"
    )
    tal_source_file: File = shell.arg(
        help="if in_lta2 is talairach.xfm, specify source for talairach",
        argstr="-tal {tal_source_file}",
        position=-5,
        requires=["tal_template_file"],
    )
    tal_template_file: File = shell.arg(
        help="if in_lta2 is talairach.xfm, specify template for talairach",
        argstr="{tal_template_file}",
        position=-4,
        requires=["tal_source_file"],
    )
    subject: str = shell.arg(
        help="set subject in output LTA", argstr="-subject {subject}"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="the combined LTA maps: src1 to dst2 = LTA2*LTA1",
            argstr="{out_file}",
            position=-1,
            path_template="{in_lta1}_concat",
        )
