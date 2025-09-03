import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.text import TextFile
import logging
import os
import os.path
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


def log_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("log_file")


@shell.define
class RegisterAVItoTalairach(shell.Task["RegisterAVItoTalairach.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.text import TextFile
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.registration.register_av_ito_talairach import RegisterAVItoTalairach

    >>> task = RegisterAVItoTalairach()
    >>> task.in_file = MghGz.mock("structural.mgz"                         # doctest: +SKIP)
    >>> task.target = File.mock()
    >>> task.vox2vox = TextFile.mock("talsrcimg_to_structural_t4_vox2vox.txt" # doctest: +SKIP)
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'avi2talxfm structural.mgz mni305.cor.mgz talsrcimg_to_structural_t4_vox2vox.txt talairach.auto.xfm'


    """

    executable = "avi2talxfm"
    in_file: MghGz = shell.arg(help="The input file", argstr="{in_file}", position=1)
    target: File = shell.arg(help="The target file", argstr="{target}", position=2)
    vox2vox: TextFile = shell.arg(
        help="The vox2vox file", argstr="{vox2vox}", position=3
    )
    out_file: Path = shell.arg(
        help="The transform output",
        argstr="{out_file}",
        position=4,
        default="talairach.auto.xfm",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="The output file for RegisterAVItoTalairach",
            callable=out_file_callable,
        )
        log_file: File | None = shell.out(
            help="The output log", callable=log_file_callable
        )
