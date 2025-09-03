import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
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
    if inputs["log_file"] is not attrs.NOTHING:
        outputs["log_file"] = os.path.abspath(inputs["log_file"])
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


def log_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("log_file")


@shell.define
class MRIFill(shell.Task["MRIFill.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.mri_fill import MRIFill

    >>> task = MRIFill()
    >>> task.in_file = MghGz.mock("wm.mgz" # doctest: +SKIP)
    >>> task.segmentation = File.mock()
    >>> task.transform = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_fill"
    in_file: MghGz = shell.arg(
        help="Input white matter file", argstr="{in_file}", position=-2
    )
    out_file: Path = shell.arg(
        help="Output filled volume file name for MRIFill",
        argstr="{out_file}",
        position=-1,
    )
    segmentation: File = shell.arg(
        help="Input segmentation file for MRIFill",
        argstr="-segmentation {segmentation}",
    )
    transform: File = shell.arg(
        help="Input transform file for MRIFill", argstr="-xform {transform}"
    )
    log_file: Path = shell.arg(
        help="Output log file for MRIFill", argstr="-a {log_file}"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="Output file from MRIFill", callable=out_file_callable
        )
        log_file: File | None = shell.out(
            help="Output log file from MRIFill", callable=log_file_callable
        )
