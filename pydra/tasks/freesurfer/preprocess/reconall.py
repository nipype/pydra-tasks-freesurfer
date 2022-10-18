from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "subject_id",
        str,
        "recon_all",
        {"help_string": "subject name", "argstr": "-subjid {subject_id}"},
    ),
    (
        "directive",
        ty.Any,
        "all",
        {"help_string": "process directive", "argstr": "-{directive}", "position": 0},
    ),
    (
        "hemi",
        ty.Any,
        {"help_string": "hemisphere to process", "argstr": "-hemi {hemi}"},
    ),
    (
        "T1_files",
        specs.MultiInputFile,
        {"help_string": "name of T1 file to process", "argstr": "-i {T1_files}..."},
    ),
    (
        "T2_file",
        specs.File,
        {
            "help_string": "Convert T2 image to orig directory",
            "argstr": "-T2 {T2_file}",
        },
    ),
    (
        "FLAIR_file",
        specs.File,
        {
            "help_string": "Convert FLAIR image to orig directory",
            "argstr": "-FLAIR {FLAIR_file}",
        },
    ),
    (
        "use_T2",
        bool,
        {
            "help_string": "Use T2 image to refine the pial surface",
            "argstr": "-T2pial",
            "xor": ["use_FLAIR"],
        },
    ),
    (
        "use_FLAIR",
        bool,
        {
            "help_string": "Use FLAIR image to refine the pial surface",
            "argstr": "-FLAIRpial",
            "xor": ["use_T2"],
        },
    ),
    (
        "openmp",
        int,
        {
            "help_string": "Number of processors to use in parallel",
            "argstr": "-openmp {openmp}",
        },
    ),
    (
        "parallel",
        bool,
        {"help_string": "Enable parallel execution", "argstr": "-parallel"},
    ),
    (
        "hires",
        bool,
        {
            "help_string": "Conform to minimum voxel size (for voxels < 1mm)",
            "argstr": "-hires",
        },
    ),
    (
        "mprage",
        bool,
        {
            "help_string": "Assume scan parameters are MGH MP-RAGE protocol, which produces darker gray matter",
            "argstr": "-mprage",
        },
    ),
    (
        "big_ventricles",
        bool,
        {
            "help_string": "For use in subjects with enlarged ventricles",
            "argstr": "-bigventricles",
        },
    ),
    (
        "brainstem",
        bool,
        {
            "help_string": "Segment brainstem structures",
            "argstr": "-brainstem-structures",
        },
    ),
    (
        "hippocampal_subfields_T1",
        bool,
        {
            "help_string": "segment hippocampal subfields using input T1 scan",
            "argstr": "-hippocampal-subfields-T1",
        },
    ),
    (
        "hippocampal_subfields_T2",
        ty.Any,
        {
            "help_string": "segment hippocampal subfields using T2 scan, identified by ID (may be combined with hippocampal_subfields_T1)",
            "argstr": "-hippocampal-subfields-T2 {hippocampal_subfields_T2} {hippocampal_subfields_T2}",
        },
    ),
    (
        "expert",
        specs.File,
        {
            "help_string": "Set parameters using expert file",
            "argstr": "-expert {expert}",
        },
    ),
    (
        "xopts",
        ty.Any,
        {
            "help_string": "Use, delete or overwrite existing expert options file",
            "argstr": "-xopts-{xopts}",
        },
    ),
    (
        "subjects_dir",
        ty.Any,
        {
            "help_string": "path to subjects directory",
            "argstr": "-sd {subjects_dir}",
            "output_file_template": "{subjects_dir}_ReconAll",
        },
    ),
    (
        "flags",
        specs.MultiInputObj,
        {"help_string": "additional parameters", "argstr": "{flags}"},
    ),
    (
        "talairach",
        str,
        {"help_string": "Flags to pass to talairach commands", "xor": ["expert"]},
    ),
    (
        "mri_normalize",
        str,
        {"help_string": "Flags to pass to mri_normalize commands", "xor": ["expert"]},
    ),
    (
        "mri_watershed",
        str,
        {"help_string": "Flags to pass to mri_watershed commands", "xor": ["expert"]},
    ),
    (
        "mri_em_register",
        str,
        {"help_string": "Flags to pass to mri_em_register commands", "xor": ["expert"]},
    ),
    (
        "mri_ca_normalize",
        str,
        {
            "help_string": "Flags to pass to mri_ca_normalize commands",
            "xor": ["expert"],
        },
    ),
    (
        "mri_ca_register",
        str,
        {"help_string": "Flags to pass to mri_ca_register commands", "xor": ["expert"]},
    ),
    (
        "mri_remove_neck",
        str,
        {"help_string": "Flags to pass to mri_remove_neck commands", "xor": ["expert"]},
    ),
    (
        "mri_ca_label",
        str,
        {"help_string": "Flags to pass to mri_ca_label commands", "xor": ["expert"]},
    ),
    (
        "mri_segstats",
        str,
        {"help_string": "Flags to pass to mri_segstats commands", "xor": ["expert"]},
    ),
    (
        "mri_mask",
        str,
        {"help_string": "Flags to pass to mri_mask commands", "xor": ["expert"]},
    ),
    (
        "mri_segment",
        str,
        {"help_string": "Flags to pass to mri_segment commands", "xor": ["expert"]},
    ),
    (
        "mri_edit_wm_with_aseg",
        str,
        {
            "help_string": "Flags to pass to mri_edit_wm_with_aseg commands",
            "xor": ["expert"],
        },
    ),
    (
        "mri_pretess",
        str,
        {"help_string": "Flags to pass to mri_pretess commands", "xor": ["expert"]},
    ),
    (
        "mri_fill",
        str,
        {"help_string": "Flags to pass to mri_fill commands", "xor": ["expert"]},
    ),
    (
        "mri_tessellate",
        str,
        {"help_string": "Flags to pass to mri_tessellate commands", "xor": ["expert"]},
    ),
    (
        "mris_smooth",
        str,
        {"help_string": "Flags to pass to mri_smooth commands", "xor": ["expert"]},
    ),
    (
        "mris_inflate",
        str,
        {"help_string": "Flags to pass to mri_inflate commands", "xor": ["expert"]},
    ),
    (
        "mris_sphere",
        str,
        {"help_string": "Flags to pass to mris_sphere commands", "xor": ["expert"]},
    ),
    (
        "mris_fix_topology",
        str,
        {
            "help_string": "Flags to pass to mris_fix_topology commands",
            "xor": ["expert"],
        },
    ),
    (
        "mris_make_surfaces",
        str,
        {
            "help_string": "Flags to pass to mris_make_surfaces commands",
            "xor": ["expert"],
        },
    ),
    (
        "mris_surf2vol",
        str,
        {"help_string": "Flags to pass to mris_surf2vol commands", "xor": ["expert"]},
    ),
    (
        "mris_register",
        str,
        {"help_string": "Flags to pass to mris_register commands", "xor": ["expert"]},
    ),
    (
        "mrisp_paint",
        str,
        {"help_string": "Flags to pass to mrisp_paint commands", "xor": ["expert"]},
    ),
    (
        "mris_ca_label",
        str,
        {"help_string": "Flags to pass to mris_ca_label commands", "xor": ["expert"]},
    ),
    (
        "mris_anatomical_stats",
        str,
        {
            "help_string": "Flags to pass to mris_anatomical_stats commands",
            "xor": ["expert"],
        },
    ),
    (
        "mri_aparc2aseg",
        str,
        {"help_string": "Flags to pass to mri_aparc2aseg commands", "xor": ["expert"]},
    ),
]
ReconAll_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ReconAll_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ReconAll(ShellCommandTask):
    """
    Example
    -------
    >>> task = ReconAll()
    >>> task.inputs.T1_files = "test.nii.gz"
    >>> task.inputs.subjects_dir = "."
    >>> task.inputs.subject_id = "foo"
    >>> task.cmdline
    'recon-all -all -i structural.nii -qcache -subjid foo -sd .'
    """

    input_spec = ReconAll_input_spec
    output_spec = ReconAll_output_spec
    executable = "recon-all"
