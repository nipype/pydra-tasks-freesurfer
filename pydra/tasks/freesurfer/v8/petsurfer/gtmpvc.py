import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import NiftiGz
from fileformats.medimage_freesurfer import Lta
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, val, inputs, argstr):
    if val is None:
        return ""

    if name == "optimization_schema":
        return (
            argstr
            % {
                "3D": 1,
                "2D": 2,
                "1D": 3,
                "3D_MB": 4,
                "2D_MB": 5,
                "1D_MB": 6,
                "MBZ": 7,
                "MB3": 8,
            }[val]
        )
    if name == "mg":
        return argstr % (val[0], " ".join(val[1]))

    return argstr.format(**inputs)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}

    if inputs["pvc_dir"] is attrs.NOTHING:
        pvcdir = os.getcwd()
    else:
        pvcdir = os.path.abspath(inputs["pvc_dir"])
    outputs["pvc_dir"] = pvcdir

    outputs["ref_file"] = os.path.join(pvcdir, "km.ref.tac.dat")
    outputs["hb_nifti"] = os.path.join(pvcdir, "km.hb.tac.nii.gz")
    outputs["hb_dat"] = os.path.join(pvcdir, "km.hb.tac.dat")
    outputs["nopvc_file"] = os.path.join(pvcdir, "nopvc.nii.gz")
    outputs["gtm_file"] = os.path.join(pvcdir, "gtm.nii.gz")
    outputs["gtm_stats"] = os.path.join(pvcdir, "gtm.stats.dat")
    outputs["reg_pet2anat"] = os.path.join(pvcdir, "aux", "bbpet2anat.lta")
    outputs["reg_anat2pet"] = os.path.join(pvcdir, "aux", "anat2bbpet.lta")
    outputs["eres"] = os.path.join(pvcdir, "eres.nii.gz")
    outputs["tissue_fraction"] = os.path.join(pvcdir, "aux", "tissue.fraction.nii.gz")
    outputs["tissue_fraction_psf"] = os.path.join(
        pvcdir, "aux", "tissue.fraction.psf.nii.gz"
    )
    outputs["seg"] = os.path.join(pvcdir, "aux", "seg.nii.gz")
    outputs["seg_ctab"] = os.path.join(pvcdir, "aux", "seg.ctab")

    if inputs["save_input"]:
        outputs["input_file"] = os.path.join(pvcdir, "input.nii.gz")
    if inputs["save_yhat0"]:
        outputs["yhat0"] = os.path.join(pvcdir, "yhat0.nii.gz")
    if inputs["save_yhat"]:
        outputs["yhat"] = os.path.join(pvcdir, "yhat.nii.gz")
    if inputs["save_yhat_full_fov"]:
        outputs["yhat_full_fov"] = os.path.join(pvcdir, "yhat.fullfov.nii.gz")
    if inputs["save_yhat_with_noise"]:
        outputs["yhat_with_noise"] = os.path.join(pvcdir, "yhat.nii.gz")
    if inputs["mgx"]:
        outputs["mgx_ctxgm"] = os.path.join(pvcdir, "mgx.ctxgm.nii.gz")
        outputs["mgx_subctxgm"] = os.path.join(pvcdir, "mgx.subctxgm.nii.gz")
        outputs["mgx_gm"] = os.path.join(pvcdir, "mgx.gm.nii.gz")
    if inputs["rbv"]:
        outputs["rbv"] = os.path.join(pvcdir, "rbv.nii.gz")
        outputs["reg_rbvpet2anat"] = os.path.join(pvcdir, "aux", "rbv2anat.lta")
        outputs["reg_anat2rbvpet"] = os.path.join(pvcdir, "aux", "anat2rbv.lta")
    if inputs["optimization_schema"]:
        outputs["opt_params"] = os.path.join(pvcdir, "aux", "opt.params.dat")

    return outputs


def ref_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("ref_file")


def hb_nifti_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("hb_nifti")


def hb_dat_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("hb_dat")


def nopvc_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("nopvc_file")


def gtm_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("gtm_file")


def gtm_stats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("gtm_stats")


def input_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("input_file")


def reg_pet2anat_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("reg_pet2anat")


def reg_anat2pet_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("reg_anat2pet")


def reg_rbvpet2anat_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("reg_rbvpet2anat")


def reg_anat2rbvpet_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("reg_anat2rbvpet")


def mgx_ctxgm_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mgx_ctxgm")


def mgx_subctxgm_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mgx_subctxgm")


def mgx_gm_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mgx_gm")


def rbv_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("rbv")


def opt_params_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("opt_params")


def yhat0_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("yhat0")


def yhat_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("yhat")


def yhat_full_fov_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("yhat_full_fov")


def yhat_with_noise_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("yhat_with_noise")


