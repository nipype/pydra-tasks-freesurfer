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
class Apas2Aseg(shell.Task["Apas2Aseg.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.apas_2_aseg import Apas2Aseg

    >>> task = Apas2Aseg()
    >>> task.in_file = MghGz.mock("aseg.mgz")
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "apas2aseg"
    in_file: MghGz = shell.arg(help="Input aparc+aseg.mgz", argstr="--i {in_file}")
    out_file: Path = shell.arg(help="Output aseg file", argstr="--o {out_file}")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="Output aseg file", callable=out_file_callable
        )
