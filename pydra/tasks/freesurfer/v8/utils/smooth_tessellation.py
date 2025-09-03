import attrs
from fileformats.generic import Directory, File
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import split_filename
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["surface"] = _gen_outfilename(
        in_file=inputs["in_file"],
        out_file=inputs["out_file"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    return outputs


def surface_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("surface")


def _gen_filename(name, inputs):
    if name == "out_file":
        return _gen_outfilename(in_file=inputs["in_file"], out_file=inputs["out_file"])
    else:
        return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class SmoothTessellation(shell.Task["SmoothTessellation.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.smooth_tessellation import SmoothTessellation

    """

    executable = "mris_smooth"
    in_file: File = shell.arg(
        help="Input volume to tessellate voxels from.",
        argstr="{in_file}",
        position=-2,
        copy_mode="File.CopyMode.copy",
    )
    curvature_averaging_iterations: int = shell.arg(
        help="Number of curvature averaging iterations (default=10)",
        argstr="-a {curvature_averaging_iterations}",
    )
    smoothing_iterations: int = shell.arg(
        help="Number of smoothing iterations (default=10)",
        argstr="-n {smoothing_iterations}",
    )
    snapshot_writing_iterations: int = shell.arg(
        help="Write snapshot every *n* iterations",
        argstr="-w {snapshot_writing_iterations}",
    )
    use_gaussian_curvature_smoothing: bool = shell.arg(
        help="Use Gaussian curvature smoothing", argstr="-g"
    )
    gaussian_curvature_norm_steps: int = shell.arg(
        help="Use Gaussian curvature smoothing",
        argstr="{gaussian_curvature_norm_steps}",
    )
    gaussian_curvature_smoothing_steps: int = shell.arg(
        help="Use Gaussian curvature smoothing",
        argstr=" {gaussian_curvature_smoothing_steps}",
    )
    disable_estimates: bool = shell.arg(
        help="Disables the writing of curvature and area estimates", argstr="-nw"
    )
    normalize_area: bool = shell.arg(
        help="Normalizes the area after smoothing", argstr="-area"
    )
    use_momentum: bool = shell.arg(help="Uses momentum", argstr="-m")
    out_file: Path = shell.arg(
        help="output filename or True to generate one", argstr="{out_file}", position=-1
    )
    out_curvature_file: Path = shell.arg(
        help='Write curvature to ``?h.curvname`` (default "curv")',
        argstr="-c {out_curvature_file}",
    )
    out_area_file: Path = shell.arg(
        help='Write area to ``?h.areaname`` (default "area")',
        argstr="-b {out_area_file}",
    )
    seed: int = shell.arg(
        help="Seed for setting random number generator", argstr="-seed {seed}"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        surface: File | None = shell.out(
            help="Smoothed surface file.", callable=surface_callable
        )


def _gen_outfilename(
    in_file=None, out_file=None, inputs=None, output_dir=None, stderr=None, stdout=None
):
    if out_file is not attrs.NOTHING:
        return os.path.abspath(out_file)
    else:
        _, name, ext = split_filename(in_file)
        return os.path.abspath(name + "_smoothed" + ext)
