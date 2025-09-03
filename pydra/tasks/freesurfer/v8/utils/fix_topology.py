import attrs
from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Nofix, Orig
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "sphere":

        suffix = os.path.basename(value).split(".", 1)[1]
        return argstr.format(**{name: suffix})

    return argstr.format(**inputs)


def sphere_formatter(field, inputs):
    return _format_arg("sphere", field, inputs, argstr="-sphere {sphere}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.abspath(inputs["in_orig"])
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


@shell.define
class FixTopology(shell.Task["FixTopology.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Nofix, Orig
    >>> from pydra.tasks.freesurfer.v8.utils.fix_topology import FixTopology

    >>> task = FixTopology()
    >>> task.in_orig = Orig.mock("lh.orig" # doctest: +SKIP)
    >>> task.in_inflated = File.mock()
    >>> task.in_brain = File.mock()
    >>> task.in_wm = File.mock()
    >>> task.subject_id = "10335"
    >>> task.ga = True
    >>> task.sphere = Nofix.mock("lh.qsphere.nofix" # doctest: +SKIP)
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_fix_topology"
    in_orig: Orig = shell.arg(help="Undocumented input file <hemisphere>.orig")
    in_inflated: File = shell.arg(help="Undocumented input file <hemisphere>.inflated")
    in_brain: File = shell.arg(help="Implicit input brain.mgz")
    in_wm: File = shell.arg(help="Implicit input wm.mgz")
    hemisphere: ty.Any = shell.arg(
        help="Hemisphere being processed", argstr="{hemisphere}", position=-1
    )
    subject_id: ty.Any | None = shell.arg(
        help="Subject being processed",
        argstr="{subject_id}",
        position=-2,
        default="subject_id",
    )
    copy_inputs: bool = shell.arg(
        help="If running as a node, set this to True otherwise, the topology fixing will be done in place."
    )
    seed: int = shell.arg(
        help="Seed for setting random number generator", argstr="-seed {seed}"
    )
    ga: bool = shell.arg(
        help="No documentation. Direct questions to analysis-bugs@nmr.mgh.harvard.edu",
        argstr="-ga",
    )
    mgz: bool = shell.arg(
        help="No documentation. Direct questions to analysis-bugs@nmr.mgh.harvard.edu",
        argstr="-mgz",
    )
    sphere: Nofix = shell.arg(help="Sphere input file", formatter="sphere_formatter")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="Output file for FixTopology", callable=out_file_callable
        )
