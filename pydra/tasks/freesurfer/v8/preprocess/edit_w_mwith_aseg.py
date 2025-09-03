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
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


@shell.define
class EditWMwithAseg(shell.Task["EditWMwithAseg.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.edit_w_mwith_aseg import EditWMwithAseg

    >>> task = EditWMwithAseg()
    >>> task.in_file = MghGz.mock("T1.mgz")
    >>> task.brain_file = File.mock()
    >>> task.seg_file = MghGz.mock("aseg.mgz")
    >>> task.keep_in = True
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_edit_wm_with_aseg"
    in_file: MghGz = shell.arg(
        help="Input white matter segmentation file", argstr="{in_file}", position=-4
    )
    brain_file: File = shell.arg(
        help="Input brain/T1 file", argstr="{brain_file}", position=-3
    )
    seg_file: MghGz = shell.arg(
        help="Input presurf segmentation file", argstr="{seg_file}", position=-2
    )
    out_file: Path = shell.arg(
        help="File to be written as output", argstr="{out_file}", position=-1
    )
    keep_in: bool = shell.arg(
        help="Keep edits as found in input volume", argstr="-keep-in"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="Output edited WM file", callable=out_file_callable
        )
