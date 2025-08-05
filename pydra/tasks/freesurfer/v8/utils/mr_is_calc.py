import attrs
from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Area
import logging
import os
from pathlib import Path
from pathlib._local import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.abspath(inputs["out_file"])
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


@shell.define(xor=[["in_float", "in_int", "in_file2"]])
class MRIsCalc(shell.Task["MRIsCalc.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Area
    >>> from pathlib._local import Path
    >>> from pydra.tasks.freesurfer.v8.utils.mr_is_calc import MRIsCalc

    >>> task = MRIsCalc()
    >>> task.inputs.in_file1 = Area.mock("lh.area" # doctest: +SKIP)
    >>> task.inputs.action = "add"
    >>> task.inputs.in_file2 = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_calc"
    in_file1: Area = shell.arg(help="Input file 1", argstr="{in_file1}", position=-3)
    action: ty.Any = shell.arg(
        help="Action to perform on input file(s)", argstr="{action}", position=-2
    )
    out_file: Path = shell.arg(
        help="Output file after calculation", argstr="-o {out_file}"
    )
    in_file2: File | None = shell.arg(
        help="Input file 2", argstr="{in_file2}", position=-1
    )
    in_float: float | None = shell.arg(
        help="Input float", argstr="{in_float}", position=-1
    )
    in_int: int | None = shell.arg(help="Input integer", argstr="{in_int}", position=-1)
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="Output file after calculation", callable=out_file_callable
        )
