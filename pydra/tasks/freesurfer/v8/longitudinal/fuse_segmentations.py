import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
from pydra.utils.typing import MultiInputObj
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name in ("in_segmentations", "in_segmentations_noCC", "in_norms"):

        return argstr.format(**{name: os.path.basename(value[0])})

    return argstr.format(**inputs)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.abspath(inputs["out_file"])
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


@shell.define
class FuseSegmentations(shell.Task["FuseSegmentations.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.longitudinal.fuse_segmentations import FuseSegmentations
    >>> from pydra.utils.typing import MultiInputObj

    >>> task = FuseSegmentations()
    >>> task.subject_id = "tp.long.A.template"
    >>> task.out_file = "aseg.fused.mgz"
    >>> task.in_segmentations_noCC = [MghGz.mock("aseg.mgz"), MghGz.mock("aseg.mgz")]
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_fuse_segmentations"
    subject_id: ty.Any = shell.arg(
        help="subject_id being processed", argstr="{subject_id}", position=-3
    )
    timepoints: MultiInputObj = shell.arg(
        help="subject_ids or timepoints to be processed",
        argstr="{timepoints}",
        position=-2,
    )
    out_file: Path = shell.arg(help="output fused segmentation file", position=-1)
    in_segmentations: list[File] = shell.arg(
        help="name of aseg file to use (default: aseg.mgz)         must include the aseg files for all the given timepoints",
        argstr="-a {in_segmentations}",
    )
    in_segmentations_noCC: list[MghGz] = shell.arg(
        help="name of aseg file w/o CC labels (default: aseg.auto_noCCseg.mgz)         must include the corresponding file for all the given timepoints",
        argstr="-c {in_segmentations_noCC}",
    )
    in_norms: list[File] = shell.arg(
        help="-n <filename>  - name of norm file to use (default: norm.mgs)         must include the corresponding norm file for all given timepoints         as well as for the current subject",
        argstr="-n {in_norms}",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: MghGz | None = shell.out(
            help="output fused segmentation file", callable=out_file_callable
        )
