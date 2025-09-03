import attrs
from fileformats.generic import Directory
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["average_subject_name"] = inputs["out_name"]
    return outputs


def average_subject_name_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("average_subject_name")


@shell.define
class MakeAverageSubject(shell.Task["MakeAverageSubject.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.make_average_subject import MakeAverageSubject

    >>> task = MakeAverageSubject()
    >>> task.subjects_ids = ["s1", "s2"]
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'make_average_subject --out average --subjects s1 s2'


    """

    executable = "make_average_subject"
    subjects_ids: list[str] = shell.arg(
        help="freesurfer subjects ids to average",
        argstr="--subjects {subjects_ids}",
        sep=" ",
    )
    out_name: Path = shell.arg(
        help="name for the average subject",
        argstr="--out {out_name}",
        default="average",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        average_subject_name: str | None = shell.out(
            help="Output registration file", callable=average_subject_name_callable
        )
