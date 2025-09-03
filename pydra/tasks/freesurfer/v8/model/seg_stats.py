import attrs
from fileformats.generic import Directory, File
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name in ("summary_file", "avgwf_txt_file"):
        if not isinstance(value, bool):
            if not os.path.isabs(value):
                value = os.path.join(".", value)
    if name in ["avgwf_txt_file", "avgwf_file", "sf_avg_file"]:
        if isinstance(value, bool):
            fname = _list_outputs(
                annot=inputs["annot"],
                segmentation_file=inputs["segmentation_file"],
                summary_file=inputs["summary_file"],
                surf_label=inputs["surf_label"],
            )[name]
        else:
            fname = value
        return argstr.format(**{name: fname})
    elif name == "in_intensity":
        intensity_name = os.path.basename(inputs["in_intensity"]).replace(".mgz", "")
        return argstr % (value, intensity_name)

    return argstr.format(**inputs)


def in_intensity_formatter(field, inputs):
    return _format_arg(
        "in_intensity",
        field,
        inputs,
        argstr="--in {in_intensity[0]} --in-intensity-name {in_intensity[1]}",
    )


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    self_dict = {}

    outputs = {}
    if inputs["summary_file"] is not attrs.NOTHING:
        outputs["summary_file"] = os.path.abspath(inputs["summary_file"])
    else:
        outputs["summary_file"] = os.path.join(os.getcwd(), "summary.stats")
    suffices = dict(
        avgwf_txt_file="_avgwf.txt",
        avgwf_file="_avgwf.nii.gz",
        sf_avg_file="sfavg.txt",
    )
    if inputs["segmentation_file"] is not attrs.NOTHING:
        _, src = os.path.split(inputs["segmentation_file"])
    if inputs["annot"] is not attrs.NOTHING:
        src = "_".join(inputs["annot"])
    if inputs["surf_label"] is not attrs.NOTHING:
        src = "_".join(inputs["surf_label"])
    for name, suffix in list(suffices.items()):
        value = getattr(self_dict["inputs"], name)
        if value is not attrs.NOTHING:
            if isinstance(value, bool):
                outputs[name] = fname_presuffix(
                    src, suffix=suffix, newpath=os.getcwd(), use_ext=False
                )
            else:
                outputs[name] = os.path.abspath(value)
    return outputs


def avgwf_txt_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("avgwf_txt_file")


def avgwf_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("avgwf_file")


def sf_avg_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("sf_avg_file")


def _gen_filename(name, inputs):
    if name == "summary_file":
        return _list_outputs(
            annot=inputs["annot"],
            segmentation_file=inputs["segmentation_file"],
            summary_file=inputs["summary_file"],
            surf_label=inputs["surf_label"],
        )[name]
    return None


def summary_file_default(inputs):
    return _gen_filename("summary_file", inputs=inputs)


