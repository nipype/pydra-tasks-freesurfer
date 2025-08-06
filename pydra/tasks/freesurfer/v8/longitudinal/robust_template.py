import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
from fileformats.medimage_freesurfer import Lta
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

    if name == "average_metric":

        return argstr.format(**{name: {"mean": 0, "median": 1}[value]})
    if name in ("transform_outputs", "scaled_intensity_outputs"):
        value = _list_outputs(
            scaled_intensity_outputs=inputs["scaled_intensity_outputs"],
            in_files=inputs["in_files"],
            transform_outputs=inputs["transform_outputs"],
            out_file=inputs["out_file"],
        )[name]

    return argstr.format(**inputs)


def average_metric_formatter(field, inputs):
    return _format_arg(
        "average_metric", field, inputs, argstr="--average {average_metric}"
    )


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.abspath(inputs["out_file"])
    n_files = len(inputs["in_files"])
    fmt = "{}{:02d}.{}" if n_files > 9 else "{}{:d}.{}"
    if inputs["transform_outputs"] is not attrs.NOTHING:
        fnames = inputs["transform_outputs"]
        if fnames is True:
            fnames = [fmt.format("tp", i + 1, "lta") for i in range(n_files)]
        outputs["transform_outputs"] = [os.path.abspath(x) for x in fnames]
    if inputs["scaled_intensity_outputs"] is not attrs.NOTHING:
        fnames = inputs["scaled_intensity_outputs"]
        if fnames is True:
            fnames = [fmt.format("is", i + 1, "txt") for i in range(n_files)]
        outputs["scaled_intensity_outputs"] = [os.path.abspath(x) for x in fnames]
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


def transform_outputs_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("transform_outputs")


def scaled_intensity_outputs_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("scaled_intensity_outputs")


@shell.define(xor=[["auto_detect_sensitivity", "outlier_sensitivity"]])
class RobustTemplate(shell.Task["RobustTemplate.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.medimage_freesurfer import Lta
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.longitudinal.robust_template import RobustTemplate

    >>> task = RobustTemplate()
    >>> task.inputs.in_files = [Nifti1.mock("structural.nii"), Nifti1.mock("functional.nii")]
    >>> task.inputs.out_file = "T1.nii"
    >>> task.inputs.subsample_threshold = 200
    >>> task.inputs.average_metric = "mean"
    >>> task.inputs.fixed_timepoint = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    >>> task = RobustTemplate()
    >>> task.inputs.transform_outputs = ["structural.lta", "functional.lta"]
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    >>> task = RobustTemplate()
    >>> task.inputs.transform_outputs = True
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_robust_template"
    in_files: list[Nifti1] = shell.arg(
        help="input movable volumes to be aligned to common mean/median template",
        argstr="--mov {in_files}",
    )
    out_file: Path | None = shell.arg(
        help="output template volume (final mean/median image)",
        argstr="--template {out_file}",
        default="mri_robust_template_out.mgz",
    )
    auto_detect_sensitivity: bool = shell.arg(
        help="auto-detect good sensitivity (recommended for head or full brain scans)",
        argstr="--satit",
    )
    outlier_sensitivity: float | None = shell.arg(
        help='set outlier sensitivity manually (e.g. "--sat 4.685" ). Higher values mean less sensitivity.',
        argstr="--sat {outlier_sensitivity:.4}",
    )
    transform_outputs: ty.Any = shell.arg(
        help="output xforms to template (for each input)",
        argstr="--lta {transform_outputs}",
    )
    intensity_scaling: bool = shell.arg(
        help="allow also intensity scaling (default off)", argstr="--iscale"
    )
    scaled_intensity_outputs: ty.Any = shell.arg(
        help="final intensity scales (will activate --iscale)",
        argstr="--iscaleout {scaled_intensity_outputs}",
    )
    subsample_threshold: int = shell.arg(
        help="subsample if dim > # on all axes (default no subs.)",
        argstr="--subsample {subsample_threshold}",
    )
    average_metric: ty.Any = shell.arg(
        help="construct template from: 0 Mean, 1 Median (default)",
        formatter="average_metric_formatter",
    )
    initial_timepoint: int = shell.arg(
        help="use TP# for special init (default random), 0: no init",
        argstr="--inittp {initial_timepoint}",
    )
    fixed_timepoint: bool = shell.arg(
        help="map everything to init TP# (init TP is not resampled)", argstr="--fixtp"
    )
    no_iteration: bool = shell.arg(
        help="do not iterate, just create first template", argstr="--noit"
    )
    initial_transforms: list[File] = shell.arg(
        help="use initial transforms (lta) on source",
        argstr="--ixforms {initial_transforms}",
    )
    in_intensity_scales: list[File] = shell.arg(
        help="use initial intensity scales", argstr="--iscalein {in_intensity_scales}"
    )
    num_threads: int = shell.arg(help="allows for specifying more threads")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Nifti1 | None = shell.out(
            help="output template volume (final mean/median image)",
            callable=out_file_callable,
        )
        transform_outputs: list[File | Lta] | None = shell.out(
            help="output xform files from moving to template",
            callable=transform_outputs_callable,
        )
        scaled_intensity_outputs: list[File] | None = shell.out(
            help="output final intensity scales",
            callable=scaled_intensity_outputs_callable,
        )
