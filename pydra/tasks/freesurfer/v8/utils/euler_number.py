import attrs
from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["defects"] = parsed_inputs["_defects"]
    outputs["euler"] = 2 - (2 * parsed_inputs["_defects"])
    return outputs


def euler_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("euler")


def defects_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("defects")


@shell.define
class EulerNumber(shell.Task["EulerNumber.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.v8.utils.euler_number import EulerNumber

    >>> task = EulerNumber()
    >>> task.inputs.in_file = Pial.mock("lh.pial")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_euler_number"
    in_file: Pial = shell.arg(
        help="Input file for EulerNumber", argstr="{in_file}", position=-1
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        euler: int | None = shell.out(
            help="Euler number of cortical surface. A value of 2 signals a topologically correct surface model with no holes",
            callable=euler_callable,
        )
        defects: int | None = shell.out(
            help="Number of defects", callable=defects_callable
        )
