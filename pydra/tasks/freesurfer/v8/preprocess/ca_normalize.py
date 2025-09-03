import attrs
from fileformats.datascience import TextMatrix
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
    outputs["control_points"] = os.path.abspath(inputs["control_points"])
    return outputs


def control_points_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("control_points")


@shell.define
class CANormalize(shell.Task["CANormalize.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.ca_normalize import CANormalize

    >>> task = CANormalize()
    >>> task.in_file = MghGz.mock("T1.mgz")
    >>> task.atlas = File.mock()
    >>> task.transform = TextMatrix.mock("trans.mat" # in practice use .lta transforms)
    >>> task.mask = File.mock()
    >>> task.long_file = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_ca_normalize"
    in_file: MghGz = shell.arg(
        help="The input file for CANormalize", argstr="{in_file}", position=-4
    )
    atlas: File = shell.arg(
        help="The atlas file in gca format", argstr="{atlas}", position=-3
    )
    transform: TextMatrix = shell.arg(
        help="The transform file in lta format", argstr="{transform}", position=-2
    )
    mask: File = shell.arg(
        help="Specifies volume to use as mask", argstr="-mask {mask}"
    )
    control_points: Path = shell.arg(
        help="File name for the output control points", argstr="-c {control_points}"
    )
    long_file: File = shell.arg(
        help="undocumented flag used in longitudinal processing",
        argstr="-long {long_file}",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="The output file for CANormalize",
            argstr="{out_file}",
            position=-1,
            path_template="{in_file}_norm",
        )
        control_points: File | None = shell.out(
            help="The output control points for Normalize",
            callable=control_points_callable,
        )
