import attrs
from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "in_aseg":
        return argstr.format(**{name: os.path.basename(value).rstrip(".mgz")})

    return argstr.format(**inputs)


def in_aseg_formatter(field, inputs):
    return _format_arg("in_aseg", field, inputs, argstr="--aseg_name {in_aseg}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    out_dir = os.path.join(inputs["subjects_dir"], inputs["subject_id"], "mri")
    outputs["out_ribbon"] = os.path.join(out_dir, "ribbon.mgz")
    if inputs["save_ribbon"]:
        outputs["rh_ribbon"] = os.path.join(out_dir, "rh.ribbon.mgz")
        outputs["lh_ribbon"] = os.path.join(out_dir, "lh.ribbon.mgz")
    return outputs


def out_ribbon_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_ribbon")


def lh_ribbon_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("lh_ribbon")


def rh_ribbon_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("rh_ribbon")


@shell.define(xor=[["aseg", "in_aseg"]])
class VolumeMask(shell.Task["VolumeMask.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pydra.tasks.freesurfer.v8.utils.volume_mask import VolumeMask

    >>> task = VolumeMask()
    >>> task.left_whitelabel = 2
    >>> task.right_whitelabel = 41
    >>> task.lh_pial = Pial.mock("lh.pial")
    >>> task.rh_pial = File.mock()
    >>> task.lh_white = Pial.mock("lh.pial")
    >>> task.rh_white = File.mock()
    >>> task.aseg = File.mock()
    >>> task.subject_id = "10335"
    >>> task.in_aseg = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_volmask"
    left_whitelabel: int = shell.arg(
        help="Left white matter label", argstr="--label_left_white {left_whitelabel}"
    )
    left_ribbonlabel: int = shell.arg(
        help="Left cortical ribbon label",
        argstr="--label_left_ribbon {left_ribbonlabel}",
    )
    right_whitelabel: int = shell.arg(
        help="Right white matter label", argstr="--label_right_white {right_whitelabel}"
    )
    right_ribbonlabel: int = shell.arg(
        help="Right cortical ribbon label",
        argstr="--label_right_ribbon {right_ribbonlabel}",
    )
    lh_pial: Pial = shell.arg(help="Implicit input left pial surface")
    rh_pial: File = shell.arg(help="Implicit input right pial surface")
    lh_white: Pial = shell.arg(help="Implicit input left white matter surface")
    rh_white: File = shell.arg(help="Implicit input right white matter surface")
    aseg: File | None = shell.arg(
        help="Implicit aseg.mgz segmentation. Specify a different aseg by using the 'in_aseg' input."
    )
    subject_id: ty.Any | None = shell.arg(
        help="Subject being processed",
        argstr="{subject_id}",
        position=-1,
        default="subject_id",
    )
    in_aseg: File | None = shell.arg(
        help="Input aseg file for VolumeMask", formatter="in_aseg_formatter"
    )
    save_ribbon: bool = shell.arg(
        help="option to save just the ribbon for the hemispheres in the format ?h.ribbon.mgz",
        argstr="--save_ribbon",
    )
    copy_inputs: bool = shell.arg(
        help="If running as a node, set this to True. This will copy the implicit input files to the node directory."
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_ribbon: File | None = shell.out(
            help="Output cortical ribbon mask", callable=out_ribbon_callable
        )
        lh_ribbon: File | None = shell.out(
            help="Output left cortical ribbon mask", callable=lh_ribbon_callable
        )
        rh_ribbon: File | None = shell.out(
            help="Output right cortical ribbon mask", callable=rh_ribbon_callable
        )
