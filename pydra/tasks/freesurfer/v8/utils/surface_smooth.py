import attrs
from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import fname_presuffix
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            fwhm=inputs["fwhm"],
            in_file=inputs["in_file"],
            out_file=inputs["out_file"],
            smooth_iters=inputs["smooth_iters"],
        )[name]
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define(xor=[["fwhm", "smooth_iters"]])
class SurfaceSmooth(shell.Task["SurfaceSmooth.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.surface_smooth import SurfaceSmooth

    >>> task = SurfaceSmooth()
    >>> task.in_file = MghGz.mock("lh.cope1.mgz")
    >>> task.hemi = "lh"
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_surf2surf"
    in_file: MghGz = shell.arg(help="source surface file", argstr="--sval {in_file}")
    subject_id: ty.Any = shell.arg(
        help="subject id of surface file", argstr="--s {subject_id}"
    )
    hemi: ty.Any = shell.arg(help="hemisphere to operate on", argstr="--hemi {hemi}")
    fwhm: float | None = shell.arg(
        help="effective FWHM of the smoothing process", argstr="--fwhm {fwhm:.4}"
    )
    smooth_iters: int | None = shell.arg(
        help="iterations of the smoothing process", argstr="--smooth {smooth_iters}"
    )
    cortex: bool = shell.arg(
        help="only smooth within ``$hemi.cortex.label``",
        argstr="--cortex",
        default=True,
    )
    reshape: bool = shell.arg(
        help="reshape surface vector to fit in non-mgh format", argstr="--reshape"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="surface file to write",
            argstr="--tval {out_file}",
            path_template="out_file",
        )


def _list_outputs(fwhm=None, in_file=None, out_file=None, smooth_iters=None):
    outputs = {}
    outputs["out_file"] = out_file
    if outputs["out_file"] is attrs.NOTHING:
        in_file = in_file
        if fwhm is not attrs.NOTHING:
            kernel = fwhm
        else:
            kernel = smooth_iters
        outputs["out_file"] = fname_presuffix(
            in_file, suffix="_smooth%d" % kernel, newpath=output_dir
        )
    return outputs
