import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Lta
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
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


@shell.define
class WatershedSkullStrip(shell.Task["WatershedSkullStrip.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Lta
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.watershed_skull_strip import WatershedSkullStrip

    >>> task = WatershedSkullStrip()
    >>> task.inputs.in_file = MghGz.mock("T1.mgz")
    >>> task.inputs.brain_atlas = File.mock()
    >>> task.inputs.transform = Lta.mock("transforms/talairach_with_skull.lta")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_watershed"
    in_file: MghGz = shell.arg(help="input volume", argstr="{in_file}", position=-2)
    out_file: Path | None = shell.arg(
        help="output volume",
        argstr="{out_file}",
        position=-1,
        default="brainmask.auto.mgz",
    )
    t1: bool = shell.arg(
        help="specify T1 input volume (T1 grey value = 110)", argstr="-T1"
    )
    brain_atlas: File = shell.arg(
        help="", argstr="-brain_atlas {brain_atlas}", position=-4
    )
    transform: Lta = shell.arg(help="undocumented", argstr="{transform}", position=-3)
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="skull stripped brain volume", callable=out_file_callable
        )
