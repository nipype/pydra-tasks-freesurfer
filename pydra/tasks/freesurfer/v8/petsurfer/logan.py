import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import split_filename
import os
from pydra.compose import shell
from pydra.utils.typing import MultiOutputType
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""
    self_dict = {}

    if name == "surf":
        _si = self_dict["inputs"]
        return argstr % (_si.subject_id, _si.hemi, _si.surf_geo)

    return argstr.format(**inputs)


def surf_formatter(field, inputs):
    return _format_arg(
        "surf", field, inputs, argstr="--surf {surf:d} {surf:d} {surf:d}"
    )


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}

    if inputs["glm_dir"] is attrs.NOTHING:
        glmdir = os.getcwd()
    else:
        glmdir = os.path.abspath(inputs["glm_dir"])
    outputs["glm_dir"] = glmdir

    if inputs["nii_gz"] is not attrs.NOTHING:
        ext = "nii.gz"
    elif inputs["nii"] is not attrs.NOTHING:
        ext = "nii"
    else:
        ext = "mgh"

    outputs["beta_file"] = os.path.join(glmdir, f"beta.{ext}")
    outputs["error_var_file"] = os.path.join(glmdir, f"rvar.{ext}")
    outputs["error_stddev_file"] = os.path.join(glmdir, f"rstd.{ext}")
    outputs["mask_file"] = os.path.join(glmdir, f"mask.{ext}")
    outputs["fwhm_file"] = os.path.join(glmdir, "fwhm.dat")
    outputs["dof_file"] = os.path.join(glmdir, "dof.dat")

    if inputs["save_residual"]:
        outputs["error_file"] = os.path.join(glmdir, f"eres.{ext}")
    if inputs["save_estimate"]:
        outputs["estimate_file"] = os.path.join(glmdir, f"yhat.{ext}")
    if any((inputs["mrtm1"], inputs["mrtm2"], inputs["logan"])):
        outputs["bp_file"] = os.path.join(glmdir, f"bp.{ext}")
    if inputs["mrtm1"]:
        outputs["k2p_file"] = os.path.join(glmdir, "k2prime.dat")

    contrasts = []
    if inputs["contrast"] is not attrs.NOTHING:
        for c in inputs["contrast"]:
            if split_filename(c)[2] in [".mat", ".dat", ".mtx", ".con"]:
                contrasts.append(split_filename(c)[1])
            else:
                contrasts.append(os.path.split(c)[1])
    elif (inputs["one_sample"] is not attrs.NOTHING) and inputs["one_sample"]:
        contrasts = ["osgm"]

    outputs["sig_file"] = [os.path.join(glmdir, c, f"sig.{ext}") for c in contrasts]
    outputs["ftest_file"] = [os.path.join(glmdir, c, f"F.{ext}") for c in contrasts]
    outputs["gamma_file"] = [os.path.join(glmdir, c, f"gamma.{ext}") for c in contrasts]
    outputs["gamma_var_file"] = [
        os.path.join(glmdir, c, f"gammavar.{ext}") for c in contrasts
    ]

    if (inputs["pca"] is not attrs.NOTHING) and inputs["pca"]:
        pcadir = os.path.join(glmdir, "pca-eres")
        outputs["spatial_eigenvectors"] = os.path.join(pcadir, f"v.{ext}")
        outputs["frame_eigenvectors"] = os.path.join(pcadir, "u.mtx")
        outputs["singluar_values"] = os.path.join(pcadir, "sdiag.mat")
        outputs["svd_stats_file"] = os.path.join(pcadir, "stats.dat")

    return outputs


def beta_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("beta_file")


def error_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("error_file")


def error_var_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("error_var_file")


def error_stddev_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("error_stddev_file")


def estimate_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("estimate_file")


def mask_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mask_file")


def fwhm_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fwhm_file")


def dof_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("dof_file")


def gamma_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("gamma_file")


def gamma_var_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("gamma_var_file")


def sig_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("sig_file")


def ftest_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("ftest_file")


