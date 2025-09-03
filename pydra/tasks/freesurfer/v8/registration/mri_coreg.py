import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
import os
import os.path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(opt, val, inputs, argstr):
    if val is None:
        return ""

    if opt in ("out_reg_file", "out_lta_file", "out_params_file") and val is True:
        val = _list_outputs(
            out_lta_file=inputs["out_lta_file"],
            out_params_file=inputs["out_params_file"],
            out_reg_file=inputs["out_reg_file"],
        )[opt]
    elif opt == "reference_mask" and val is False:
        return "--no-ref-mask"

    return argstr.format(**inputs)


def reference_mask_formatter(field, inputs):
    return _format_arg(
        "reference_mask", field, inputs, argstr="--ref-mask {reference_mask}"
    )


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}

    out_lta_file = inputs["out_lta_file"]
    if out_lta_file is not attrs.NOTHING:
        if out_lta_file is True:
            out_lta_file = "registration.lta"
        outputs["out_lta_file"] = os.path.abspath(out_lta_file)

    out_reg_file = inputs["out_reg_file"]
    if out_reg_file is not attrs.NOTHING:
        if out_reg_file is True:
            out_reg_file = "registration.dat"
        outputs["out_reg_file"] = os.path.abspath(out_reg_file)

    out_params_file = inputs["out_params_file"]
    if out_params_file is not attrs.NOTHING:
        if out_params_file is True:
            out_params_file = "registration.par"
        outputs["out_params_file"] = os.path.abspath(out_params_file)

    return outputs


def out_reg_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_reg_file")


def out_lta_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_lta_file")


def out_params_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_params_file")