@shell.define(
    xor=[
        ["annot", "segmentation_file", "surf_label"],
        ["color_table_file", "default_color_table", "gca_color_table"],
    ]
)
class SegStats(shell.Task["SegStats.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.model.seg_stats import SegStats

    >>> task = SegStats()
    >>> task.segmentation_file = File.mock()
    >>> task.annot = ("PWS04", "lh", "aparc")
    >>> task.summary_file = "summary.stats"
    >>> task.partial_volume_file = File.mock()
    >>> task.in_file = File.mock()
    >>> task.color_table_file = File.mock()
    >>> task.gca_color_table = File.mock()
    >>> task.mask_file = File.mock()
    >>> task.brainmask_file = File.mock()
    >>> task.in_intensity = File.mock()
    >>> task.subjects_dir = Directory.mock(".")
    >>> task.cmdline
    'None'


    """

    executable = "mri_segstats"
    segmentation_file: File | None = shell.arg(
        help="segmentation volume path", argstr="--seg {segmentation_file}"
    )
    annot: ty.Any | None = shell.arg(
        help="subject hemi parc : use surface parcellation",
        argstr="--annot {annot[0]} {annot[1]} {annot[2]}",
    )
    surf_label: ty.Any | None = shell.arg(
        help="subject hemi label : use surface label",
        argstr="--slabel {surf_label[0]} {surf_label[1]} {surf_label[2]}",
    )
    partial_volume_file: File = shell.arg(
        help="Compensate for partial voluming", argstr="--pv {partial_volume_file}"
    )
    in_file: File = shell.arg(
        help="Use the segmentation to report stats on this volume",
        argstr="--i {in_file}",
    )
    frame: int = shell.arg(
        help="Report stats on nth frame of input volume", argstr="--frame {frame}"
    )
    multiply: float = shell.arg(help="multiply input by val", argstr="--mul {multiply}")
    calc_snr: bool = shell.arg(
        help="save mean/std as extra column in output table", argstr="--snr"
    )
    calc_power: ty.Any = shell.arg(
        help="Compute either the sqr or the sqrt of the input", argstr="--{calc_power}"
    )
    color_table_file: File | None = shell.arg(
        help="color table file with seg id names", argstr="--ctab {color_table_file}"
    )
    default_color_table: bool = shell.arg(
        help="use $FREESURFER_HOME/FreeSurferColorLUT.txt", argstr="--ctab-default"
    )
    gca_color_table: File | None = shell.arg(
        help="get color table from GCA (CMA)", argstr="--ctab-gca {gca_color_table}"
    )
    segment_id: list[ty.Any] = shell.arg(
        help="Manually specify segmentation ids", argstr="--id {segment_id}..."
    )
    exclude_id: int = shell.arg(
        help="Exclude seg id from report", argstr="--excludeid {exclude_id}"
    )
    exclude_ctx_gm_wm: bool = shell.arg(
        help="exclude cortical gray and white matter", argstr="--excl-ctxgmwm"
    )
    wm_vol_from_surf: bool = shell.arg(
        help="Compute wm volume from surf", argstr="--surf-wm-vol"
    )
    cortex_vol_from_surf: bool = shell.arg(
        help="Compute cortex volume from surf", argstr="--surf-ctx-vol"
    )
    non_empty_only: bool = shell.arg(
        help="Only report nonempty segmentations", argstr="--nonempty"
    )
    empty: bool = shell.arg(
        help="Report on segmentations listed in the color table", argstr="--empty"
    )
    mask_file: File = shell.arg(
        help="Mask volume (same size as seg", argstr="--mask {mask_file}"
    )
    mask_thresh: float = shell.arg(
        help="binarize mask with this threshold <0.5>",
        argstr="--maskthresh {mask_thresh}",
    )
    mask_sign: ty.Any = shell.arg(help="Sign for mask threshold: pos, neg, or abs")
    mask_frame: int = shell.arg(
        help="Mask with this (0 based) frame of the mask volume", requires=["mask_file"]
    )
    mask_invert: bool = shell.arg(
        help="Invert binarized mask volume", argstr="--maskinvert"
    )
    mask_erode: int = shell.arg(
        help="Erode mask by some amount", argstr="--maskerode {mask_erode}"
    )
    brain_vol: ty.Any = shell.arg(
        help="Compute brain volume either with ``brainmask`` or ``brain-vol-from-seg``",
        argstr="--{brain_vol}",
    )
    brainmask_file: File = shell.arg(
        help="Load brain mask and compute the volume of the brain as the non-zero voxels in this volume",
        argstr="--brainmask {brainmask_file}",
    )
    etiv: bool = shell.arg(help="Compute ICV from talairach transform", argstr="--etiv")
    etiv_only: ty.Any = shell.arg(
        help="Compute etiv and exit.  Use ``etiv`` or ``old-etiv``"
    )
    avgwf_txt_file: ty.Any = shell.arg(
        help="Save average waveform into file (bool or filename)",
        argstr="--avgwf {avgwf_txt_file}",
    )
    avgwf_file: ty.Any = shell.arg(
        help="Save as binary volume (bool or filename)",
        argstr="--avgwfvol {avgwf_file}",
    )
    sf_avg_file: ty.Any = shell.arg(
        help="Save mean across space and time", argstr="--sfavg {sf_avg_file}"
    )
    vox: list[int] = shell.arg(
        help="Replace seg with all 0s except at C R S (three int inputs)",
        argstr="--vox {vox}",
    )
    supratent: bool = shell.arg(help="Undocumented input flag", argstr="--supratent")
    subcort_gm: bool = shell.arg(
        help="Compute volume of subcortical gray matter", argstr="--subcortgray"
    )
    total_gray: bool = shell.arg(
        help="Compute volume of total gray matter", argstr="--totalgray"
    )
    euler: bool = shell.arg(
        help="Write out number of defect holes in orig.nofix based on the euler number",
        argstr="--euler",
    )
    in_intensity: File = shell.arg(
        help="Undocumented input norm.mgz file", formatter="in_intensity_formatter"
    )
    intensity_units: ty.Any = shell.arg(
        help="Intensity units",
        argstr="--in-intensity-units {intensity_units}",
        requires=["in_intensity"],
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        summary_file: Path = shell.outarg(
            help="Segmentation stats summary table file",
            argstr="--sum {summary_file}",
            position=-1,
            path_template='"summary.stats"',
        )
        avgwf_txt_file: File | None = shell.out(
            help="Text file with functional statistics averaged over segs",
            callable=avgwf_txt_file_callable,
        )
        avgwf_file: File | None = shell.out(
            help="Volume with functional statistics averaged over segs",
            callable=avgwf_file_callable,
        )
        sf_avg_file: File | None = shell.out(
            help="Text file with func statistics averaged over segs and framss",
            callable=sf_avg_file_callable,
        )