def spatial_eigenvectors_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("spatial_eigenvectors")


def frame_eigenvectors_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("frame_eigenvectors")


def singular_values_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("singular_values")


def svd_stats_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("svd_stats_file")


def k2p_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("k2p_file")


def bp_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("bp_file")


def _gen_filename(name, inputs):
    if name == "glm_dir":
        return os.getcwd()
    return None


def glm_dir_default(inputs):
    return _gen_filename("glm_dir", inputs=inputs)


@shell.define(
    xor=[
        ["contrast", "design", "fsgd", "one_sample"],
        ["cortex", "label_file"],
        ["design", "fsgd", "one_sample"],
        ["fixed_fx_dof", "fixed_fx_dof_file"],
        ["nii", "nii_gz"],
        ["no_prune", "prune_thresh"],
        ["weight_file", "weight_inv", "weight_sqrt", "weighted_ls"],
        ["weight_file", "weighted_ls"],
        ["weight_inv", "weighted_ls"],
        ["weight_sqrt", "weighted_ls"],
    ]
)
class Logan(shell.Task["Logan.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.freesurfer.v8.petsurfer.logan import Logan
    >>> from pydra.utils.typing import MultiOutputType

    >>> task = Logan()
    >>> task.glm_dir = "logan"
    >>> task.in_file = Nifti1.mock("tac.nii")
    >>> task.design = File.mock()
    >>> task.weighted_ls = File.mock()
    >>> task.fixed_fx_var = File.mock()
    >>> task.fixed_fx_dof_file = File.mock()
    >>> task.weight_file = File.mock()
    >>> task.mask_file = File.mock()
    >>> task.label_file = File.mock()
    >>> task.sim_done_file = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_glmfit"
    logan: ty.Any = shell.arg(
        help="RefTac TimeSec tstar   : perform Logan kinetic modeling",
        argstr="--logan {logan[0]} {logan[1]} {logan[2]}",
    )
    in_file: Nifti1 = shell.arg(help="input 4D file", argstr="--y {in_file}")
    fsgd: ty.Any | None = shell.arg(
        help="freesurfer descriptor file", argstr="--fsgd {fsgd[0]} {fsgd[1]}"
    )
    design: File | None = shell.arg(help="design matrix file", argstr="--X {design}")
    contrast: list[File] = shell.arg(help="contrast file", argstr="--C {contrast}...")
    one_sample: bool = shell.arg(
        help="construct X and C as a one-sample group mean", argstr="--osgm"
    )
    no_contrast_ok: bool = shell.arg(
        help="do not fail if no contrasts specified", argstr="--no-contrasts-ok"
    )
    per_voxel_reg: list[File] = shell.arg(
        help="per-voxel regressors", argstr="--pvr {per_voxel_reg}..."
    )
    self_reg: ty.Any = shell.arg(
        help="self-regressor from index col row slice",
        argstr="--selfreg {self_reg[0]} {self_reg[1]} {self_reg[2]}",
    )
    weighted_ls: File | None = shell.arg(
        help="weighted least squares", argstr="--wls {weighted_ls}"
    )
    fixed_fx_var: File = shell.arg(
        help="for fixed effects analysis", argstr="--yffxvar {fixed_fx_var}"
    )
    fixed_fx_dof: int | None = shell.arg(
        help="dof for fixed effects analysis", argstr="--ffxdof {fixed_fx_dof}"
    )
    fixed_fx_dof_file: File | None = shell.arg(
        help="text file with dof for fixed effects analysis",
        argstr="--ffxdofdat {fixed_fx_dof_file}",
    )
    weight_file: File | None = shell.arg(help="weight for each input at each voxel")
    weight_inv: bool = shell.arg(help="invert weights", argstr="--w-inv")
    weight_sqrt: bool = shell.arg(help="sqrt of weights", argstr="--w-sqrt")
    fwhm: ty.Any = shell.arg(help="smooth input by fwhm", argstr="--fwhm {fwhm}")
    var_fwhm: ty.Any = shell.arg(
        help="smooth variance by fwhm", argstr="--var-fwhm {var_fwhm}"
    )
    no_mask_smooth: bool = shell.arg(
        help="do not mask when smoothing", argstr="--no-mask-smooth"
    )
    no_est_fwhm: bool = shell.arg(
        help="turn off FWHM output estimation", argstr="--no-est-fwhm"
    )
    mask_file: File = shell.arg(help="binary mask", argstr="--mask {mask_file}")
    label_file: File | None = shell.arg(
        help="use label as mask, surfaces only", argstr="--label {label_file}"
    )
    cortex: bool = shell.arg(
        help="use subjects ?h.cortex.label as label", argstr="--cortex"
    )
    invert_mask: bool = shell.arg(help="invert mask", argstr="--mask-inv")
    prune: bool = shell.arg(
        help="remove voxels that do not have a non-zero value at each frame (def)",
        argstr="--prune",
    )
    no_prune: bool = shell.arg(help="do not prune", argstr="--no-prune")
    prune_thresh: float | None = shell.arg(
        help="prune threshold. Default is FLT_MIN", argstr="--prune_thr {prune_thresh}"
    )
    compute_log_y: bool = shell.arg(
        help="compute natural log of y prior to analysis", argstr="--logy"
    )
    save_estimate: bool = shell.arg(
        help="save signal estimate (yhat)", argstr="--yhat-save"
    )
    save_residual: bool = shell.arg(
        help="save residual error (eres)", argstr="--eres-save"
    )
    save_res_corr_mtx: bool = shell.arg(
        help="save residual error spatial correlation matrix (eres.scm). Big!",
        argstr="--eres-scm",
    )
    surf: bool = shell.arg(
        help="analysis is on a surface mesh",
        requires=["subject_id", "hemi"],
        formatter="surf_formatter",
    )
    subject_id: str = shell.arg(help="subject id for surface geometry")
    hemi: ty.Any = shell.arg(help="surface hemisphere")
    surf_geo: str = shell.arg(
        help="surface geometry name (e.g. white, pial)", default="white"
    )
    simulation: ty.Any = shell.arg(
        help="nulltype nsim thresh csdbasename",
        argstr="--sim {simulation[0]} {simulation[1]} {simulation[2]} {simulation[3]}",
    )
    sim_sign: ty.Any = shell.arg(
        help="abs, pos, or neg", argstr="--sim-sign {sim_sign}"
    )
    uniform: ty.Any = shell.arg(
        help="use uniform distribution instead of gaussian",
        argstr="--uniform {uniform[0]} {uniform[1]}",
    )
    pca: bool = shell.arg(help="perform pca/svd analysis on residual", argstr="--pca")
    calc_AR1: bool = shell.arg(
        help="compute and save temporal AR1 of residual", argstr="--tar1"
    )
    save_cond: bool = shell.arg(
        help="flag to save design matrix condition at each voxel", argstr="--save-cond"
    )
    vox_dump: ty.Any = shell.arg(
        help="dump voxel GLM and exit",
        argstr="--voxdump {vox_dump[0]} {vox_dump[1]} {vox_dump[2]}",
    )
    seed: int = shell.arg(help="used for synthesizing noise", argstr="--seed {seed}")
    synth: bool = shell.arg(help="replace input with gaussian", argstr="--synth")
    resynth_test: int = shell.arg(
        help="test GLM by resynthsis", argstr="--resynthtest {resynth_test}"
    )
    profile: int = shell.arg(help="niters : test speed", argstr="--profile {profile}")
    mrtm1: ty.Any = shell.arg(
        help="RefTac TimeSec : perform MRTM1 kinetic modeling",
        argstr="--mrtm1 {mrtm1[0]} {mrtm1[1]}",
    )
    mrtm2: ty.Any = shell.arg(
        help="RefTac TimeSec k2prime : perform MRTM2 kinetic modeling",
        argstr="--mrtm2 {mrtm2[0]} {mrtm2[1]} {mrtm2[2]}",
    )
    bp_clip_neg: bool = shell.arg(
        help="set negative BP voxels to zero", argstr="--bp-clip-neg"
    )
    bp_clip_max: float = shell.arg(
        help="set BP voxels above max to max", argstr="--bp-clip-max {bp_clip_max}"
    )
    force_perm: bool = shell.arg(
        help="force perumtation test, even when design matrix is not orthog",
        argstr="--perm-force",
    )
    diag: int = shell.arg(
        help="Gdiag_no : set diagnostic level", argstr="--diag {diag}"
    )
    diag_cluster: bool = shell.arg(
        help="save sig volume and exit from first sim loop", argstr="--diag-cluster"
    )
    debug: bool = shell.arg(help="turn on debugging", argstr="--debug")
    check_opts: bool = shell.arg(
        help="don't run anything, just check options and exit", argstr="--checkopts"
    )
    allow_repeated_subjects: bool = shell.arg(
        help="allow subject names to repeat in the fsgd file (must appear before --fsgd",
        argstr="--allowsubjrep",
    )
    allow_ill_cond: bool = shell.arg(
        help="allow ill-conditioned design matrices", argstr="--illcond"
    )
    sim_done_file: File = shell.arg(
        help="create file when simulation finished", argstr="--sim-done {sim_done_file}"
    )
    nii: bool = shell.arg(help="save outputs as nii", argstr="--nii")
    nii_gz: bool = shell.arg(help="save outputs as nii.gz", argstr="--nii.gz")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        glm_dir: str = shell.outarg(
            help="save outputs to dir",
            argstr="--glmdir {glm_dir}",
            path_template='"logan"',
        )
        beta_file: File | None = shell.out(
            help="map of regression coefficients", callable=beta_file_callable
        )
        error_file: File | None = shell.out(
            help="map of residual error", callable=error_file_callable
        )
        error_var_file: File | None = shell.out(
            help="map of residual error variance", callable=error_var_file_callable
        )
        error_stddev_file: File | None = shell.out(
            help="map of residual error standard deviation",
            callable=error_stddev_file_callable,
        )
        estimate_file: File | None = shell.out(
            help="map of the estimated Y values", callable=estimate_file_callable
        )
        mask_file: File | None = shell.out(
            help="map of the mask used in the analysis", callable=mask_file_callable
        )
        fwhm_file: File | None = shell.out(
            help="text file with estimated smoothness", callable=fwhm_file_callable
        )
        dof_file: File | None = shell.out(
            help="text file with effective degrees-of-freedom for the analysis",
            callable=dof_file_callable,
        )
        gamma_file: list | object | MultiOutputType | None = shell.out(
            help="map of contrast of regression coefficients",
            callable=gamma_file_callable,
        )
        gamma_var_file: list | object | MultiOutputType | None = shell.out(
            help="map of regression contrast variance", callable=gamma_var_file_callable
        )
        sig_file: list | object | MultiOutputType | None = shell.out(
            help="map of F-test significance (in -log10p)", callable=sig_file_callable
        )
        ftest_file: list | object | MultiOutputType | None = shell.out(
            help="map of test statistic values", callable=ftest_file_callable
        )
        spatial_eigenvectors: File | None = shell.out(
            help="map of spatial eigenvectors from residual PCA",
            callable=spatial_eigenvectors_callable,
        )
        frame_eigenvectors: File | None = shell.out(
            help="matrix of frame eigenvectors from residual PCA",
            callable=frame_eigenvectors_callable,
        )
        singular_values: File | None = shell.out(
            help="matrix singular values from residual PCA",
            callable=singular_values_callable,
        )
        svd_stats_file: File | None = shell.out(
            help="text file summarizing the residual PCA",
            callable=svd_stats_file_callable,
        )
        k2p_file: File | None = shell.out(
            help="estimate of k2p parameter", callable=k2p_file_callable
        )
        bp_file: File | None = shell.out(
            help="Binding potential estimates", callable=bp_file_callable
        )