@shell.define(
    xor=[
        ["brute_force_limit", "no_brute_force"],
        ["brute_force_samples", "no_brute_force"],
        ["reference_file", "subject_id"],
    ]
)
class MRICoreg(shell.Task["MRICoreg.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.freesurfer.v8.registration.mri_coreg import MRICoreg

    >>> task = MRICoreg()
    >>> task.source_file = Nifti1.mock("moving1.nii")
    >>> task.reference_file = File.mock()
    >>> task.subjects_dir = Directory.mock(".")
    >>> task.cmdline
    'None'


    >>> task = MRICoreg()
    >>> task.source_file = Nifti1.mock("moving1.nii")
    >>> task.reference_file = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.subject_id = "fsaverage"
    >>> task.cmdline
    'mri_coreg --s fsaverage --no-ref-mask --lta .../registration.lta --mov moving1.nii --sd .'


    >>> task = MRICoreg()
    >>> task.source_file = Nifti1.mock()
    >>> task.reference_file = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.sep = [4]
    >>> task.cmdline
    'mri_coreg --s fsaverage --no-ref-mask --lta .../registration.lta --sep 4 --mov moving1.nii --sd .'


    >>> task = MRICoreg()
    >>> task.source_file = Nifti1.mock()
    >>> task.reference_file = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.sep = [4, 5]
    >>> task.cmdline
    'mri_coreg --s fsaverage --no-ref-mask --lta .../registration.lta --sep 4 --sep 5 --mov moving1.nii --sd .'


    """

    executable = "mri_coreg"
    source_file: Nifti1 = shell.arg(
        help="source file to be registered", argstr="--mov {source_file}"
    )
    reference_file: File | None = shell.arg(
        help="reference (target) file", argstr="--ref {reference_file}"
    )
    out_lta_file: ty.Any = shell.arg(
        help="output registration file (LTA format)",
        argstr="--lta {out_lta_file}",
        default=True,
    )
    out_reg_file: ty.Any = shell.arg(
        help="output registration file (REG format)", argstr="--regdat {out_reg_file}"
    )
    out_params_file: ty.Any = shell.arg(
        help="output parameters file", argstr="--params {out_params_file}"
    )
    subjects_dir: Directory = shell.arg(
        help="FreeSurfer SUBJECTS_DIR", argstr="--sd {subjects_dir}"
    )
    subject_id: str = shell.arg(
        help="freesurfer subject ID (implies ``reference_mask == aparc+aseg.mgz`` unless otherwise specified)",
        argstr="--s {subject_id}",
        position=1,
        requires=["subjects_dir"],
    )
    dof: ty.Any = shell.arg(
        help="number of transform degrees of freedom", argstr="--dof {dof}"
    )
    reference_mask: ty.Any = shell.arg(
        help="mask reference volume with given mask, or None if ``False``",
        position=2,
        formatter="reference_mask_formatter",
    )
    source_mask: str = shell.arg(
        help="mask source file with given mask", argstr="--mov-mask"
    )
    num_threads: int = shell.arg(
        help="number of OpenMP threads", argstr="--threads {num_threads}"
    )
    no_coord_dithering: bool = shell.arg(
        help="turn off coordinate dithering", argstr="--no-coord-dither"
    )
    no_intensity_dithering: bool = shell.arg(
        help="turn off intensity dithering", argstr="--no-intensity-dither"
    )
    sep: list[ty.Any] = shell.arg(
        help="set spatial scales, in voxels (default [2, 4])", argstr="--sep {sep}..."
    )
    initial_translation: ty.Any = shell.arg(
        help="initial translation in mm (implies no_cras0)",
        argstr="--trans {initial_translation[0]} {initial_translation[1]} {initial_translation[2]}",
    )
    initial_rotation: ty.Any = shell.arg(
        help="initial rotation in degrees",
        argstr="--rot {initial_rotation[0]} {initial_rotation[1]} {initial_rotation[2]}",
    )
    initial_scale: ty.Any = shell.arg(
        help="initial scale",
        argstr="--scale {initial_scale[0]} {initial_scale[1]} {initial_scale[2]}",
    )
    initial_shear: ty.Any = shell.arg(
        help="initial shear (Hxy, Hxz, Hyz)",
        argstr="--shear {initial_shear[0]} {initial_shear[1]} {initial_shear[2]}",
    )
    no_cras0: bool = shell.arg(
        help="do not set translation parameters to align centers of source and reference files",
        argstr="--no-cras0",
    )
    max_iters: ty.Any = shell.arg(
        help="maximum iterations (default: 4)", argstr="--nitersmax {max_iters}"
    )
    ftol: float = shell.arg(
        help="floating-point tolerance (default=1e-7)", argstr="--ftol %e"
    )
    linmintol: float = shell.arg(help="", argstr="--linmintol %e")
    saturation_threshold: ty.Any = shell.arg(
        help="saturation threshold (default=9.999)",
        argstr="--sat {saturation_threshold}",
    )
    conform_reference: bool = shell.arg(
        help="conform reference without rescaling", argstr="--conf-ref"
    )
    no_brute_force: bool = shell.arg(help="do not brute force search", argstr="--no-bf")
    brute_force_limit: float | None = shell.arg(
        help="constrain brute force search to +/- lim",
        argstr="--bf-lim {brute_force_limit}",
    )
    brute_force_samples: int | None = shell.arg(
        help="number of samples in brute force search",
        argstr="--bf-nsamp {brute_force_samples}",
    )
    no_smooth: bool = shell.arg(
        help="do not apply smoothing to either reference or source file",
        argstr="--no-smooth",
    )
    ref_fwhm: float = shell.arg(
        help="apply smoothing to reference file", argstr="--ref-fwhm"
    )
    source_oob: bool = shell.arg(
        help="count source voxels that are out-of-bounds as 0", argstr="--mov-oob"
    )

    class Outputs(shell.Outputs):
        out_reg_file: File | None = shell.out(
            help="output registration file", callable=out_reg_file_callable
        )
        out_lta_file: File | None = shell.out(
            help="output LTA-style registration file", callable=out_lta_file_callable
        )
        out_params_file: File | None = shell.out(
            help="output parameters file", callable=out_params_file_callable
        )
