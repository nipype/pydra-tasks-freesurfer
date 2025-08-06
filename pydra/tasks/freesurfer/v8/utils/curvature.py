import attrs
from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if inputs["copy_input"]:
        if name == "in_file":
            basename = os.path.basename(value)
            return argstr.format(**{name: basename})

    return argstr.format(**inputs)


def in_file_formatter(field, inputs):
    return _format_arg("in_file", field, inputs, argstr="{in_file}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    if inputs["copy_input"]:
        in_file = os.path.basename(inputs["in_file"])
    else:
        in_file = inputs["in_file"]
    outputs["out_mean"] = os.path.abspath(in_file) + ".H"
    outputs["out_gauss"] = os.path.abspath(in_file) + ".K"
    return outputs


def out_mean_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_mean")


def out_gauss_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_gauss")


@shell.define
class Curvature(shell.Task["Curvature.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.v8.utils.curvature import Curvature

    >>> task = Curvature()
    >>> task.inputs.in_file = Pial.mock("lh.pial")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_curvature"
    in_file: Pial = shell.arg(
        help="Input file for Curvature",
        position=-2,
        formatter="in_file_formatter",
        copy_mode="File.CopyMode.copy",
    )
    threshold: float = shell.arg(
        help="Undocumented input threshold", argstr="-thresh {threshold:.3}"
    )
    n: bool = shell.arg(help="Undocumented boolean flag", argstr="-n")
    averages: int = shell.arg(
        help="Perform this number iterative averages of curvature measure before saving",
        argstr="-a {averages}",
    )
    save: bool = shell.arg(
        help="Save curvature files (will only generate screen output without this option)",
        argstr="-w",
    )
    distances: ty.Any = shell.arg(
        help="Undocumented input integer distances",
        argstr="-distances {distances[0]} {distances[1]}",
    )
    copy_input: bool = shell.arg(help="Copy input file to current directory")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_mean: File | None = shell.out(
            help="Mean curvature output file", callable=out_mean_callable
        )
        out_gauss: File | None = shell.out(
            help="Gaussian curvature output file", callable=out_gauss_callable
        )
