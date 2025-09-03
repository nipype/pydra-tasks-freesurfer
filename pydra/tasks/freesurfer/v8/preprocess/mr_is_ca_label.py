from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


@shell.define
class MRIsCALabel(shell.Task["MRIsCALabel.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.mr_is_ca_label import MRIsCALabel

    >>> task = MRIsCALabel()
    >>> task.subject_id = "test"
    >>> task.canonsurf = Pial.mock("lh.pial")
    >>> task.classifier = File.mock()
    >>> task.smoothwm = Pial.mock("lh.pial")
    >>> task.curv = File.mock()
    >>> task.sulc = Pial.mock("lh.pial")
    >>> task.label = File.mock()
    >>> task.aseg = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_ca_label test lh lh.pial im1.nii lh.aparc.annot'


    """

    executable = "mris_ca_label"
    subject_id: ty.Any | None = shell.arg(
        help="Subject name or ID",
        argstr="{subject_id}",
        position=-5,
        default="subject_id",
    )
    hemisphere: ty.Any = shell.arg(
        help="Hemisphere ('lh' or 'rh')", argstr="{hemisphere}", position=-4
    )
    canonsurf: Pial = shell.arg(
        help="Input canonical surface file", argstr="{canonsurf}", position=-3
    )
    classifier: File = shell.arg(
        help="Classifier array input file", argstr="{classifier}", position=-2
    )
    smoothwm: Pial = shell.arg(help="implicit input {hemisphere}.smoothwm")
    curv: File = shell.arg(help="implicit input {hemisphere}.curv")
    sulc: Pial = shell.arg(help="implicit input {hemisphere}.sulc")
    label: File = shell.arg(
        help="Undocumented flag. Autorecon3 uses ../label/{hemisphere}.cortex.label as input file",
        argstr="-l {label}",
    )
    aseg: File = shell.arg(
        help="Undocumented flag. Autorecon3 uses ../mri/aseg.presurf.mgz as input file",
        argstr="-aseg {aseg}",
    )
    seed: int = shell.arg(help="", argstr="-seed {seed}")
    copy_inputs: bool = shell.arg(
        help="Copies implicit inputs to node directory and creates a temp subjects_directory. Use this when running as a node"
    )
    num_threads: int = shell.arg(help="allows for specifying more threads")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Annotated surface output file",
            argstr="{out_file}",
            position=-1,
            path_template="{hemisphere}.aparc.annot",
        )
