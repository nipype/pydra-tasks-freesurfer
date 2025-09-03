import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Annot, White
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    subject_dir = os.path.join(inputs["subjects_dir"], inputs["subject_id"])
    outputs["out_contrast"] = os.path.join(
        subject_dir, "surf", str(inputs["hemisphere"]) + ".w-g.pct.mgh"
    )
    outputs["out_stats"] = os.path.join(
        subject_dir, "stats", str(inputs["hemisphere"]) + ".w-g.pct.stats"
    )
    outputs["out_log"] = os.path.join(subject_dir, "scripts", "pctsurfcon.log")
    return outputs


def out_contrast_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_contrast")


def out_stats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_stats")


def out_log_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_log")


@shell.define
class Contrast(shell.Task["Contrast.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Annot, White
    >>> from pydra.tasks.freesurfer.v8.utils.contrast import Contrast

    >>> task = Contrast()
    >>> task.subject_id = "10335"
    >>> task.thickness = File.mock()
    >>> task.white = White.mock("lh.white" # doctest: +SKIP)
    >>> task.annotation = Annot.mock("../label/lh.aparc.annot" # doctest: +SKIP)
    >>> task.cortex = File.mock()
    >>> task.orig = File.mock()
    >>> task.rawavg = MghGz.mock("../mri/rawavg.mgz" # doctest: +SKIP)
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "pctsurfcon"
    subject_id: ty.Any | None = shell.arg(
        help="Subject being processed", argstr="--s {subject_id}", default="subject_id"
    )
    hemisphere: ty.Any = shell.arg(
        help="Hemisphere being processed", argstr="--{hemisphere}-only"
    )
    thickness: File = shell.arg(
        help="Input file must be <subject_id>/surf/?h.thickness"
    )
    white: White = shell.arg(
        help="Input file must be <subject_id>/surf/<hemisphere>.white"
    )
    annotation: Annot = shell.arg(
        help="Input annotation file must be <subject_id>/label/<hemisphere>.aparc.annot"
    )
    cortex: File = shell.arg(
        help="Input cortex label must be <subject_id>/label/<hemisphere>.cortex.label"
    )
    orig: File = shell.arg(help="Implicit input file mri/orig.mgz")
    rawavg: MghGz = shell.arg(help="Implicit input file mri/rawavg.mgz")
    copy_inputs: bool = shell.arg(
        help="If running as a node, set this to True. This will copy the input files to the node directory."
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_contrast: File | None = shell.out(
            help="Output contrast file from Contrast", callable=out_contrast_callable
        )
        out_stats: File | None = shell.out(
            help="Output stats file from Contrast", callable=out_stats_callable
        )
        out_log: File | None = shell.out(
            help="Output log from Contrast", callable=out_log_callable
        )
