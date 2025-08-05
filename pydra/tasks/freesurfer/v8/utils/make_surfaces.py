import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name in ["in_T1", "in_aseg"]:

        basename = os.path.basename(value)

        if inputs["mgz"]:
            prefix = os.path.splitext(basename)[0]
        else:
            prefix = basename
        if prefix == "aseg":
            return  # aseg is already the default
        return argstr.format(**{name: prefix})
    elif name in ["orig_white", "orig_pial"]:

        basename = os.path.basename(value)
        suffix = basename.split(".")[1]
        return argstr.format(**{name: suffix})
    elif name == "in_orig":
        if value.endswith(("lh.orig", "rh.orig")):

            return
        else:

            basename = os.path.basename(value)
            suffix = basename.split(".")[1]
            return argstr.format(**{name: suffix})

    return argstr.format(**inputs)


def in_orig_formatter(field, inputs):
    return _format_arg("in_orig", field, inputs, argstr="-orig {in_orig}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}

    dest_dir = os.path.join(inputs["subjects_dir"], inputs["subject_id"], "surf")

    label_dir = os.path.join(inputs["subjects_dir"], inputs["subject_id"], "label")
    if not inputs["no_white"]:
        outputs["out_white"] = os.path.join(
            dest_dir, str(inputs["hemisphere"]) + ".white"
        )

    outputs["out_curv"] = os.path.join(dest_dir, str(inputs["hemisphere"]) + ".curv")
    outputs["out_area"] = os.path.join(dest_dir, str(inputs["hemisphere"]) + ".area")

    if (inputs["orig_pial"] is not attrs.NOTHING) or inputs["white"] == "NOWRITE":
        outputs["out_curv"] = outputs["out_curv"] + ".pial"
        outputs["out_area"] = outputs["out_area"] + ".pial"
        outputs["out_pial"] = os.path.join(
            dest_dir, str(inputs["hemisphere"]) + ".pial"
        )
        outputs["out_thickness"] = os.path.join(
            dest_dir, str(inputs["hemisphere"]) + ".thickness"
        )
    else:

        outputs["out_cortex"] = os.path.join(
            label_dir, str(inputs["hemisphere"]) + ".cortex.label"
        )
    return outputs


def out_white_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_white")


def out_curv_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_curv")


def out_area_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_area")


def out_cortex_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_cortex")


def out_pial_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_pial")


def out_thickness_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_thickness")


@shell.define(xor=[["noaparc", "in_label"]])
class MakeSurfaces(shell.Task["MakeSurfaces.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.v8.utils.make_surfaces import MakeSurfaces

    >>> task = MakeSurfaces()
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.in_orig = Pial.mock("lh.pial")
    >>> task.inputs.in_wm = File.mock()
    >>> task.inputs.in_filled = MghGz.mock("norm.mgz")
    >>> task.inputs.in_white = File.mock()
    >>> task.inputs.in_label = File.mock()
    >>> task.inputs.orig_white = File.mock()
    >>> task.inputs.orig_pial = File.mock()
    >>> task.inputs.in_aseg = File.mock()
    >>> task.inputs.in_T1 = MghGz.mock("T1.mgz")
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_make_surfaces"
    hemisphere: ty.Any = shell.arg(
        help="Hemisphere being processed", argstr="{hemisphere}", position=-1
    )
    subject_id: ty.Any | None = shell.arg(
        help="Subject being processed",
        argstr="{subject_id}",
        position=-2,
        default="subject_id",
    )
    in_orig: Pial = shell.arg(
        help="Implicit input file <hemisphere>.orig", formatter="in_orig_formatter"
    )
    in_wm: File = shell.arg(help="Implicit input file wm.mgz")
    in_filled: MghGz = shell.arg(help="Implicit input file filled.mgz")
    in_white: File = shell.arg(help="Implicit input that is sometimes used")
    in_label: File | None = shell.arg(
        help="Implicit input label/<hemisphere>.aparc.annot"
    )
    orig_white: File = shell.arg(
        help="Specify a white surface to start with", argstr="-orig_white {orig_white}"
    )
    orig_pial: File = shell.arg(
        help="Specify a pial surface to start with",
        argstr="-orig_pial {orig_pial}",
        requires=["in_label"],
    )
    fix_mtl: bool = shell.arg(help="Undocumented flag", argstr="-fix_mtl")
    no_white: bool = shell.arg(help="Undocumented flag", argstr="-nowhite")
    white_only: bool = shell.arg(help="Undocumented flag", argstr="-whiteonly")
    in_aseg: File = shell.arg(help="Input segmentation file", argstr="-aseg {in_aseg}")
    in_T1: MghGz = shell.arg(help="Input brain or T1 file", argstr="-T1 {in_T1}")
    mgz: bool = shell.arg(
        help="No documentation. Direct questions to analysis-bugs@nmr.mgh.harvard.edu",
        argstr="-mgz",
    )
    noaparc: bool = shell.arg(
        help="No documentation. Direct questions to analysis-bugs@nmr.mgh.harvard.edu",
        argstr="-noaparc",
    )
    maximum: float = shell.arg(
        help="No documentation (used for longitudinal processing)",
        argstr="-max {maximum:.1}",
    )
    longitudinal: bool = shell.arg(
        help="No documentation (used for longitudinal processing)", argstr="-long"
    )
    white: ty.Any = shell.arg(help="White surface name", argstr="-white {white}")
    copy_inputs: bool = shell.arg(
        help="If running as a node, set this to True. This will copy the input files to the node  directory."
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_white: File | None = shell.out(
            help="Output white matter hemisphere surface", callable=out_white_callable
        )
        out_curv: File | None = shell.out(
            help="Output curv file for MakeSurfaces", callable=out_curv_callable
        )
        out_area: File | None = shell.out(
            help="Output area file for MakeSurfaces", callable=out_area_callable
        )
        out_cortex: File | None = shell.out(
            help="Output cortex file for MakeSurfaces", callable=out_cortex_callable
        )
        out_pial: File | None = shell.out(
            help="Output pial surface for MakeSurfaces", callable=out_pial_callable
        )
        out_thickness: File | None = shell.out(
            help="Output thickness file for MakeSurfaces",
            callable=out_thickness_callable,
        )
