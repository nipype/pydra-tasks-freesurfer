import attrs
from fileformats.generic import File
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.interfaces.io import FreeSurferSource
import os
from pydra.compose import shell
from pydra.utils.typing import MultiInputObj
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "T1_files":
        if _is_resuming(
            base_template_id=inputs["base_template_id"],
            longitudinal_template_id=inputs["longitudinal_template_id"],
            longitudinal_timepoint_id=inputs["longitudinal_timepoint_id"],
            subject_id=inputs["subject_id"],
            subjects_dir=inputs["subjects_dir"],
        ):
            return None
    if name == "hippocampal_subfields_T1" and (
        inputs["hippocampal_subfields_T2"] is not attrs.NOTHING
    ):
        return None
    if all(
        (
            name == "hippocampal_subfields_T2",
            (inputs["hippocampal_subfields_T1"] is not attrs.NOTHING)
            and inputs["hippocampal_subfields_T1"],
        )
    ):
        argstr = argstr.replace("T2", "T1T2")
        return argstr % value
    if name == "directive" and value == "autorecon-hemi":
        if inputs["hemi"] is attrs.NOTHING:
            raise ValueError("Directive 'autorecon-hemi' requires hemi input to be set")
        value += " " + inputs["hemi"]
    if all(
        (
            name == "hemi",
            (inputs["directive"] is not attrs.NOTHING)
            and inputs["directive"] == "autorecon-hemi",
        )
    ):
        return None

    return argstr.format(**inputs)


def T1_files_formatter(field, inputs):
    return _format_arg("T1_files", field, inputs, argstr="-i {T1_files}...")


def hippocampal_subfields_T1_formatter(field, inputs):
    return _format_arg(
        "hippocampal_subfields_T1", field, inputs, argstr="-hippocampal-subfields-T1"
    )


def hippocampal_subfields_T2_formatter(field, inputs):
    return _format_arg(
        "hippocampal_subfields_T2",
        field,
        inputs,
        argstr="-hippocampal-subfields-T2 {hippocampal_subfields_T2[0]} {hippocampal_subfields_T2[1]}",
    )


def directive_formatter(field, inputs):
    return _format_arg("directive", field, inputs, argstr="-{directive}")


