import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import fname_presuffix
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "transformed_file":
        return _get_outfile(
            fs_target=inputs["fs_target"],
            inverse=inputs["inverse"],
            source_file=inputs["source_file"],
            target_file=inputs["target_file"],
            transformed_file=inputs["transformed_file"],
        )
    return None


def transformed_file_default(inputs):
    return _gen_filename("transformed_file", inputs=inputs)


@shell.define(
    xor=[
        ["fs_target", "tal", "target_file"],
        [
            "fsl_reg_file",
            "lta_file",
            "lta_inv_file",
            "mni_152_reg",
            "reg_file",
            "reg_header",
            "subject",
            "xfm_reg_file",
        ],
    ]
)
class ApplyVolTransform(shell.Task["ApplyVolTransform.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.apply_vol_transform import ApplyVolTransform

    >>> task = ApplyVolTransform()
    >>> task.source_file = Nifti1.mock("structural.nii")
    >>> task.transformed_file = "struct_warped.nii"
    >>> task.target_file = File.mock()
    >>> task.reg_file = File.mock()
    >>> task.lta_file = File.mock()
    >>> task.lta_inv_file = File.mock()
    >>> task.fsl_reg_file = File.mock()
    >>> task.xfm_reg_file = File.mock()
    >>> task.m3z_file = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_vol2vol --fstarg --reg register.dat --mov structural.nii --o struct_warped.nii'


    """

    executable = "mri_vol2vol"
    source_file: Nifti1 = shell.arg(
        help="Input volume you wish to transform", argstr="--mov {source_file}"
    )
    target_file: File | None = shell.arg(
        help="Output template volume", argstr="--targ {target_file}"
    )
    tal: bool = shell.arg(
        help="map to a sub FOV of MNI305 (with --reg only)", argstr="--tal"
    )
    tal_resolution: float = shell.arg(
        help="Resolution to sample when using tal",
        argstr="--talres {tal_resolution:.10}",
    )
    fs_target: bool = shell.arg(
        help="use orig.mgz from subject in regfile as target",
        argstr="--fstarg",
        requires=["reg_file"],
    )
    reg_file: File | None = shell.arg(
        help="tkRAS-to-tkRAS matrix   (tkregister2 format)", argstr="--reg {reg_file}"
    )
    lta_file: File | None = shell.arg(
        help="Linear Transform Array file", argstr="--lta {lta_file}"
    )
    lta_inv_file: File | None = shell.arg(
        help="LTA, invert", argstr="--lta-inv {lta_inv_file}"
    )
    fsl_reg_file: File | None = shell.arg(
        help="fslRAS-to-fslRAS matrix (FSL format)", argstr="--fsl {fsl_reg_file}"
    )
    xfm_reg_file: File | None = shell.arg(
        help="ScannerRAS-to-ScannerRAS matrix (MNI format)",
        argstr="--xfm {xfm_reg_file}",
    )
    reg_header: bool = shell.arg(
        help="ScannerRAS-to-ScannerRAS matrix = identity", argstr="--regheader"
    )
    mni_152_reg: bool = shell.arg(help="target MNI152 space", argstr="--regheader")
    subject: str = shell.arg(
        help="set matrix = identity and use subject for any templates",
        argstr="--s {subject}",
    )
    inverse: bool = shell.arg(help="sample from target to source", argstr="--inv")
    interp: ty.Any = shell.arg(
        help="Interpolation method (<trilin> or nearest)", argstr="--interp {interp}"
    )
    no_resample: bool = shell.arg(
        help="Do not resample; just change vox2ras matrix", argstr="--no-resample"
    )
    m3z_file: File = shell.arg(
        help="This is the morph to be applied to the volume. Unless the morph is in mri/transforms (eg.: for talairach.m3z computed by reconall), you will need to specify the full path to this morph and use the --noDefM3zPath flag.",
        argstr="--m3z {m3z_file}",
    )
    no_ded_m3z_path: bool = shell.arg(
        help="To be used with the m3z flag. Instructs the code not to look for them3z morph in the default location (SUBJECTS_DIR/subj/mri/transforms), but instead just use the path indicated in --m3z.",
        argstr="--noDefM3zPath",
        requires=["m3z_file"],
    )
    invert_morph: bool = shell.arg(
        help="Compute and use the inverse of the non-linear morph to resample the input volume. To be used by --m3z.",
        argstr="--inv-morph",
        requires=["m3z_file"],
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        transformed_file: Path = shell.outarg(
            help="Output volume",
            argstr="--o {transformed_file}",
            path_template='"struct_warped.nii"',
        )


def _get_outfile(
    fs_target=None,
    inverse=None,
    source_file=None,
    target_file=None,
    transformed_file=None,
):
    outfile = transformed_file
    if outfile is attrs.NOTHING:
        if inverse is True:
            if fs_target is True:
                src = "orig.mgz"
            else:
                src = target_file
        else:
            src = source_file
        outfile = fname_presuffix(src, newpath=output_dir, suffix="_warped")
    return outfile
