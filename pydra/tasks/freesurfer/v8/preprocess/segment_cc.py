import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Lta
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import shutil
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name in ["in_file", "in_norm", "out_file"]:

        basename = os.path.basename(value)
        return argstr.format(**{name: basename})

    return argstr.format(**inputs)


def aggregate_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    needed_outputs = ["out_rotation"]

    predicted_outputs = _list_outputs(
        out_file=inputs["out_file"],
        out_rotation=inputs["out_rotation"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    for name in ["out_file", "out_rotation"]:
        out_file = predicted_outputs[name]
        if not os.path.isfile(out_file):
            out_base = os.path.basename(out_file)
            if inputs["subjects_dir"] is not attrs.NOTHING:
                subj_dir = os.path.join(inputs["subjects_dir"], inputs["subject_id"])
            else:
                subj_dir = os.path.join(os.getcwd(), inputs["subject_id"])
            if name == "out_file":
                out_tmp = os.path.join(subj_dir, "mri", out_base)
            elif name == "out_rotation":
                out_tmp = os.path.join(subj_dir, "mri", "transforms", out_base)
            else:
                out_tmp = None

            if out_tmp and os.path.isfile(out_tmp):
                if not os.path.isdir(os.path.dirname(out_tmp)):
                    os.makedirs(os.path.dirname(out_tmp))
                shutil.move(out_tmp, out_file)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):

    outputs = {}
    outputs["out_file"] = os.path.abspath(inputs["out_file"])
    outputs["out_rotation"] = os.path.abspath(inputs["out_rotation"])
    return outputs


def out_rotation_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_rotation")


@shell.define
class SegmentCC(shell.Task["SegmentCC.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Lta
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.segment_cc import SegmentCC

    >>> task = SegmentCC()
    >>> task.in_file = MghGz.mock("aseg.mgz")
    >>> task.in_norm = File.mock()
    >>> task.out_rotation = "cc.lta"
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_cc"
    in_file: MghGz = shell.arg(
        help="Input aseg file to read from subjects directory", argstr="-aseg {in_file}"
    )
    in_norm: File = shell.arg(help="Required undocumented input {subject}/mri/norm.mgz")
    out_rotation: Path = shell.arg(
        help="Global filepath for writing rotation lta", argstr="-lta {out_rotation}"
    )
    subject_id: ty.Any | None = shell.arg(
        help="Subject name", argstr="{subject_id}", position=-1, default="subject_id"
    )
    copy_inputs: bool = shell.arg(
        help="If running as a node, set this to True. This will copy the input files to the node directory."
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Filename to write aseg including CC",
            argstr="-o {out_file}",
            path_template="{in_file}.auto.mgz",
        )
        out_rotation: Lta | None = shell.out(
            help="Output lta rotation file", callable=out_rotation_callable
        )
