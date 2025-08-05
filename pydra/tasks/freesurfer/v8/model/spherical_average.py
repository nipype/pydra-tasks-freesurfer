import attrs
from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
import os
from pathlib import Path
from pathlib._local import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "in_orig" or name == "in_surf":
        surf = os.path.basename(value)
        for item in ["lh.", "rh."]:
            surf = surf.replace(item, "")
        return argstr.format(**{name: surf})

    return argstr.format(**inputs)


def in_orig_formatter(field, inputs):
    return _format_arg("in_orig", field, inputs, argstr="-orig {in_orig}")


def in_surf_formatter(field, inputs):
    return _format_arg("in_surf", field, inputs, argstr="{in_surf}")


def _gen_filename(name, inputs):
    if name == "in_average":
        avg_subject = str(inputs["hemisphere"]) + ".EC_average"
        avg_directory = os.path.join(inputs["subjects_dir"], avg_subject)
        if not os.path.isdir(avg_directory):
            fs_home = os.path.abspath(os.environ.get("FREESURFER_HOME"))
        return avg_subject
    elif name == "out_file":
        return _list_outputs(
            in_average=inputs["in_average"],
            out_file=inputs["out_file"],
            subject_id=inputs["subject_id"],
            subjects_dir=inputs["subjects_dir"],
            hemisphere=inputs["hemisphere"],
        )[name]
    else:
        return None


def in_average_default(inputs):
    return _gen_filename("in_average", inputs=inputs)


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class SphericalAverage(shell.Task["SphericalAverage.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib._local import Path
    >>> from pydra.tasks.freesurfer.v8.model.spherical_average import SphericalAverage

    >>> task = SphericalAverage()
    >>> task.inputs.out_file = "test.out"
    >>> task.inputs.in_surf = Pial.mock("lh.pial")
    >>> task.inputs.fname = "lh.entorhinal"
    >>> task.inputs.subject_id = "10335"
    >>> task.inputs.in_orig = File.mock()
    >>> task.inputs.threshold = 5
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_spherical_average"
    in_average: ty.Any = shell.arg(
        help="Average subject", argstr="{in_average}", position=-2
    )
    in_surf: Pial = shell.arg(
        help="Input surface file", position=-3, formatter="in_surf_formatter"
    )
    hemisphere: ty.Any = shell.arg(
        help="Input hemisphere", argstr="{hemisphere}", position=-4
    )
    fname: ty.Any = shell.arg(
        help="Filename from the average subject directory.\nExample: to use rh.entorhinal.label as the input label filename, set fname to 'rh.entorhinal'\nand which to 'label'. The program will then search for\n``<in_average>/label/rh.entorhinal.label``",
        argstr="{fname}",
        position=-5,
    )
    which: ty.Any = shell.arg(help="No documentation", argstr="{which}", position=-6)
    subject_id: ty.Any = shell.arg(help="Output subject id", argstr="-o {subject_id}")
    erode: int = shell.arg(help="Undocumented", argstr="-erode {erode}")
    in_orig: File = shell.arg(
        help="Original surface filename", formatter="in_orig_formatter"
    )
    threshold: float = shell.arg(help="Undocumented", argstr="-t {threshold:.1}")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Output filename",
            argstr="{out_file}",
            position=-1,
            path_template='"test.out"',
        )


def _list_outputs(
    in_average=None, out_file=None, subject_id=None, subjects_dir=None, hemisphere=None
):
    outputs = {}
    if out_file is not attrs.NOTHING:
        outputs["out_file"] = os.path.abspath(out_file)
    else:
        out_dir = os.path.join(subjects_dir, subject_id, "label")
        if in_average is not attrs.NOTHING:
            basename = os.path.basename(in_average)
            basename = basename.replace("_", "_exvivo_") + ".label"
        else:
            basename = str(hemisphere) + ".EC_exvivo_average.label"
        outputs["out_file"] = os.path.join(out_dir, basename)
    return outputs