def hemi_formatter(field, inputs):
    return _format_arg("hemi", field, inputs, argstr="-hemi {hemi}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    if inputs["subjects_dir"] is not attrs.NOTHING:
        subjects_dir = inputs["subjects_dir"]
    else:
        subjects_dir = _gen_subjects_dir(
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )

    if inputs["hemi"] is not attrs.NOTHING:
        hemi = inputs["hemi"]
    else:
        hemi = "both"

    outputs = {}

    if inputs["base_template_id"] is not attrs.NOTHING:
        outputs["update"](
            FreeSurferSource(
                subject_id=inputs["base_template_id"],
                subjects_dir=subjects_dir,
                hemi=hemi,
            )._list_outputs()
        )
        outputs["subject_id"] = inputs["base_template_id"]
    elif inputs["longitudinal_timepoint_id"] is not attrs.NOTHING:
        subject_id = f"{inputs['longitudinal_timepoint_id']}.long.{inputs['longitudinal_template_id']}"
        outputs["update"](
            FreeSurferSource(
                subject_id=subject_id, subjects_dir=subjects_dir, hemi=hemi
            )._list_outputs()
        )
        outputs["subject_id"] = subject_id
    else:
        outputs["update"](
            FreeSurferSource(
                subject_id=inputs["subject_id"],
                subjects_dir=subjects_dir,
                hemi=hemi,
            )._list_outputs()
        )
        outputs["subject_id"] = inputs["subject_id"]

    outputs["subjects_dir"] = subjects_dir
    return outputs


def subject_id_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("subject_id")


def T1_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("T1")


def aseg_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("aseg")


def brain_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("brain")


def brainmask_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("brainmask")


def filled_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("filled")


def norm_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("norm")


def nu_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("nu")


def orig_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("orig")


def rawavg_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("rawavg")


def ribbon_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("ribbon")


def wm_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("wm")


def wmparc_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("wmparc")


def curv_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("curv")


def avg_curv_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("avg_curv")


def inflated_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("inflated")


def pial_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("pial")


def area_pial_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("area_pial")


def curv_pial_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("curv_pial")


def smoothwm_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("smoothwm")


def sphere_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("sphere")


def sulc_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("sulc")


def thickness_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("thickness")


def volume_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("volume")


def white_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("white")


def jacobian_white_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("jacobian_white")


def graymid_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("graymid")


def label_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("label")


def annot_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("annot")


def aparc_aseg_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("aparc_aseg")


def sphere_reg_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("sphere_reg")


def aseg_stats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("aseg_stats")


def wmparc_stats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("wmparc_stats")


def aparc_stats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("aparc_stats")


def BA_stats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("BA_stats")


def aparc_a2009s_stats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("aparc_a2009s_stats")


def curv_stats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("curv_stats")


def entorhinal_exvivo_stats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("entorhinal_exvivo_stats")


def _gen_filename(name, inputs):
    if name == "subjects_dir":
        return _gen_subjects_dir()
    return None


def subjects_dir_default(inputs):
    return _gen_filename("subjects_dir", inputs=inputs)


@shell.define(
    xor=[
        ["base_template_id", "longitudinal_timepoint_id", "subject_id"],
        ["expert", "mri_aparc2aseg"],
        ["expert", "mri_ca_label"],
        ["expert", "mri_ca_normalize"],
        ["expert", "mri_ca_register"],
        ["expert", "mri_edit_wm_with_aseg"],
        ["expert", "mri_em_register"],
        ["expert", "mri_fill"],
        ["expert", "mri_mask"],
        ["expert", "mri_normalize"],
        ["expert", "mri_pretess"],
        ["expert", "mri_remove_neck"],
        ["expert", "mri_segment"],
        ["expert", "mri_segstats"],
        ["expert", "mri_tessellate"],
        ["expert", "mri_watershed"],
        ["expert", "mris_anatomical_stats"],
        ["expert", "mris_ca_label"],
        ["expert", "mris_fix_topology"],
        ["expert", "mris_inflate"],
        ["expert", "mris_make_surfaces"],
        ["expert", "mris_register"],
        ["expert", "mris_smooth"],
        ["expert", "mris_sphere"],
        ["expert", "mris_surf2vol"],
        ["expert", "mrisp_paint"],
        ["expert", "talairach"],
        ["use_FLAIR", "use_T2"],
    ]
)
class ReconAll(shell.Task["ReconAll.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.freesurfer.v8.preprocess.recon_all import ReconAll
    >>> from pydra.utils.typing import MultiInputObj

    >>> task = ReconAll()
    >>> task.subject_id = "foo"
    >>> task.T2_file = File.mock()
    >>> task.FLAIR_file = File.mock()
    >>> task.expert = File.mock()
    >>> task.subjects_dir = "."
    >>> task.flags = ["-cw256", "-qcache"]
    >>> task.cmdline
    'recon-all -all -i structural.nii -cw256 -qcache -subjid foo -sd .'


    >>> task = ReconAll()
    >>> task.T2_file = File.mock()
    >>> task.FLAIR_file = File.mock()
    >>> task.expert = File.mock()
    >>> task.flags = []
    >>> task.cmdline
    'recon-all -all -i structural.nii -hemi lh -subjid foo -sd .'


    >>> task = ReconAll()
    >>> task.directive = "autorecon-hemi"
    >>> task.T2_file = File.mock()
    >>> task.FLAIR_file = File.mock()
    >>> task.expert = File.mock()
    >>> task.cmdline
    'recon-all -autorecon-hemi lh -i structural.nii -subjid foo -sd .'


    >>> task = ReconAll()
    >>> task.subject_id = "foo"
    >>> task.T2_file = File.mock()
    >>> task.FLAIR_file = File.mock()
    >>> task.hippocampal_subfields_T1 = False
    >>> task.hippocampal_subfields_T2 = ( "structural.nii", "test")
    >>> task.expert = File.mock()
    >>> task.subjects_dir = "."
    >>> task.cmdline
    'recon-all -all -i structural.nii -hippocampal-subfields-T2 structural.nii test -subjid foo -sd .'


    >>> task = ReconAll()
    >>> task.directive = "all"
    >>> task.T2_file = File.mock()
    >>> task.FLAIR_file = File.mock()
    >>> task.expert = File.mock()
    >>> task.base_template_id = "sub-template"
    >>> task.cmdline
    'None'


    >>> task = ReconAll()
    >>> task.directive = "all"
    >>> task.T2_file = File.mock()
    >>> task.FLAIR_file = File.mock()
    >>> task.expert = File.mock()
    >>> task.longitudinal_timepoint_id = "ses-1"
    >>> task.cmdline
    'None'


    """

    executable = "recon-all"
    subject_id: str = shell.arg(help="subject name", argstr="-subjid {subject_id}")
    directive: ty.Any = shell.arg(
        help="process directive",
        formatter="directive_formatter",
        position=1,
        default="all",
    )
    hemi: ty.Any = shell.arg(
        help="hemisphere to process",
        requires=["subject_id"],
        formatter="hemi_formatter",
    )
    T1_files: list[File] = shell.arg(
        help="name of T1 file to process",
        requires=["subject_id"],
        formatter="T1_files_formatter",
    )
    T2_file: File | None = shell.arg(
        help="Convert T2 image to orig directory",
        argstr="-T2 {T2_file}",
        requires=["subject_id"],
    )
    FLAIR_file: File | None = shell.arg(
        help="Convert FLAIR image to orig directory",
        argstr="-FLAIR {FLAIR_file}",
        requires=["subject_id"],
    )
    use_T2: bool = shell.arg(
        help="Use T2 image to refine the pial surface", argstr="-T2pial"
    )
    use_FLAIR: bool = shell.arg(
        help="Use FLAIR image to refine the pial surface", argstr="-FLAIRpial"
    )
    openmp: int = shell.arg(
        help="Number of processors to use in parallel", argstr="-openmp {openmp}"
    )
    parallel: bool = shell.arg(help="Enable parallel execution", argstr="-parallel")
    hires: bool = shell.arg(
        help="Conform to minimum voxel size (for voxels < 1mm)", argstr="-hires"
    )
    mprage: bool = shell.arg(
        help="Assume scan parameters are MGH MP-RAGE protocol, which produces darker gray matter",
        argstr="-mprage",
        requires=["subject_id"],
    )
    big_ventricles: bool = shell.arg(
        help="For use in subjects with enlarged ventricles", argstr="-bigventricles"
    )
    brainstem: bool = shell.arg(
        help="Segment brainstem structures",
        argstr="-brainstem-structures",
        requires=["subject_id"],
    )
    hippocampal_subfields_T1: bool = shell.arg(
        help="segment hippocampal subfields using input T1 scan",
        requires=["subject_id"],
        formatter="hippocampal_subfields_T1_formatter",
    )
    hippocampal_subfields_T2: ty.Any = shell.arg(
        help="segment hippocampal subfields using T2 scan, identified by ID (may be combined with hippocampal_subfields_T1)",
        requires=["subject_id"],
        formatter="hippocampal_subfields_T2_formatter",
    )
    expert: File | None = shell.arg(
        help="Set parameters using expert file", argstr="-expert {expert}"
    )
    xopts: ty.Any = shell.arg(
        help="Use, delete or overwrite existing expert options file",
        argstr="-xopts-{xopts}",
    )
    flags: MultiInputObj = shell.arg(help="additional parameters", argstr="{flags}")
    base_template_id: str = shell.arg(
        help="base template id",
        argstr="-base {base_template_id}",
        requires=["base_timepoint_ids"],
    )
    base_timepoint_ids: MultiInputObj = shell.arg(
        help="processed timepoint to use in template",
        argstr="-base-tp {base_timepoint_ids}...",
    )
    longitudinal_timepoint_id: str = shell.arg(
        help="longitudinal session/timepoint id",
        argstr="-long {longitudinal_timepoint_id}",
        requires=["longitudinal_template_id"],
        position=2,
    )
    longitudinal_template_id: str = shell.arg(
        help="longitudinal base template id",
        argstr="{longitudinal_template_id}",
        position=3,
    )
    talairach: str = shell.arg(help="Flags to pass to talairach commands")
    mri_normalize: str = shell.arg(help="Flags to pass to mri_normalize commands")
    mri_watershed: str = shell.arg(help="Flags to pass to mri_watershed commands")
    mri_em_register: str = shell.arg(help="Flags to pass to mri_em_register commands")
    mri_ca_normalize: str = shell.arg(help="Flags to pass to mri_ca_normalize commands")
    mri_ca_register: str = shell.arg(help="Flags to pass to mri_ca_register commands")
    mri_remove_neck: str = shell.arg(help="Flags to pass to mri_remove_neck commands")
    mri_ca_label: str = shell.arg(help="Flags to pass to mri_ca_label commands")
    mri_segstats: str = shell.arg(help="Flags to pass to mri_segstats commands")
    mri_mask: str = shell.arg(help="Flags to pass to mri_mask commands")
    mri_segment: str = shell.arg(help="Flags to pass to mri_segment commands")
    mri_edit_wm_with_aseg: str = shell.arg(
        help="Flags to pass to mri_edit_wm_with_aseg commands"
    )
    mri_pretess: str = shell.arg(help="Flags to pass to mri_pretess commands")
    mri_fill: str = shell.arg(help="Flags to pass to mri_fill commands")
    mri_tessellate: str = shell.arg(help="Flags to pass to mri_tessellate commands")
    mris_smooth: str = shell.arg(help="Flags to pass to mri_smooth commands")
    mris_inflate: str = shell.arg(help="Flags to pass to mri_inflate commands")
    mris_sphere: str = shell.arg(help="Flags to pass to mris_sphere commands")
    mris_fix_topology: str = shell.arg(
        help="Flags to pass to mris_fix_topology commands"
    )
    mris_make_surfaces: str = shell.arg(
        help="Flags to pass to mris_make_surfaces commands"
    )
    mris_surf2vol: str = shell.arg(help="Flags to pass to mris_surf2vol commands")
    mris_register: str = shell.arg(help="Flags to pass to mris_register commands")
    mrisp_paint: str = shell.arg(help="Flags to pass to mrisp_paint commands")
    mris_ca_label: str = shell.arg(help="Flags to pass to mris_ca_label commands")
    mris_anatomical_stats: str = shell.arg(
        help="Flags to pass to mris_anatomical_stats commands"
    )
    mri_aparc2aseg: str = shell.arg(help="Flags to pass to mri_aparc2aseg commands")

    class Outputs(shell.Outputs):
        subjects_dir: ty.Any = shell.outarg(
            help="path to subjects directory",
            argstr="-sd {subjects_dir}",
            path_template='"."',
        )
        subject_id: str | None = shell.out(
            help="Subject name for whom to retrieve data", callable=subject_id_callable
        )
        T1: File | None = shell.out(
            help="Intensity normalized whole-head volume", callable=T1_callable
        )
        aseg: File | None = shell.out(
            help="Volumetric map of regions from automatic segmentation",
            callable=aseg_callable,
        )
        brain: File | None = shell.out(
            help="Intensity normalized brain-only volume", callable=brain_callable
        )
        brainmask: File | None = shell.out(
            help="Skull-stripped (brain-only) volume", callable=brainmask_callable
        )
        filled: File | None = shell.out(
            help="Subcortical mass volume", callable=filled_callable
        )
        norm: File | None = shell.out(
            help="Normalized skull-stripped volume", callable=norm_callable
        )
        nu: File | None = shell.out(
            help="Non-uniformity corrected whole-head volume", callable=nu_callable
        )
        orig: File | None = shell.out(
            help="Base image conformed to Freesurfer space", callable=orig_callable
        )
        rawavg: File | None = shell.out(
            help="Volume formed by averaging input images", callable=rawavg_callable
        )
        ribbon: list[File] | None = shell.out(
            help="Volumetric maps of cortical ribbons", callable=ribbon_callable
        )
        wm: File | None = shell.out(
            help="Segmented white-matter volume", callable=wm_callable
        )
        wmparc: File | None = shell.out(
            help="Aparc parcellation projected into subcortical white matter",
            callable=wmparc_callable,
        )
        curv: list[File] | None = shell.out(
            help="Maps of surface curvature", callable=curv_callable
        )
        avg_curv: list[File] | None = shell.out(
            help="Average atlas curvature, sampled to subject",
            callable=avg_curv_callable,
        )
        inflated: list[File] | None = shell.out(
            help="Inflated surface meshes", callable=inflated_callable
        )
        pial: list[File] | None = shell.out(
            help="Gray matter/pia matter surface meshes", callable=pial_callable
        )
        area_pial: list[File] | None = shell.out(
            help="Mean area of triangles each vertex on the pial surface is associated with",
            callable=area_pial_callable,
        )
        curv_pial: list[File] | None = shell.out(
            help="Curvature of pial surface", callable=curv_pial_callable
        )
        smoothwm: list[File] | None = shell.out(
            help="Smoothed original surface meshes", callable=smoothwm_callable
        )
        sphere: list[File] | None = shell.out(
            help="Spherical surface meshes", callable=sphere_callable
        )
        sulc: list[File] | None = shell.out(
            help="Surface maps of sulcal depth", callable=sulc_callable
        )
        thickness: list[File] | None = shell.out(
            help="Surface maps of cortical thickness", callable=thickness_callable
        )
        volume: list[File] | None = shell.out(
            help="Surface maps of cortical volume", callable=volume_callable
        )
        white: list[File] | None = shell.out(
            help="White/gray matter surface meshes", callable=white_callable
        )
        jacobian_white: list[File] | None = shell.out(
            help="Distortion required to register to spherical atlas",
            callable=jacobian_white_callable,
        )
        graymid: list[File] | None = shell.out(
            help="Graymid/midthickness surface meshes", callable=graymid_callable
        )
        label: list[File] | None = shell.out(
            help="Volume and surface label files", callable=label_callable
        )
        annot: list[File] | None = shell.out(
            help="Surface annotation files", callable=annot_callable
        )
        aparc_aseg: list[File] | None = shell.out(
            help="Aparc parcellation projected into aseg volume",
            callable=aparc_aseg_callable,
        )
        sphere_reg: list[File] | None = shell.out(
            help="Spherical registration file", callable=sphere_reg_callable
        )
        aseg_stats: list[File] | None = shell.out(
            help="Automated segmentation statistics file", callable=aseg_stats_callable
        )
        wmparc_stats: list[File] | None = shell.out(
            help="White matter parcellation statistics file",
            callable=wmparc_stats_callable,
        )
        aparc_stats: list[File] | None = shell.out(
            help="Aparc parcellation statistics files", callable=aparc_stats_callable
        )
        BA_stats: list[File] | None = shell.out(
            help="Brodmann Area statistics files", callable=BA_stats_callable
        )
        aparc_a2009s_stats: list[File] | None = shell.out(
            help="Aparc a2009s parcellation statistics files",
            callable=aparc_a2009s_stats_callable,
        )
        curv_stats: list[File] | None = shell.out(
            help="Curvature statistics files", callable=curv_stats_callable
        )
        entorhinal_exvivo_stats: list[File] | None = shell.out(
            help="Entorhinal exvivo statistics files",
            callable=entorhinal_exvivo_stats_callable,
        )


def _gen_subjects_dir(inputs=None, output_dir=None, stderr=None, stdout=None):
    return output_dir


def _is_resuming(
    base_template_id=None,
    longitudinal_template_id=None,
    longitudinal_timepoint_id=None,
    subject_id=None,
    subjects_dir=None,
):
    subjects_dir = subjects_dir
    if subjects_dir is attrs.NOTHING:
        subjects_dir = _gen_subjects_dir()

    if subject_id is attrs.NOTHING:
        if base_template_id is not attrs.NOTHING:
            if os.path.isdir(os.path.join(subjects_dir, base_template_id, "mri")):
                return True
        elif longitudinal_template_id is not attrs.NOTHING:
            if os.path.isdir(
                os.path.join(
                    subjects_dir,
                    f"{longitudinal_timepoint_id}.long.{longitudinal_template_id}",
                    "mri",
                )
            ):
                return True
    else:
        if os.path.isdir(os.path.join(subjects_dir, subject_id, "mri")):
            return True
    return False
