import attrs
from fileformats.generic import Directory, File
from fileformats.text import TextFile
import logging
import os
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["log_file"] = os.path.abspath("output.nipype")
    return outputs


def log_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("log_file")


@shell.define
class TalairachQC(shell.Task["TalairachQC.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.freesurfer.v8.utils.talairach_qc import TalairachQC

    >>> task = TalairachQC()
    >>> task.log_file = File.mock("dirs.txt")
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'tal_QC_AZS dirs.txt'


    """

    executable = "tal_QC_AZS"
    log_file: File = shell.arg(
        help="The log file for TalairachQC", argstr="{log_file}", position=1
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        log_file: TextFile | None = shell.out(
            help="The output log", callable=log_file_callable
        )
