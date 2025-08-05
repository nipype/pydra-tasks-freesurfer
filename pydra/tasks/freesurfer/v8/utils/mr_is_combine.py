from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pathlib._local import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define
class MRIsCombine(shell.Task["MRIsCombine.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib._local import Path
    >>> from pydra.tasks.freesurfer.v8.utils.mr_is_combine import MRIsCombine

    >>> task = MRIsCombine()
    >>> task.inputs.in_files = [Pial.mock("lh.pial"), Pial.mock("rh.pial")]
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mris_convert --combinesurfs lh.pial rh.pial bh.pial'


    """

    executable = "mris_convert"
    in_files: list[Pial] = shell.arg(
        help="Two surfaces to be combined.",
        argstr="--combinesurfs {in_files}",
        position=1,
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Output filename. Combined surfaces from in_files.",
            argstr="{out_file}",
            position=-1,
            path_template="out_file",
        )
