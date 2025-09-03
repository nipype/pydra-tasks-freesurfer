import attrs
from fileformats.generic import Directory, File
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.join(
        str(inputs["subjects_dir"]),
        str(inputs["subject_id"]),
        "label",
        str(inputs["hemisphere"]) + "." + str(inputs["out_annot"]) + ".annot",
    )
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


@shell.define
class Label2Annot(shell.Task["Label2Annot.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.v8.model.label_2_annot import Label2Annot

    >>> task = Label2Annot()
    >>> task.hemisphere = "lh"
    >>> task.in_labels = ["lh.aparc.label"]
    >>> task.out_annot = "test"
    >>> task.orig = File.mock()
    >>> task.color_table = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_label2annot"
    hemisphere: ty.Any = shell.arg(
        help="Input hemisphere", argstr="--hemi {hemisphere}"
    )
    subject_id: ty.Any | None = shell.arg(
        help="Subject name/ID", argstr="--s {subject_id}", default="subject_id"
    )
    in_labels: list[ty.Any] = shell.arg(
        help="List of input label files", argstr="--l {in_labels}..."
    )
    out_annot: ty.Any = shell.arg(
        help="Name of the annotation to create", argstr="--a {out_annot}"
    )
    orig: File = shell.arg(help="implicit {hemisphere}.orig")
    keep_max: bool = shell.arg(
        help="Keep label with highest 'stat' value", argstr="--maxstatwinner"
    )
    verbose_off: bool = shell.arg(
        help="Turn off overlap and stat override messages", argstr="--noverbose"
    )
    color_table: File = shell.arg(
        help="File that defines the structure names, their indices, and their color",
        argstr="--ctab {color_table}",
    )
    copy_inputs: bool = shell.arg(
        help="copy implicit inputs and create a temp subjects_dir"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="Output annotation file", callable=out_file_callable
        )
