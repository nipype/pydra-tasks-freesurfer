from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "source_file",
        specs.File,
        {
            "help_string": "Input volume you wish to transform",
            "argstr": "--mov {source_file}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "transformed_file",
        str,
        {
            "help_string": "Output volume",
            "argstr": "--o {transformed_file}",
            "output_file_template": "{source_file}_warped",
        },
    ),
    (
        "target_file",
        specs.File,
        {
            "help_string": "Output template volume",
            "argstr": "--targ {target_file}",
            "mandatory": True,
            "xor": ("target_file", "tal", "fs_target"),
        },
    ),
    (
        "tal",
        bool,
        {
            "help_string": "map to a sub FOV of MNI305 (with --reg only)",
            "argstr": "--tal",
            "mandatory": True,
            "xor": ("target_file", "tal", "fs_target"),
        },
    ),
    (
        "tal_resolution",
        float,
        {
            "help_string": "Resolution to sample when using tal",
            "argstr": "--talres {tal_resolution:.10f}",
        },
    ),
    (
        "fs_target",
        bool,
        {
            "help_string": "use orig.mgz from subject in regfile as target",
            "argstr": "--fstarg",
            "mandatory": True,
            "requires": ["reg_file"],
            "xor": ("target_file", "tal", "fs_target"),
        },
    ),
    (
        "reg_file",
        specs.File,
        {
            "help_string": "tkRAS-to-tkRAS matrix   (tkregister2 format)",
            "argstr": "--reg {reg_file}",
            "mandatory": True,
            "xor": (
                "reg_file",
                "lta_file",
                "lta_inv_file",
                "fsl_reg_file",
                "xfm_reg_file",
                "reg_header",
                "mni_152_reg",
                "subject",
            ),
        },
    ),
    (
        "lta_file",
        specs.File,
        {
            "help_string": "Linear Transform Array file",
            "argstr": "--lta {lta_file}",
            "mandatory": True,
            "xor": (
                "reg_file",
                "lta_file",
                "lta_inv_file",
                "fsl_reg_file",
                "xfm_reg_file",
                "reg_header",
                "mni_152_reg",
                "subject",
            ),
        },
    ),
    (
        "lta_inv_file",
        specs.File,
        {
            "help_string": "LTA, invert",
            "argstr": "--lta-inv {lta_inv_file}",
            "mandatory": True,
            "xor": (
                "reg_file",
                "lta_file",
                "lta_inv_file",
                "fsl_reg_file",
                "xfm_reg_file",
                "reg_header",
                "mni_152_reg",
                "subject",
            ),
        },
    ),
    (
        "fsl_reg_file",
        specs.File,
        {
            "help_string": "fslRAS-to-fslRAS matrix (FSL format)",
            "argstr": "--fsl {fsl_reg_file}",
            "mandatory": True,
            "xor": (
                "reg_file",
                "lta_file",
                "lta_inv_file",
                "fsl_reg_file",
                "xfm_reg_file",
                "reg_header",
                "mni_152_reg",
                "subject",
            ),
        },
    ),
    (
        "xfm_reg_file",
        specs.File,
        {
            "help_string": "ScannerRAS-to-ScannerRAS matrix (MNI format)",
            "argstr": "--xfm {xfm_reg_file}",
            "mandatory": True,
            "xor": (
                "reg_file",
                "lta_file",
                "lta_inv_file",
                "fsl_reg_file",
                "xfm_reg_file",
                "reg_header",
                "mni_152_reg",
                "subject",
            ),
        },
    ),
    (
        "reg_header",
        bool,
        {
            "help_string": "ScannerRAS-to-ScannerRAS matrix = identity",
            "argstr": "--regheader",
            "mandatory": True,
            "xor": (
                "reg_file",
                "lta_file",
                "lta_inv_file",
                "fsl_reg_file",
                "xfm_reg_file",
                "reg_header",
                "mni_152_reg",
                "subject",
            ),
        },
    ),
    (
        "mni_152_reg",
        bool,
        {
            "help_string": "target MNI152 space",
            "argstr": "--regheader",
            "mandatory": True,
            "xor": (
                "reg_file",
                "lta_file",
                "lta_inv_file",
                "fsl_reg_file",
                "xfm_reg_file",
                "reg_header",
                "mni_152_reg",
                "subject",
            ),
        },
    ),
    (
        "subject",
        str,
        {
            "help_string": "set matrix = identity and use subject for any templates",
            "argstr": "--s {subject}",
            "mandatory": True,
            "xor": (
                "reg_file",
                "lta_file",
                "lta_inv_file",
                "fsl_reg_file",
                "xfm_reg_file",
                "reg_header",
                "mni_152_reg",
                "subject",
            ),
        },
    ),
    (
        "inverse",
        bool,
        {"help_string": "sample from target to source", "argstr": "--inv"},
    ),
    (
        "interp",
        ty.Any,
        {
            "help_string": "Interpolation method (<trilin> or nearest)",
            "argstr": "--interp {interp}",
        },
    ),
    (
        "no_resample",
        bool,
        {
            "help_string": "Do not resample; just change vox2ras matrix",
            "argstr": "--no-resample",
        },
    ),
    (
        "m3z_file",
        str,
        {
            "help_string": "This is the morph to be applied to the volume. Unless the morph is in mri/transforms (eg.: for talairach.m3z computed by reconall), you will need to specify the full path to this morph and use the --noDefM3zPath flag.",
            "argstr": "--m3z {m3z_file}",
        },
    ),
    (
        "no_ded_m3z_path",
        bool,
        {
            "help_string": "To be used with the m3z flag. Instructs the code not to look for them3z morph in the default location (SUBJECTS_DIR/subj/mri/transforms), but instead just use the path indicated in --m3z.",
            "argstr": "--noDefM3zPath",
            "requires": ["m3z_file"],
        },
    ),
    (
        "invert_morph",
        bool,
        {
            "help_string": "Compute and use the inverse of the non-linear morph to resample the input volume. To be used by --m3z.",
            "argstr": "--inv-morph",
            "requires": ["m3z_file"],
        },
    ),
    ("subjects_dir", ty.Any, {"help_string": "subjects directory"}),
]
ApplyVolTransform_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ApplyVolTransform_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ApplyVolTransform(ShellCommandTask):
    """
    Example
    -------
    >>> task = ApplyVolTransform()
    >>> task.inputs.source_file = "structural.nii.gz"
    >>> task.inputs.reg_file = "register.dat"
    >>> task.cmdline
    ''mri_vol2vol --fstarg --reg register.dat --mov structural.nii --o struct_warped.nii''
    """

    input_spec = ApplyVolTransform_input_spec
    output_spec = ApplyVolTransform_output_spec
    executable = "mri_vol2vol"
