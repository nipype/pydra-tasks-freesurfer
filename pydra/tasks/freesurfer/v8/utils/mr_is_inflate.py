import attrs
from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.abspath(inputs["out_file"])
    if not inputs["no_save_sulc"]:

        outputs["out_sulc"] = os.path.abspath(inputs["out_sulc"])
    return outputs


def out_sulc_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_sulc")


@shell.define(xor=[["out_sulc", "no_save_sulc"]])
class MRIsInflate(shell.Task["MRIsInflate.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.mr_is_inflate import MRIsInflate

    >>> task = MRIsInflate()
    >>> task.inputs.in_file = Pial.mock("lh.pial")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_inflate"
    in_file: Pial = shell.arg(
        help="Input file for MRIsInflate",
        argstr="{in_file}",
        position=-2,
        copy_mode="File.CopyMode.copy",
    )
    out_sulc: Path | None = shell.arg(help="Output sulc file")
    no_save_sulc: bool = shell.arg(
        help="Do not save sulc file as output", argstr="-no-save-sulc"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Output file for MRIsInflate",
            argstr="{out_file}",
            position=-1,
            path_template="{in_file}.inflated",
        )
        out_sulc: File | None = shell.out(
            help="Output sulc file", callable=out_sulc_callable
        )
