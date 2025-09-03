import attrs
from fileformats.generic import File
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name.startswith("out_") and value is True:
        value = _list_outputs()[name]

    return argstr.format(**inputs)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    self_dict = {}

    outputs = {}
    for name, default in (
        ("out_lta", "out.lta"),
        ("out_fsl", "out.mat"),
        ("out_mni", "out.xfm"),
        ("out_reg", "out.dat"),
        ("out_itk", "out.txt"),
    ):
        attr = getattr(self_dict["inputs"], name)
        if attr:
            fname = default if attr is True else attr
            outputs[name] = os.path.abspath(fname)

    return outputs


def out_lta_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_lta")


def out_fsl_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_fsl")


def out_mni_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_mni")


def out_reg_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_reg")


def out_itk_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_itk")


@shell.define(xor=[["in_fsl", "in_itk", "in_lta", "in_mni", "in_niftyreg", "in_reg"]])
class LTAConvert(shell.Task["LTAConvert.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.freesurfer.v8.utils.lta_convert import LTAConvert

    """

    executable = "lta_convert"
    in_lta: ty.Any | None = shell.arg(
        help="input transform of LTA type", argstr="--inlta {in_lta}"
    )
    in_fsl: File | None = shell.arg(
        help="input transform of FSL type", argstr="--infsl {in_fsl}"
    )
    in_mni: File | None = shell.arg(
        help="input transform of MNI/XFM type", argstr="--inmni {in_mni}"
    )
    in_reg: File | None = shell.arg(
        help="input transform of TK REG type (deprecated format)",
        argstr="--inreg {in_reg}",
    )
    in_niftyreg: File | None = shell.arg(
        help="input transform of Nifty Reg type (inverse RAS2RAS)",
        argstr="--inniftyreg {in_niftyreg}",
    )
    in_itk: File | None = shell.arg(
        help="input transform of ITK type", argstr="--initk {in_itk}"
    )
    out_lta: ty.Any = shell.arg(
        help="output linear transform (LTA Freesurfer format)",
        argstr="--outlta {out_lta}",
    )
    out_fsl: ty.Any = shell.arg(
        help="output transform in FSL format", argstr="--outfsl {out_fsl}"
    )
    out_mni: ty.Any = shell.arg(
        help="output transform in MNI/XFM format", argstr="--outmni {out_mni}"
    )
    out_reg: ty.Any = shell.arg(
        help="output transform in reg dat format", argstr="--outreg {out_reg}"
    )
    out_itk: ty.Any = shell.arg(
        help="output transform in ITK format", argstr="--outitk {out_itk}"
    )
    invert: bool = shell.arg(help="", argstr="--invert")
    ltavox2vox: bool = shell.arg(help="", argstr="--ltavox2vox", requires=["out_lta"])
    source_file: File = shell.arg(help="", argstr="--src {source_file}")
    target_file: File = shell.arg(help="", argstr="--trg {target_file}")
    target_conform: bool = shell.arg(help="", argstr="--trgconform")

    class Outputs(shell.Outputs):
        out_lta: File | None = shell.out(
            help="output linear transform (LTA Freesurfer format)",
            callable=out_lta_callable,
        )
        out_fsl: File | None = shell.out(
            help="output transform in FSL format", callable=out_fsl_callable
        )
        out_mni: File | None = shell.out(
            help="output transform in MNI/XFM format", callable=out_mni_callable
        )
        out_reg: File | None = shell.out(
            help="output transform in reg dat format", callable=out_reg_callable
        )
        out_itk: File | None = shell.out(
            help="output transform in ITK format", callable=out_itk_callable
        )