def eres_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("eres")


def tissue_fraction_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("tissue_fraction")


def tissue_fraction_psf_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("tissue_fraction_psf")


def seg_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("seg")


def seg_ctab_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("seg_ctab")


@shell.define(
    xor=[
        ["color_table_file", "default_color_table"],
        ["reg_file", "reg_identity", "regheader"],
        ["save_yhat", "save_yhat_with_noise"],
    ]
)
class GTMPVC(shell.Task["GTMPVC.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import NiftiGz
    >>> from fileformats.medimage_freesurfer import Lta
    >>> from pydra.tasks.freesurfer.v8.petsurfer.gtmpvc import GTMPVC

    >>> task = GTMPVC()
    >>> task.in_file = NiftiGz.mock("sub-01_ses-baseline_pet.nii.gz")
    >>> task.psf = 4
    >>> task.segmentation = File.mock()
    >>> task.reg_file = Lta.mock("sub-01_ses-baseline_pet_mean_reg.lta")
    >>> task.mask_file = File.mock()
    >>> task.auto_mask = (1, 0.1)
    >>> task.color_table_file = File.mock()
    >>> task.km_hb = ["11 12 50 51"]
    >>> task.save_input = True
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    >>> task = GTMPVC()
    >>> task.in_file = NiftiGz.mock("sub-01_ses-baseline_pet.nii.gz")
    >>> task.segmentation = File.mock()
    >>> task.reg_file = Lta.mock()
    >>> task.regheader = True
    >>> task.mask_file = File.mock()
    >>> task.color_table_file = File.mock()
    >>> task.mg = (0.5, ["ROI1", "ROI2"])
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_gtmpvc --i sub-01_ses-baseline_pet.nii.gz --mg 0.5 ROI1 ROI2 --o pvc --regheader --seg gtmseg.mgz'


    """

    executable = "mri_gtmpvc"
    in_file: NiftiGz = shell.arg(
        help="input volume - source data to pvc", argstr="--i {in_file}"
    )
    frame: int = shell.arg(
        help="only process 0-based frame F from inputvol", argstr="--frame {frame}"
    )
    psf: float = shell.arg(help="scanner PSF FWHM in mm", argstr="--psf {psf}")
    segmentation: File = shell.arg(
        help="segfile : anatomical segmentation to define regions for GTM",
        argstr="--seg {segmentation}",
    )
    reg_file: Lta | None = shell.arg(
        help="LTA registration file that maps PET to anatomical",
        argstr="--reg {reg_file}",
    )
    regheader: bool = shell.arg(
        help="assume input and seg share scanner space", argstr="--regheader"
    )
    reg_identity: bool = shell.arg(
        help="assume that input is in anatomical space", argstr="--reg-identity"
    )
    mask_file: File = shell.arg(
        help="ignore areas outside of the mask (in input vol space)",
        argstr="--mask {mask_file}",
    )
    auto_mask: ty.Any = shell.arg(
        help="FWHM thresh : automatically compute mask",
        argstr="--auto-mask {auto_mask[0]} {auto_mask[1]}",
    )
    no_reduce_fov: bool = shell.arg(
        help="do not reduce FoV to encompass mask", argstr="--no-reduce-fov"
    )
    reduce_fox_eqodd: bool = shell.arg(
        help="reduce FoV to encompass mask but force nc=nr and ns to be odd",
        argstr="--reduce-fox-eqodd",
    )
    contrast: list[File] = shell.arg(help="contrast file", argstr="--C {contrast}...")
    default_seg_merge: bool = shell.arg(
        help="default schema for merging ROIs", argstr="--default-seg-merge"
    )
    merge_hypos: bool = shell.arg(
        help="merge left and right hypointensites into to ROI", argstr="--merge-hypos"
    )
    merge_cblum_wm_gyri: bool = shell.arg(
        help="cerebellum WM gyri back into cerebellum WM",
        argstr="--merge-cblum-wm-gyri",
    )
    tt_reduce: bool = shell.arg(
        help="reduce segmentation to that of a tissue type", argstr="--tt-reduce"
    )
    replace: ty.Any = shell.arg(
        help="Id1 Id2 : replace seg Id1 with seg Id2",
        argstr="--replace {replace[0]} {replace[1]}",
    )
    rescale: list[ty.Any] = shell.arg(
        help="Id1 <Id2...>  : specify reference region(s) used to rescale (default is pons)",
        argstr="--rescale {rescale}...",
    )
    no_rescale: bool = shell.arg(
        help="do not global rescale such that mean of reference region is scaleref",
        argstr="--no-rescale",
    )
    scale_refval: float = shell.arg(
        help="refval : scale such that mean in reference region is refval",
        argstr="--scale-refval {scale_refval}",
    )
    color_table_file: File | None = shell.arg(
        help="color table file with seg id names", argstr="--ctab {color_table_file}"
    )
    default_color_table: bool = shell.arg(
        help="use $FREESURFER_HOME/FreeSurferColorLUT.txt", argstr="--ctab-default"
    )
    tt_update: bool = shell.arg(
        help="changes tissue type of VentralDC, BrainStem, and Pons to be SubcortGM",
        argstr="--tt-update",
    )
    lat: bool = shell.arg(help="lateralize tissue types", argstr="--lat")
    no_tfe: bool = shell.arg(
        help="do not correct for tissue fraction effect (with --psf 0 turns off PVC entirely)",
        argstr="--no-tfe",
    )
    no_pvc: bool = shell.arg(
        help="turns off PVC entirely (both PSF and TFE)", argstr="--no-pvc"
    )
    tissue_fraction_resolution: float = shell.arg(
        help="set the tissue fraction resolution parameter (def is 0.5)",
        argstr="--segpvfres {tissue_fraction_resolution}",
    )
    rbv: bool = shell.arg(
        help="perform Region-based Voxelwise (RBV) PVC",
        argstr="--rbv",
        requires=["subjects_dir"],
    )
    rbv_res: float = shell.arg(
        help="voxsize : set RBV voxel resolution (good for when standard res takes too much memory)",
        argstr="--rbv-res {rbv_res}",
    )
    mg: ty.Any = shell.arg(
        help="gmthresh RefId1 RefId2 ...: perform Mueller-Gaertner PVC, gmthresh is min gm pvf bet 0 and 1",
        argstr="--mg {mg[0]} {mg[1]}",
    )
    mg_ref_cerebral_wm: bool = shell.arg(
        help=" set MG RefIds to 2 and 41", argstr="--mg-ref-cerebral-wm"
    )
    mg_ref_lobes_wm: bool = shell.arg(
        help="set MG RefIds to those for lobes when using wm subseg",
        argstr="--mg-ref-lobes-wm",
    )
    mgx: float = shell.arg(
        help="gmxthresh : GLM-based Mueller-Gaertner PVC, gmxthresh is min gm pvf bet 0 and 1",
        argstr="--mgx {mgx}",
    )
    km_ref: list[ty.Any] = shell.arg(
        help="RefId1 RefId2 ... : compute reference TAC for KM as mean of given RefIds",
        argstr="--km-ref {km_ref}...",
    )
    km_hb: list[ty.Any] = shell.arg(
        help="RefId1 RefId2 ... : compute HiBinding TAC for KM as mean of given RefIds",
        argstr="--km-hb {km_hb}...",
    )
    steady_state_params: ty.Any = shell.arg(
        help="bpc scale dcf : steady-state analysis spec blood plasma concentration, unit scale and decay correction factor. You must also spec --km-ref. Turns off rescaling",
        argstr="--ss {steady_state_params[0]} {steady_state_params[1]} {steady_state_params[2]}",
    )
    X: bool = shell.arg(
        help="save X matrix in matlab4 format as X.mat (it will be big)", argstr="--X"
    )
    y: bool = shell.arg(help="save y matrix in matlab4 format as y.mat", argstr="--y")
    beta: bool = shell.arg(
        help="save beta matrix in matlab4 format as beta.mat", argstr="--beta"
    )
    X0: bool = shell.arg(
        help="save X0 matrix in matlab4 format as X0.mat (it will be big)",
        argstr="--X0",
    )
    save_input: bool = shell.arg(
        help="saves rescaled input as input.rescaled.nii.gz", argstr="--save-input"
    )
    save_eres: bool = shell.arg(help="saves residual error", argstr="--save-eres")
    save_yhat: bool = shell.arg(
        help="save signal estimate (yhat) smoothed with the PSF", argstr="--save-yhat"
    )
    save_yhat_with_noise: ty.Any | None = shell.arg(
        help="seed nreps : save signal estimate (yhat) with noise",
        argstr="--save-yhat-with-noise {save_yhat_with_noise[0]} {save_yhat_with_noise[1]}",
    )
    save_yhat_full_fov: bool = shell.arg(
        help="save signal estimate (yhat)", argstr="--save-yhat-full-fov"
    )
    save_yhat0: bool = shell.arg(
        help="save signal estimate (yhat)", argstr="--save-yhat0"
    )
    optimization_schema: ty.Any = shell.arg(
        help="opt : optimization schema for applying adaptive GTM",
        argstr="--opt {optimization_schema}",
    )
    opt_tol: ty.Any = shell.arg(
        help="n_iters_max ftol lin_min_tol : optimization parameters for adaptive gtm using fminsearch",
        argstr="--opt-tol {opt_tol[0]} {opt_tol[1]} {opt_tol[2]}",
    )
    opt_brain: bool = shell.arg(help="apply adaptive GTM", argstr="--opt-brain")
    opt_seg_merge: bool = shell.arg(
        help="optimal schema for merging ROIs when applying adaptive GTM",
        argstr="--opt-seg-merge",
    )
    num_threads: int = shell.arg(
        help="threads : number of threads to use", argstr="--threads {num_threads}"
    )
    psf_col: float = shell.arg(
        help="xFWHM : full-width-half-maximum in the x-direction",
        argstr="--psf-col {psf_col}",
    )
    psf_row: float = shell.arg(
        help="yFWHM : full-width-half-maximum in the y-direction",
        argstr="--psf-row {psf_row}",
    )
    psf_slice: float = shell.arg(
        help="zFWHM : full-width-half-maximum in the z-direction",
        argstr="--psf-slice {psf_slice}",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        pvc_dir: str = shell.outarg(
            help="save outputs to dir", argstr="--o {pvc_dir}", path_template="pvc_dir"
        )
        ref_file: File | None = shell.out(
            help="Reference TAC in .dat", callable=ref_file_callable
        )
        hb_nifti: File | None = shell.out(
            help="High-binding TAC in nifti", callable=hb_nifti_callable
        )
        hb_dat: File | None = shell.out(
            help="High-binding TAC in .dat", callable=hb_dat_callable
        )
        nopvc_file: File | None = shell.out(
            help="TACs for all regions with no PVC", callable=nopvc_file_callable
        )
        gtm_file: File | None = shell.out(
            help="TACs for all regions with GTM PVC", callable=gtm_file_callable
        )
        gtm_stats: File | None = shell.out(
            help="Statistics for the GTM PVC", callable=gtm_stats_callable
        )
        input_file: File | None = shell.out(
            help="4D PET file in native volume space", callable=input_file_callable
        )
        reg_pet2anat: File | None = shell.out(
            help="Registration file to go from PET to anat",
            callable=reg_pet2anat_callable,
        )
        reg_anat2pet: File | None = shell.out(
            help="Registration file to go from anat to PET",
            callable=reg_anat2pet_callable,
        )
        reg_rbvpet2anat: File | None = shell.out(
            help="Registration file to go from RBV corrected PET to anat",
            callable=reg_rbvpet2anat_callable,
        )
        reg_anat2rbvpet: File | None = shell.out(
            help="Registration file to go from anat to RBV corrected PET",
            callable=reg_anat2rbvpet_callable,
        )
        mgx_ctxgm: File | None = shell.out(
            help="Cortical GM voxel-wise values corrected using the extended Muller-Gartner method",
            callable=mgx_ctxgm_callable,
        )
        mgx_subctxgm: File | None = shell.out(
            help="Subcortical GM voxel-wise values corrected using the extended Muller-Gartner method",
            callable=mgx_subctxgm_callable,
        )
        mgx_gm: File | None = shell.out(
            help="All GM voxel-wise values corrected using the extended Muller-Gartner method",
            callable=mgx_gm_callable,
        )
        rbv: File | None = shell.out(
            help="All GM voxel-wise values corrected using the RBV method",
            callable=rbv_callable,
        )
        opt_params: File | None = shell.out(
            help="Optimal parameter estimates for the FWHM using adaptive GTM",
            callable=opt_params_callable,
        )
        yhat0: File | None = shell.out(
            help="4D PET file of signal estimate (yhat) after PVC (unsmoothed)",
            callable=yhat0_callable,
        )
        yhat: File | None = shell.out(
            help="4D PET file of signal estimate (yhat) after PVC (smoothed with PSF)",
            callable=yhat_callable,
        )
        yhat_full_fov: File | None = shell.out(
            help="4D PET file with full FOV of signal estimate (yhat) after PVC (smoothed with PSF)",
            callable=yhat_full_fov_callable,
        )
        yhat_with_noise: File | None = shell.out(
            help="4D PET file with full FOV of signal estimate (yhat) with noise after PVC (smoothed with PSF)",
            callable=yhat_with_noise_callable,
        )
        eres: File | None = shell.out(
            help="4D PET file of residual error after PVC (smoothed with PSF)",
            callable=eres_callable,
        )
        tissue_fraction: File | None = shell.out(
            help="4D PET file of tissue fraction before PVC",
            callable=tissue_fraction_callable,
        )
        tissue_fraction_psf: File | None = shell.out(
            help="4D PET file of tissue fraction after PVC (smoothed with PSF)",
            callable=tissue_fraction_psf_callable,
        )
        seg: File | None = shell.out(
            help="Segmentation file of regions used for PVC", callable=seg_callable
        )
        seg_ctab: File | None = shell.out(
            help="Color table file for segmentation file", callable=seg_ctab_callable
        )
