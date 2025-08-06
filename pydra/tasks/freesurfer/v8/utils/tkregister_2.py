import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz, Nifti1
from fileformats.medimage_freesurfer import Dat
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib._local import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "lta_in" and inputs["invert_lta_in"]:
        spec = "--lta-inv %s"
    if name in ("fsl_out", "lta_out") and value is True:
        value = _list_outputs(
            fsl_out=inputs["fsl_out"],
            reg_file=inputs["reg_file"],
            lta_out=inputs["lta_out"],
        )[f"{name[:3]}_file"]

    return argstr.format(**inputs)


def lta_in_formatter(field, inputs):
    return _format_arg("lta_in", field, inputs, argstr="--lta {lta_in}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    reg_file = os.path.abspath(inputs["reg_file"])
    outputs["reg_file"] = reg_file

    cwd = os.getcwd()
    fsl_out = inputs["fsl_out"]
    if fsl_out is not attrs.NOTHING:
        if fsl_out is True:
            outputs["fsl_file"] = fname_presuffix(
                reg_file, suffix=".mat", newpath=cwd, use_ext=False
            )
        else:
            outputs["fsl_file"] = os.path.abspath(inputs["fsl_out"])

    lta_out = inputs["lta_out"]
    if lta_out is not attrs.NOTHING:
        if lta_out is True:
            outputs["lta_file"] = fname_presuffix(
                reg_file, suffix=".lta", newpath=cwd, use_ext=False
            )
        else:
            outputs["lta_file"] = os.path.abspath(inputs["lta_out"])
    return outputs


def reg_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("reg_file")


def fsl_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fsl_file")


def lta_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("lta_file")


@shell.define(
    xor=[
        ["fstarg", "target_image"],
        ["fstal", "moving_image", "reg_file", "target_image"],
    ]
)
class Tkregister2(shell.Task["Tkregister2.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz, Nifti1
    >>> from fileformats.medimage_freesurfer import Dat
    >>> from pathlib._local import Path
    >>> from pydra.tasks.freesurfer.v8.utils.tkregister_2 import Tkregister2

    >>> task = Tkregister2()
    >>> task.inputs.target_image = File.mock()
    >>> task.inputs.moving_image = "T1.mgz"
    >>> task.inputs.fsl_in_matrix = File.mock()
    >>> task.inputs.xfm = File.mock()
    >>> task.inputs.lta_in = File.mock()
    >>> task.inputs.reg_file = "T1_to_native.dat"
    >>> task.inputs.reg_header = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'tkregister2 --mov T1.mgz --noedit --reg T1_to_native.dat --regheader --targ structural.nii'


    >>> task = Tkregister2()
    >>> task.inputs.target_image = File.mock()
    >>> task.inputs.moving_image = "epi.nii"
    >>> task.inputs.fsl_in_matrix = File.mock()
    >>> task.inputs.xfm = File.mock()
    >>> task.inputs.lta_in = File.mock()
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'tkregister2 --fsl flirt.mat --mov epi.nii --noedit --reg register.dat'


    """

    executable = "tkregister2"
    target_image: File | None = shell.arg(
        help="target volume", argstr="--targ {target_image}"
    )
    fstarg: bool = shell.arg(help="use subject's T1 as reference", argstr="--fstarg")
    moving_image: Nifti1 | MghGz | None = shell.arg(
        help="moving volume", argstr="--mov {moving_image}"
    )
    fsl_in_matrix: File = shell.arg(
        help="fsl-style registration input matrix", argstr="--fsl {fsl_in_matrix}"
    )
    xfm: File = shell.arg(
        help="use a matrix in MNI coordinates as initial registration",
        argstr="--xfm {xfm}",
    )
    lta_in: File = shell.arg(
        help="use a matrix in MNI coordinates as initial registration",
        formatter="lta_in_formatter",
    )
    invert_lta_in: bool = shell.arg(
        help="Invert input LTA before applying", requires=["lta_in"]
    )
    fsl_out: ty.Any = shell.arg(
        help="compute an FSL-compatible resgitration matrix",
        argstr="--fslregout {fsl_out}",
    )
    lta_out: ty.Any = shell.arg(
        help="output registration file (LTA format)", argstr="--ltaout {lta_out}"
    )
    invert_lta_out: bool = shell.arg(
        help="Invert input LTA before applying",
        argstr="--ltaout-inv",
        requires=["lta_in"],
    )
    subject_id: ty.Any = shell.arg(
        help="freesurfer subject ID", argstr="--s {subject_id}"
    )
    noedit: bool = shell.arg(
        help="do not open edit window (exit)", argstr="--noedit", default=True
    )
    reg_file: Path | None = shell.arg(
        help="freesurfer-style registration file",
        argstr="--reg {reg_file}",
        default="register.dat",
    )
    reg_header: bool = shell.arg(
        help="compute registration from headers", argstr="--regheader"
    )
    fstal: bool = shell.arg(
        help="set mov to be tal and reg to be tal xfm", argstr="--fstal"
    )
    movscale: float = shell.arg(
        help="adjust registration matrix to scale mov", argstr="--movscale {movscale}"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        reg_file: Dat | None = shell.out(
            help="freesurfer-style registration file", callable=reg_file_callable
        )
        fsl_file: File | None = shell.out(
            help="FSL-style registration file", callable=fsl_file_callable
        )
        lta_file: File | None = shell.out(
            help="LTA-style registration file", callable=lta_file_callable
        )
