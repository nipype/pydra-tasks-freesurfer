import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import fname_presuffix
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    options = (
        "out_reg_file",
        "registered_file",
        "weights_file",
        "half_source",
        "half_targ",
        "half_weights",
        "half_source_xfm",
        "half_targ_xfm",
    )
    if name in options and isinstance(value, bool):
        value = _list_outputs(
            source_file=inputs["source_file"], target_file=inputs["target_file"]
        )[name]

    return argstr.format(**inputs)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    self_dict = {}

    outputs = {}
    cwd = os.getcwd()
    prefixes = dict(src=inputs["source_file"], trg=inputs["target_file"])
    suffixes = dict(
        out_reg_file=("src", "_robustreg.lta", False),
        registered_file=("src", "_robustreg", True),
        weights_file=("src", "_robustweights", True),
        half_source=("src", "_halfway", True),
        half_targ=("trg", "_halfway", True),
        half_weights=("src", "_halfweights", True),
        half_source_xfm=("src", "_robustxfm.lta", False),
        half_targ_xfm=("trg", "_robustxfm.lta", False),
    )
    for name, sufftup in list(suffixes.items()):
        value = getattr(self_dict["inputs"], name)
        if value:
            if value is True:
                outputs[name] = fname_presuffix(
                    prefixes[sufftup[0]],
                    suffix=sufftup[1],
                    newpath=cwd,
                    use_ext=sufftup[2],
                )
            else:
                outputs[name] = os.path.abspath(value)
    return outputs


def out_reg_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_reg_file")


def registered_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("registered_file")


def weights_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("weights_file")


def half_source_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("half_source")


def half_targ_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("half_targ")


def half_weights_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("half_weights")


def half_source_xfm_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("half_source_xfm")


def half_targ_xfm_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("half_targ_xfm")


@shell.define(xor=[["auto_sens", "outlier_sens"]])
class RobustRegister(shell.Task["RobustRegister.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.freesurfer.v8.preprocess.robust_register import RobustRegister

    >>> task = RobustRegister()
    >>> task.source_file = Nifti1.mock("structural.nii")
    >>> task.target_file = File.mock()
    >>> task.in_xfm_file = File.mock()
    >>> task.auto_sens = True
    >>> task.mask_source = File.mock()
    >>> task.mask_target = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_robust_register"
    source_file: Nifti1 = shell.arg(
        help="volume to be registered", argstr="--mov {source_file}"
    )
    target_file: File = shell.arg(
        help="target volume for the registration", argstr="--dst {target_file}"
    )
    out_reg_file: ty.Any = shell.arg(
        help="registration file; either True or filename",
        argstr="--lta {out_reg_file}",
        default=True,
    )
    registered_file: ty.Any = shell.arg(
        help="registered image; either True or filename",
        argstr="--warp {registered_file}",
    )
    weights_file: ty.Any = shell.arg(
        help="weights image to write; either True or filename",
        argstr="--weights {weights_file}",
    )
    est_int_scale: bool = shell.arg(
        help="estimate intensity scale (recommended for unnormalized images)",
        argstr="--iscale",
    )
    trans_only: bool = shell.arg(
        help="find 3 parameter translation only", argstr="--transonly"
    )
    in_xfm_file: File = shell.arg(
        help="use initial transform on source", argstr="--transform"
    )
    half_source: ty.Any = shell.arg(
        help="write source volume mapped to halfway space",
        argstr="--halfmov {half_source}",
    )
    half_targ: ty.Any = shell.arg(
        help="write target volume mapped to halfway space",
        argstr="--halfdst {half_targ}",
    )
    half_weights: ty.Any = shell.arg(
        help="write weights volume mapped to halfway space",
        argstr="--halfweights {half_weights}",
    )
    half_source_xfm: ty.Any = shell.arg(
        help="write transform from source to halfway space",
        argstr="--halfmovlta {half_source_xfm}",
    )
    half_targ_xfm: ty.Any = shell.arg(
        help="write transform from target to halfway space",
        argstr="--halfdstlta {half_targ_xfm}",
    )
    auto_sens: bool = shell.arg(help="auto-detect good sensitivity", argstr="--satit")
    outlier_sens: float | None = shell.arg(
        help="set outlier sensitivity explicitly", argstr="--sat {outlier_sens:.4}"
    )
    least_squares: bool = shell.arg(
        help="use least squares instead of robust estimator", argstr="--leastsquares"
    )
    no_init: bool = shell.arg(help="skip transform init", argstr="--noinit")
    init_orient: bool = shell.arg(
        help="use moments for initial orient (recommended for stripped brains)",
        argstr="--initorient",
    )
    max_iterations: int = shell.arg(
        help="maximum # of times on each resolution", argstr="--maxit {max_iterations}"
    )
    high_iterations: int = shell.arg(
        help="max # of times on highest resolution", argstr="--highit {high_iterations}"
    )
    iteration_thresh: float = shell.arg(
        help="stop iterations when below threshold",
        argstr="--epsit {iteration_thresh:.3}",
    )
    subsample_thresh: int = shell.arg(
        help="subsample if dimension is above threshold size",
        argstr="--subsample {subsample_thresh}",
    )
    outlier_limit: float = shell.arg(
        help="set maximal outlier limit in satit", argstr="--wlimit {outlier_limit:.3}"
    )
    write_vo2vox: bool = shell.arg(
        help="output vox2vox matrix (default is RAS2RAS)", argstr="--vox2vox"
    )
    no_multi: bool = shell.arg(help="work on highest resolution", argstr="--nomulti")
    mask_source: File = shell.arg(
        help="image to mask source volume with", argstr="--maskmov {mask_source}"
    )
    mask_target: File = shell.arg(
        help="image to mask target volume with", argstr="--maskdst {mask_target}"
    )
    force_double: bool = shell.arg(
        help="use double-precision intensities", argstr="--doubleprec"
    )
    force_float: bool = shell.arg(help="use float intensities", argstr="--floattype")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_reg_file: File | None = shell.out(
            help="output registration file", callable=out_reg_file_callable
        )
        registered_file: File | None = shell.out(
            help="output image with registration applied",
            callable=registered_file_callable,
        )
        weights_file: File | None = shell.out(
            help="image of weights used", callable=weights_file_callable
        )
        half_source: File | None = shell.out(
            help="source image mapped to halfway space", callable=half_source_callable
        )
        half_targ: File | None = shell.out(
            help="target image mapped to halfway space", callable=half_targ_callable
        )
        half_weights: File | None = shell.out(
            help="weights image mapped to halfway space", callable=half_weights_callable
        )
        half_source_xfm: File | None = shell.out(
            help="transform file to map source image to halfway space",
            callable=half_source_xfm_callable,
        )
        half_targ_xfm: File | None = shell.out(
            help="transform file to map target image to halfway space",
            callable=half_targ_xfm_callable,
        )
