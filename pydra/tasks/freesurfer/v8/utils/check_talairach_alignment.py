import attrs
from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
import logging
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = inputs["in_file"]
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


@shell.define(xor=[["in_file", "subject"]])
class CheckTalairachAlignment(shell.Task["CheckTalairachAlignment.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.v8.utils.check_talairach_alignment import CheckTalairachAlignment

    >>> task = CheckTalairachAlignment()
    >>> task.in_file = TextMatrix.mock("trans.mat")
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'talairach_afd -T 0.005 -xfm trans.mat'


    """

    executable = "talairach_afd"
    in_file: TextMatrix | None = shell.arg(
        help="specify the talairach.xfm file to check",
        argstr="-xfm {in_file}",
        position=-1,
    )
    subject: ty.Any | None = shell.arg(
        help="specify subject's name", argstr="-subj {subject}", position=-1
    )
    threshold: float = shell.arg(
        help="Talairach transforms for subjects with p-values <= T are considered as very unlikely default=0.010",
        argstr="-T {threshold:.3}",
        default=0.01,
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="The input file for CheckTalairachAlignment",
            callable=out_file_callable,
        )
