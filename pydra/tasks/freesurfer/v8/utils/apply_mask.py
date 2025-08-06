from fileformats.generic import Directory, File
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define
class ApplyMask(shell.Task["ApplyMask.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.apply_mask import ApplyMask

    """

    executable = "mri_mask"
    in_file: File = shell.arg(
        help="input image (will be masked)", argstr="{in_file}", position=-3
    )
    mask_file: File = shell.arg(
        help="image defining mask space", argstr="{mask_file}", position=-2
    )
    xfm_file: File = shell.arg(
        help="LTA-format transformation matrix to align mask with input",
        argstr="-xform {xfm_file}",
    )
    invert_xfm: bool = shell.arg(help="invert transformation", argstr="-invert")
    xfm_source: File = shell.arg(
        help="image defining transform source space", argstr="-lta_src {xfm_source}"
    )
    xfm_target: File = shell.arg(
        help="image defining transform target space", argstr="-lta_dst {xfm_target}"
    )
    use_abs: bool = shell.arg(
        help="take absolute value of mask before applying", argstr="-abs"
    )
    mask_thresh: float = shell.arg(
        help="threshold mask before applying", argstr="-T {mask_thresh:.4}"
    )
    keep_mask_deletion_edits: bool = shell.arg(
        help="transfer voxel-deletion edits (voxels=1) from mask to out vol",
        argstr="-keep_mask_deletion_edits",
    )
    transfer: int = shell.arg(
        help="transfer only voxel value # from mask to out",
        argstr="-transfer {transfer}",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="final image to write",
            argstr="{out_file}",
            position=-1,
            path_template="{in_file}_masked",
        )
