from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pathlib._local import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


@shell.define
class Label2Label(shell.Task["Label2Label.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib._local import Path
    >>> from pydra.tasks.freesurfer.v8.model.label_2_label import Label2Label

    >>> task = Label2Label()
    >>> task.inputs.hemisphere = "lh"
    >>> task.inputs.sphere_reg = Pial.mock("lh.pial")
    >>> task.inputs.white = File.mock()
    >>> task.inputs.source_sphere_reg = File.mock()
    >>> task.inputs.source_white = Pial.mock("lh.pial")
    >>> task.inputs.source_label = File.mock()
    >>> task.inputs.source_subject = "fsaverage"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_label2label"
    hemisphere: ty.Any = shell.arg(
        help="Input hemisphere", argstr="--hemi {hemisphere}"
    )
    subject_id: ty.Any | None = shell.arg(
        help="Target subject", argstr="--trgsubject {subject_id}", default="subject_id"
    )
    sphere_reg: Pial = shell.arg(help="Implicit input <hemisphere>.sphere.reg")
    white: File = shell.arg(help="Implicit input <hemisphere>.white")
    source_sphere_reg: File = shell.arg(help="Implicit input <hemisphere>.sphere.reg")
    source_white: Pial = shell.arg(help="Implicit input <hemisphere>.white")
    source_label: File = shell.arg(
        help="Source label", argstr="--srclabel {source_label}"
    )
    source_subject: ty.Any = shell.arg(
        help="Source subject name", argstr="--srcsubject {source_subject}"
    )
    registration_method: ty.Any = shell.arg(
        help="Registration method",
        argstr="--regmethod {registration_method}",
        default="surface",
    )
    copy_inputs: bool = shell.arg(
        help="If running as a node, set this to True. This will copy the input files to the node directory."
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Target label",
            argstr="--trglabel {out_file}",
            path_template="{source_label}_converted",
        )
