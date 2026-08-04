import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.vendor.freesurfer.medimage import Pial
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None or value is False:
        return ""

    if name == "aseg":

        basename = os.path.basename(value).replace(".mgz", "")
        return argstr.format(**{name: basename})
    elif name == "out_file":
        return argstr.format(**{name: os.path.abspath(value)})

    return argstr.format(**inputs)


def aseg_formatter(field, inputs):
    value = inputs["aseg"] if isinstance(inputs, dict) else inputs.aseg
    return _format_arg("aseg", value, inputs, argstr="--aseg {aseg}")


def out_file_formatter(field, inputs):
    value = inputs["out_file"] if isinstance(inputs, dict) else inputs.out_file
    return _format_arg("out_file", value, inputs, argstr="--o {out_file}")


def ctxseg_formatter(field, inputs):
    value = inputs["ctxseg"] if isinstance(inputs, dict) else inputs.ctxseg
    if value is None or value is False:
        return ""
    return f"--ctxseg {value}"


def _no_cmdline(field, inputs):
    return ""


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
class Aparc2Aseg(shell.Task["Aparc2Aseg.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.vendor.freesurfer.medimage import Pial
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.aparc_2_aseg import Aparc2Aseg

    >>> task = Aparc2Aseg()
    >>> task.lh_white = Pial.mock("lh.pial")
    >>> task.rh_white = File.mock()
    >>> task.lh_pial = Pial.mock("lh.pial")
    >>> task.rh_pial = File.mock()
    >>> task.lh_ribbon = MghGz.mock("label.mgz")
    >>> task.rh_ribbon = File.mock()
    >>> task.ribbon = MghGz.mock("label.mgz")
    >>> task.lh_annotation = File.mock()
    >>> task.rh_annotation = Pial.mock("lh.pial")
    >>> task.filled = File.mock()
    >>> task.aseg = File.mock()
    >>> task.ctxseg = File.mock()
    >>> task.label_wm = True
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_aparc2aseg"
    subject_id: ty.Any | None = shell.arg(
        help="Subject being processed", argstr="--s {subject_id}", default=False
    )
    annot: str | None = shell.arg(
        help="Annotation short name; mri_aparc2aseg looks for <subject>/label/?h.<annot>.annot",
        argstr="--annot {annot}",
        default=None,
    )
    out_file: Path = shell.arg(
        help="Full path of file to save the output segmentation in",
        formatter=out_file_formatter,
    )
    lh_white: ty.Any | None = shell.arg(
        help="Input file must be <subject_id>/surf/lh.white",
        default=False,
    )
    rh_white: ty.Any | None = shell.arg(
        help="Input file must be <subject_id>/surf/rh.white",
        default=False,
    )
    lh_pial: ty.Any | None = shell.arg(
        help="Input file must be <subject_id>/surf/lh.pial",
        default=False,
    )
    rh_pial: ty.Any | None = shell.arg(
        help="Input file must be <subject_id>/surf/rh.pial",
        default=False,
    )
    lh_ribbon: ty.Any | None = shell.arg(
        help="Input file must be <subject_id>/mri/lh.ribbon.mgz",
        default=False,
    )
    rh_ribbon: ty.Any | None = shell.arg(
        help="Input file must be <subject_id>/mri/rh.ribbon.mgz",
        default=False,
    )
    ribbon: ty.Any | None = shell.arg(
        help="Input file must be <subject_id>/mri/ribbon.mgz",
        default=False,
    )
    lh_annotation: ty.Any = shell.arg(
        help="Input file must be <subject_id>/label/lh.aparc.annot",
        formatter=_no_cmdline,
    )
    rh_annotation: ty.Any = shell.arg(
        help="Input file must be <subject_id>/label/rh.aparc.annot",
        formatter=_no_cmdline,
    )
    filled: ty.Any | None = shell.arg(
        help="Implicit input filled file. Only required with FS v5.3.",
        default=False,
    )
    aseg: ty.Any | None = shell.arg(
        help="Input aseg file",
        formatter=aseg_formatter,
        default=False,
    )
    volmask: bool | None = shell.arg(
        help="Volume mask flag",
        argstr="--volmask",
        default=False,
    )
    ctxseg: ty.Any | None = shell.arg(
        help="",
        formatter=ctxseg_formatter,
        default=False,
    )
    label_wm: bool | None = shell.arg(
        help="For each voxel labeled as white matter in the aseg, re-assign\nits label to be that of the closest cortical point if its\ndistance is less than dmaxctx.",
        argstr="--labelwm",
        default=False,
    )
    hypo_wm: bool | None = shell.arg(
        help="Label hypointensities as WM",
        argstr="--hypo-as-wm",
        default=False,
    )
    rip_unknown: bool | None = shell.arg(
        help="Do not label WM based on 'unknown' corical label",
        argstr="--rip-unknown",
        default=False,
    )
    a2009s: bool | None = shell.arg(
        help="Using the a2009s atlas",
        argstr="--a2009s",
        default=False,
    )
    copy_inputs: bool | None = shell.arg(
        help="If running as a node, set this to True.This will copy the input files to the node directory.",
        default=False,
    )
    # subjects_dir: Directory = shell.arg(help="subjects directory")
    old_ribbon: bool | None = shell.arg(
        help="	use mri/hemi.ribbon.mgz as a mask for the cortex",
        argstr="--old-ribbon",
        default=False,
    )

    class Outputs(shell.Outputs):
        out_file: File | None = shell.outarg(
            help="Full path of file to save the output segmentation in",
            # callable=out_file_callable,
            argstr="--o {out_file}",
            path_template="out_file",
        )
