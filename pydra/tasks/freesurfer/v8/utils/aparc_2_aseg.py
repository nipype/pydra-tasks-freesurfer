import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "aseg":

        basename = os.path.basename(value).replace(".mgz", "")
        return argstr.format(**{name: basename})
    elif name == "out_file":
        return argstr.format(**{name: os.path.abspath(value)})

    return argstr.format(**inputs)


def aseg_formatter(field, inputs):
    return _format_arg("aseg", field, inputs, argstr="--aseg {aseg}")


def out_file_formatter(field, inputs):
    return _format_arg("out_file", field, inputs, argstr="--o {out_file}")


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
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.aparc_2_aseg import Aparc2Aseg

    >>> task = Aparc2Aseg()
    >>> task.inputs.lh_white = Pial.mock("lh.pial")
    >>> task.inputs.rh_white = File.mock()
    >>> task.inputs.lh_pial = Pial.mock("lh.pial")
    >>> task.inputs.rh_pial = File.mock()
    >>> task.inputs.lh_ribbon = MghGz.mock("label.mgz")
    >>> task.inputs.rh_ribbon = File.mock()
    >>> task.inputs.ribbon = MghGz.mock("label.mgz")
    >>> task.inputs.lh_annotation = File.mock()
    >>> task.inputs.rh_annotation = Pial.mock("lh.pial")
    >>> task.inputs.filled = File.mock()
    >>> task.inputs.aseg = File.mock()
    >>> task.inputs.ctxseg = File.mock()
    >>> task.inputs.label_wm = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_aparc2aseg"
    subject_id: ty.Any | None = shell.arg(
        help="Subject being processed", argstr="--s {subject_id}", default="subject_id"
    )
    out_file: Path = shell.arg(
        help="Full path of file to save the output segmentation in",
        formatter="out_file_formatter",
    )
    lh_white: Pial = shell.arg(help="Input file must be <subject_id>/surf/lh.white")
    rh_white: File = shell.arg(help="Input file must be <subject_id>/surf/rh.white")
    lh_pial: Pial = shell.arg(help="Input file must be <subject_id>/surf/lh.pial")
    rh_pial: File = shell.arg(help="Input file must be <subject_id>/surf/rh.pial")
    lh_ribbon: MghGz = shell.arg(
        help="Input file must be <subject_id>/mri/lh.ribbon.mgz"
    )
    rh_ribbon: File = shell.arg(
        help="Input file must be <subject_id>/mri/rh.ribbon.mgz"
    )
    ribbon: MghGz = shell.arg(help="Input file must be <subject_id>/mri/ribbon.mgz")
    lh_annotation: File = shell.arg(
        help="Input file must be <subject_id>/label/lh.aparc.annot"
    )
    rh_annotation: Pial = shell.arg(
        help="Input file must be <subject_id>/label/rh.aparc.annot"
    )
    filled: File = shell.arg(
        help="Implicit input filled file. Only required with FS v5.3."
    )
    aseg: File = shell.arg(help="Input aseg file", formatter="aseg_formatter")
    volmask: bool = shell.arg(help="Volume mask flag", argstr="--volmask")
    ctxseg: File = shell.arg(help="", argstr="--ctxseg {ctxseg}")
    label_wm: bool = shell.arg(
        help="For each voxel labeled as white matter in the aseg, re-assign\nits label to be that of the closest cortical point if its\ndistance is less than dmaxctx.",
        argstr="--labelwm",
    )
    hypo_wm: bool = shell.arg(help="Label hypointensities as WM", argstr="--hypo-as-wm")
    rip_unknown: bool = shell.arg(
        help="Do not label WM based on 'unknown' corical label", argstr="--rip-unknown"
    )
    a2009s: bool = shell.arg(help="Using the a2009s atlas", argstr="--a2009s")
    copy_inputs: bool = shell.arg(
        help="If running as a node, set this to True.This will copy the input files to the node directory."
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="Output aseg file", callable=out_file_callable
        )
