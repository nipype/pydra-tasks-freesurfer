import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "transform":
        return value  # os.path.abspath(value)

    return argstr.format(**inputs)


def transform_formatter(field, inputs):
    return _format_arg("transform", field, inputs, argstr="{transform}")


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


@shell.define
class AddXFormToHeader(shell.Task["AddXFormToHeader.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.add_x_form_to_header import AddXFormToHeader

    >>> task = AddXFormToHeader()
    >>> task.in_file = MghGz.mock("norm.mgz")
    >>> task.transform = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    >>> task = AddXFormToHeader()
    >>> task.in_file = MghGz.mock()
    >>> task.transform = File.mock()
    >>> task.copy_name = True
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_add_xform_to_header -c trans.mat norm.mgz output.mgz'


    """

    executable = "mri_add_xform_to_header"
    in_file: MghGz = shell.arg(help="input volume", argstr="{in_file}", position=-2)
    transform: File = shell.arg(
        help="xfm file", position=-3, formatter="transform_formatter"
    )
    out_file: Path = shell.arg(
        help="output volume", argstr="{out_file}", position=-1, default="output.mgz"
    )
    copy_name: bool = shell.arg(
        help="do not try to load the xfmfile, just copy name", argstr="-c"
    )
    verbose: bool = shell.arg(help="be verbose", argstr="-v")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="output volume", callable=out_file_callable
        )
