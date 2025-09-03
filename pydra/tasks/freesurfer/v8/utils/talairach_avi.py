import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.abspath(inputs["out_file"])
    outputs["out_log"] = os.path.abspath("talairach_avi.log")
    outputs["out_txt"] = os.path.join(
        os.path.dirname(inputs["out_file"]),
        "talsrcimg_to_" + str(inputs["atlas"]) + "t4_vox2vox.txt",
    )
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


def out_log_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_log")


def out_txt_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_txt")


@shell.define
class TalairachAVI(shell.Task["TalairachAVI.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.talairach_avi import TalairachAVI

    >>> task = TalairachAVI()
    >>> task.in_file = MghGz.mock("norm.mgz")
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'talairach_avi --i norm.mgz --xfm trans.mat'


    """

    executable = "talairach_avi"
    in_file: MghGz = shell.arg(help="input volume", argstr="--i {in_file}")
    out_file: Path = shell.arg(help="output xfm file", argstr="--xfm {out_file}")
    atlas: ty.Any = shell.arg(
        help="alternate target atlas (in freesurfer/average dir)",
        argstr="--atlas {atlas}",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="The output transform for TalairachAVI", callable=out_file_callable
        )
        out_log: File | None = shell.out(
            help="The output log file for TalairachAVI", callable=out_log_callable
        )
        out_txt: File | None = shell.out(
            help="The output text file for TaliarachAVI", callable=out_txt_callable
        )
