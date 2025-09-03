import attrs
from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import White
import logging
import os
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = _associated_file(
        inputs["in_file"],
        inputs["out_name"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


@shell.define
class MRIsExpand(shell.Task["MRIsExpand.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import White
    >>> from pydra.tasks.freesurfer.v8.utils.mr_is_expand import MRIsExpand

    >>> task = MRIsExpand()
    >>> task.in_file = White.mock("lh.white")
    >>> task.distance = 0.5
    >>> task.out_name = "graymid"
    >>> task.thickness = True
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_expand"
    in_file: White = shell.arg(
        help="Surface to expand", argstr="{in_file}", position=-3
    )
    distance: float = shell.arg(
        help="Distance in mm or fraction of cortical thickness",
        argstr="{distance}",
        position=-2,
    )
    out_name: str = shell.arg(
        help='Output surface file. If no path, uses directory of ``in_file``. If no path AND missing "lh." or "rh.", derive from ``in_file``',
        argstr="{out_name}",
        position=-1,
        default="expanded",
    )
    thickness: bool = shell.arg(
        help="Expand by fraction of cortical thickness, not mm", argstr="-thickness"
    )
    thickness_name: str = shell.arg(
        help='Name of thickness file (implicit: "thickness")\nIf no path, uses directory of ``in_file``\nIf no path AND missing "lh." or "rh.", derive from `in_file`',
        argstr="-thickness_name {thickness_name}",
    )
    pial: str = shell.arg(
        help='Name of pial file (implicit: "pial")\nIf no path, uses directory of ``in_file``\nIf no path AND missing "lh." or "rh.", derive from ``in_file``',
        argstr="-pial {pial}",
    )
    sphere: str = shell.arg(help="WARNING: Do not change this trait", default="sphere")
    spring: float = shell.arg(help="Spring term (implicit: 0.05)", argstr="-S {spring}")
    dt: float = shell.arg(help="dt (implicit: 0.25)", argstr="-T {dt}")
    write_iterations: int = shell.arg(
        help="Write snapshots of expansion every N iterations",
        argstr="-W {write_iterations}",
    )
    smooth_averages: int = shell.arg(
        help="Smooth surface with N iterations after expansion",
        argstr="-A {smooth_averages}",
    )
    nsurfaces: int = shell.arg(
        help="Number of surfacces to write during expansion", argstr="-N {nsurfaces}"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="Output surface file", callable=out_file_callable
        )


def _associated_file(
    in_file, out_name, inputs=None, output_dir=None, stderr=None, stdout=None
):
    """Based on MRIsBuildFileName in freesurfer/utils/mrisurf.c

    If no path information is provided for out_name, use path and
    hemisphere (if also unspecified) from in_file to determine the path
    of the associated file.
    Use in_file prefix to indicate hemisphere for out_name, rather than
    inspecting the surface data structure.
    """
    path, base = os.path.split(out_name)
    if path == "":
        path, in_file = os.path.split(in_file)
        hemis = ("lh.", "rh.")
        if in_file[:3] in hemis and base[:3] not in hemis:
            base = in_file[:3] + base
    return os.path.join(path, base)
