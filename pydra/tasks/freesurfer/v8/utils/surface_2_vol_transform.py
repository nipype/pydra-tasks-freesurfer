from fileformats.generic import File
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define(xor=[["mkmask", "source_file"], ["reg_file", "subject_id"]])
class Surface2VolTransform(shell.Task["Surface2VolTransform.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.surface_2_vol_transform import Surface2VolTransform

    >>> task = Surface2VolTransform()
    >>> task.source_file = MghGz.mock("lh.cope1.mgz")
    >>> task.hemi = "lh"
    >>> task.reg_file = File.mock()
    >>> task.template_file = File.mock()
    >>> task.subjects_dir = "."
    >>> task.cmdline
    'mri_surf2vol --hemi lh --volreg register.mat --surfval lh.cope1.mgz --sd . --template cope1.nii.gz --outvol lh.cope1_asVol.nii --vtxvol lh.cope1_asVol_vertex.nii'


    """

    executable = "mri_surf2vol"
    source_file: MghGz | None = shell.arg(
        help="This is the source of the surface values",
        argstr="--surfval {source_file}",
    )
    hemi: str = shell.arg(help="hemisphere of data", argstr="--hemi {hemi}")
    reg_file: File | None = shell.arg(
        help="tkRAS-to-tkRAS matrix   (tkregister2 format)",
        argstr="--volreg {reg_file}",
    )
    template_file: File = shell.arg(
        help="Output template volume", argstr="--template {template_file}"
    )
    mkmask: bool = shell.arg(
        help="make a mask instead of loading surface values", argstr="--mkmask"
    )
    surf_name: str = shell.arg(
        help="surfname (default is white)", argstr="--surf {surf_name}"
    )
    projfrac: float = shell.arg(
        help="thickness fraction", argstr="--projfrac {projfrac}"
    )
    subjects_dir: str = shell.arg(
        help="freesurfer subjects directory defaults to $SUBJECTS_DIR",
        argstr="--sd {subjects_dir}",
    )
    subject_id: str = shell.arg(help="subject id", argstr="--identity {subject_id}")

    class Outputs(shell.Outputs):
        transformed_file: Path = shell.outarg(
            help="Output volume",
            argstr="--outvol {transformed_file}",
            path_template="{source_file}_asVol.nii",
        )
        vertexvol_file: Path = shell.outarg(
            help="Path name of the vertex output volume, which is the same as output volume except that the value of each voxel is the vertex-id that is mapped to that voxel.",
            argstr="--vtxvol {vertexvol_file}",
            path_template="{source_file}_asVol_vertex.nii",
        )
