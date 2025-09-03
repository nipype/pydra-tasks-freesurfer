import attrs
from fileformats.generic import Directory, File
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.join(
        inputs["subjects_dir"],
        inputs["subject_id"],
        "mri",
        inputs["out_file"],
    )
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


@shell.define
class GTMSeg(shell.Task["GTMSeg.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.petsurfer.gtm_seg import GTMSeg

    >>> task = GTMSeg()
    >>> task.subject_id = "subject_id"
    >>> task.colortable = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "gtmseg"
    subject_id: ty.Any = shell.arg(help="subject id", argstr="--s {subject_id}")
    xcerseg: bool = shell.arg(
        help="run xcerebralseg on this subject to create apas+head.mgz",
        argstr="--xcerseg",
    )
    out_file: Path = shell.arg(
        help="output volume relative to subject/mri",
        argstr="--o {out_file}",
        default="gtmseg.mgz",
    )
    upsampling_factor: int = shell.arg(
        help="upsampling factor (default is 2)", argstr="--usf {upsampling_factor}"
    )
    subsegwm: bool = shell.arg(
        help="subsegment WM into lobes (default)", argstr="--subsegwm"
    )
    keep_hypo: bool = shell.arg(
        help="do not relabel hypointensities as WM when subsegmenting WM",
        argstr="--keep-hypo",
    )
    keep_cc: bool = shell.arg(
        help="do not relabel corpus callosum as WM", argstr="--keep-cc"
    )
    dmax: float = shell.arg(
        help="distance threshold to use when subsegmenting WM (default is 5)",
        argstr="--dmax {dmax}",
    )
    ctx_annot: ty.Any = shell.arg(
        help="annot lhbase rhbase : annotation to use for cortical segmentation (default is aparc 1000 2000)",
        argstr="--ctx-annot {ctx_annot[0]} {ctx_annot[1]} {ctx_annot[2]}",
    )
    wm_annot: ty.Any = shell.arg(
        help="annot lhbase rhbase : annotation to use for WM segmentation (with --subsegwm, default is lobes 3200 4200)",
        argstr="--wm-annot {wm_annot[0]} {wm_annot[1]} {wm_annot[2]}",
    )
    output_upsampling_factor: int = shell.arg(
        help="set output USF different than USF, mostly for debugging",
        argstr="--output-usf {output_upsampling_factor}",
    )
    head: ty.Any = shell.arg(
        help="use headseg instead of apas+head.mgz", argstr="--head {head}"
    )
    subseg_cblum_wm: bool = shell.arg(
        help="subsegment cerebellum WM into core and gyri", argstr="--subseg-cblum-wm"
    )
    no_pons: bool = shell.arg(
        help="do not add pons segmentation when doing ---xcerseg", argstr="--no-pons"
    )
    no_vermis: bool = shell.arg(
        help="do not add vermis segmentation when doing ---xcerseg",
        argstr="--no-vermis",
    )
    colortable: File = shell.arg(help="colortable", argstr="--ctab {colortable}")
    no_seg_stats: bool = shell.arg(
        help="do not compute segmentation stats", argstr="--no-seg-stats"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="GTM segmentation", callable=out_file_callable
        )
