import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name in ["in_type", "out_type", "template_type"]:
        if value == "niigz":
            return argstr.format(**{name: "nii"})

    return argstr.format(**inputs)


def _gen_filename(name, inputs):
    if name == "out_file":
        return _get_outfilename(
            in_file=inputs["in_file"],
            out_file=inputs["out_file"],
            out_type=inputs["out_type"],
        )
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class MRIConvert(shell.Task["MRIConvert.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.mri_convert import MRIConvert

    >>> task = MRIConvert()
    >>> task.autoalign_matrix = File.mock()
    >>> task.apply_transform = File.mock()
    >>> task.apply_inv_transform = File.mock()
    >>> task.out_type = "mgz"
    >>> task.in_file = Nifti1.mock("structural.nii")
    >>> task.reslice_like = File.mock()
    >>> task.in_like = File.mock()
    >>> task.color_file = File.mock()
    >>> task.status_file = File.mock()
    >>> task.sdcm_list = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_convert --out_type mgz --input_volume structural.nii --output_volume outfile.mgz'


    """

    executable = "mri_convert"
    read_only: bool = shell.arg(help="read the input volume", argstr="--read_only")
    no_write: bool = shell.arg(help="do not write output", argstr="--no_write")
    in_info: bool = shell.arg(help="display input info", argstr="--in_info")
    out_info: bool = shell.arg(help="display output info", argstr="--out_info")
    in_stats: bool = shell.arg(help="display input stats", argstr="--in_stats")
    out_stats: bool = shell.arg(help="display output stats", argstr="--out_stats")
    in_matrix: bool = shell.arg(help="display input matrix", argstr="--in_matrix")
    out_matrix: bool = shell.arg(help="display output matrix", argstr="--out_matrix")
    in_i_size: int = shell.arg(help="input i size", argstr="--in_i_size {in_i_size}")
    in_j_size: int = shell.arg(help="input j size", argstr="--in_j_size {in_j_size}")
    in_k_size: int = shell.arg(help="input k size", argstr="--in_k_size {in_k_size}")
    force_ras: bool = shell.arg(
        help="use default when orientation info absent", argstr="--force_ras_good"
    )
    in_i_dir: ty.Any = shell.arg(
        help="<R direction> <A direction> <S direction>",
        argstr="--in_i_direction {in_i_dir[0]} {in_i_dir[1]} {in_i_dir[2]}",
    )
    in_j_dir: ty.Any = shell.arg(
        help="<R direction> <A direction> <S direction>",
        argstr="--in_j_direction {in_j_dir[0]} {in_j_dir[1]} {in_j_dir[2]}",
    )
    in_k_dir: ty.Any = shell.arg(
        help="<R direction> <A direction> <S direction>",
        argstr="--in_k_direction {in_k_dir[0]} {in_k_dir[1]} {in_k_dir[2]}",
    )
    in_orientation: ty.Any = shell.arg(
        help="specify the input orientation", argstr="--in_orientation {in_orientation}"
    )
    in_center: list[float] = shell.arg(
        help="<R coordinate> <A coordinate> <S coordinate>",
        argstr="--in_center {in_center}",
    )
    sphinx: bool = shell.arg(
        help="change orientation info to sphinx", argstr="--sphinx"
    )
    out_i_count: int = shell.arg(
        help="some count ?? in i direction", argstr="--out_i_count {out_i_count}"
    )
    out_j_count: int = shell.arg(
        help="some count ?? in j direction", argstr="--out_j_count {out_j_count}"
    )
    out_k_count: int = shell.arg(
        help="some count ?? in k direction", argstr="--out_k_count {out_k_count}"
    )
    vox_size: ty.Any = shell.arg(
        help="<size_x> <size_y> <size_z> specify the size (mm) - useful for upsampling or downsampling",
        argstr="-voxsize {vox_size[0]} {vox_size[1]} {vox_size[2]}",
    )
    out_i_size: int = shell.arg(
        help="output i size", argstr="--out_i_size {out_i_size}"
    )
    out_j_size: int = shell.arg(
        help="output j size", argstr="--out_j_size {out_j_size}"
    )
    out_k_size: int = shell.arg(
        help="output k size", argstr="--out_k_size {out_k_size}"
    )
    out_i_dir: ty.Any = shell.arg(
        help="<R direction> <A direction> <S direction>",
        argstr="--out_i_direction {out_i_dir[0]} {out_i_dir[1]} {out_i_dir[2]}",
    )
    out_j_dir: ty.Any = shell.arg(
        help="<R direction> <A direction> <S direction>",
        argstr="--out_j_direction {out_j_dir[0]} {out_j_dir[1]} {out_j_dir[2]}",
    )
    out_k_dir: ty.Any = shell.arg(
        help="<R direction> <A direction> <S direction>",
        argstr="--out_k_direction {out_k_dir[0]} {out_k_dir[1]} {out_k_dir[2]}",
    )
    out_orientation: ty.Any = shell.arg(
        help="specify the output orientation",
        argstr="--out_orientation {out_orientation}",
    )
    out_center: ty.Any = shell.arg(
        help="<R coordinate> <A coordinate> <S coordinate>",
        argstr="--out_center {out_center[0]} {out_center[1]} {out_center[2]}",
    )
    out_datatype: ty.Any = shell.arg(
        help="output data type <uchar|short|int|float>",
        argstr="--out_data_type {out_datatype}",
    )
    resample_type: ty.Any = shell.arg(
        help="<interpolate|weighted|nearest|sinc|cubic> (default is interpolate)",
        argstr="--resample_type {resample_type}",
    )
    no_scale: bool = shell.arg(
        help="dont rescale values for COR", argstr="--no_scale 1"
    )
    no_change: bool = shell.arg(
        help="don't change type of input to that of template", argstr="--nochange"
    )
    tr: int = shell.arg(help="TR in msec", argstr="-tr {tr}")
    te: int = shell.arg(help="TE in msec", argstr="-te {te}")
    ti: int = shell.arg(help="TI in msec (note upper case flag)", argstr="-ti {ti}")
    autoalign_matrix: File = shell.arg(
        help="text file with autoalign matrix", argstr="--autoalign {autoalign_matrix}"
    )
    unwarp_gradient: bool = shell.arg(
        help="unwarp gradient nonlinearity", argstr="--unwarp_gradient_nonlinearity"
    )
    apply_transform: File = shell.arg(
        help="apply xfm file", argstr="--apply_transform {apply_transform}"
    )
    apply_inv_transform: File = shell.arg(
        help="apply inverse transformation xfm file",
        argstr="--apply_inverse_transform {apply_inv_transform}",
    )
    devolve_transform: str = shell.arg(
        help="subject id", argstr="--devolvexfm {devolve_transform}"
    )
    crop_center: ty.Any = shell.arg(
        help="<x> <y> <z> crop to 256 around center (x, y, z)",
        argstr="--crop {crop_center[0]} {crop_center[1]} {crop_center[2]}",
    )
    crop_size: ty.Any = shell.arg(
        help="<dx> <dy> <dz> crop to size <dx, dy, dz>",
        argstr="--cropsize {crop_size[0]} {crop_size[1]} {crop_size[2]}",
    )
    cut_ends: int = shell.arg(
        help="remove ncut slices from the ends", argstr="--cutends {cut_ends}"
    )
    slice_crop: ty.Any = shell.arg(
        help="s_start s_end : keep slices s_start to s_end",
        argstr="--slice-crop {slice_crop[0]} {slice_crop[1]}",
    )
    slice_reverse: bool = shell.arg(
        help="reverse order of slices, update vox2ras", argstr="--slice-reverse"
    )
    slice_bias: float = shell.arg(
        help="apply half-cosine bias field", argstr="--slice-bias {slice_bias}"
    )
    fwhm: float = shell.arg(
        help="smooth input volume by fwhm mm", argstr="--fwhm {fwhm}"
    )
    in_type: ty.Any = shell.arg(help="input file type", argstr="--in_type {in_type}")
    out_type: ty.Any = shell.arg(
        help="output file type", argstr="--out_type {out_type}"
    )
    ascii: bool = shell.arg(
        help="save output as ascii col>row>slice>frame", argstr="--ascii"
    )
    reorder: ty.Any = shell.arg(
        help="olddim1 olddim2 olddim3",
        argstr="--reorder {reorder[0]} {reorder[1]} {reorder[2]}",
    )
    invert_contrast: float = shell.arg(
        help="threshold for inversting contrast",
        argstr="--invert_contrast {invert_contrast}",
    )
    in_file: Nifti1 = shell.arg(
        help="File to read/convert", argstr="--input_volume {in_file}", position=-2
    )
    conform: bool = shell.arg(
        help="conform to 1mm voxel size in coronal slice direction with 256^3 or more",
        argstr="--conform",
    )
    conform_min: bool = shell.arg(
        help="conform to smallest size", argstr="--conform_min"
    )
    conform_size: float = shell.arg(
        help="conform to size_in_mm", argstr="--conform_size {conform_size}"
    )
    cw256: bool = shell.arg(help="confrom to dimensions of 256^3", argstr="--cw256")
    parse_only: bool = shell.arg(help="parse input only", argstr="--parse_only")
    subject_name: str = shell.arg(
        help="subject name ???", argstr="--subject_name {subject_name}"
    )
    reslice_like: File = shell.arg(
        help="reslice output to match file", argstr="--reslice_like {reslice_like}"
    )
    template_type: ty.Any = shell.arg(
        help="template file type", argstr="--template_type {template_type}"
    )
    split_: bool = shell.arg(
        help="split output frames into separate output files.", argstr="--split"
    )
    frame: int = shell.arg(
        help="keep only 0-based frame number", argstr="--frame {frame}"
    )
    midframe: bool = shell.arg(help="keep only the middle frame", argstr="--mid-frame")
    skip_n: int = shell.arg(help="skip the first n frames", argstr="--nskip {skip_n}")
    drop_n: int = shell.arg(help="drop the last n frames", argstr="--ndrop {drop_n}")
    frame_subsample: ty.Any = shell.arg(
        help="start delta end : frame subsampling (end = -1 for end)",
        argstr="--fsubsample {frame_subsample[0]} {frame_subsample[1]} {frame_subsample[2]}",
    )
    in_scale: float = shell.arg(
        help="input intensity scale factor", argstr="--scale {in_scale}"
    )
    out_scale: float = shell.arg(
        help="output intensity scale factor", argstr="--out-scale {out_scale}"
    )
    in_like: File = shell.arg(help="input looks like", argstr="--in_like {in_like}")
    fill_parcellation: bool = shell.arg(
        help="fill parcellation", argstr="--fill_parcellation"
    )
    smooth_parcellation: bool = shell.arg(
        help="smooth parcellation", argstr="--smooth_parcellation"
    )
    zero_outlines: bool = shell.arg(help="zero outlines", argstr="--zero_outlines")
    color_file: File = shell.arg(help="color file", argstr="--color_file {color_file}")
    no_translate: bool = shell.arg(help="???", argstr="--no_translate")
    status_file: File = shell.arg(
        help="status file for DICOM conversion", argstr="--status {status_file}"
    )
    sdcm_list: File = shell.arg(
        help="list of DICOM files for conversion", argstr="--sdcmlist {sdcm_list}"
    )
    template_info: bool = shell.arg(
        help="dump info about template", argstr="--template_info"
    )
    crop_gdf: bool = shell.arg(help="apply GDF cropping", argstr="--crop_gdf")
    zero_ge_z_offset: bool = shell.arg(
        help="zero ge z offset ???", argstr="--zero_ge_z_offset"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="output filename or True to generate one",
            argstr="--output_volume {out_file}",
            position=-1,
            path_template="out_file",
        )


def _get_outfilename(in_file=None, out_file=None, out_type=None):
    self_dict = {}
    outfile = out_file
    if outfile is attrs.NOTHING:
        if out_type is not attrs.NOTHING:
            suffix = "_out." + self_dict["filemap"][out_type]
        else:
            suffix = "_out.nii.gz"
        outfile = fname_presuffix(
            in_file, newpath=output_dir, suffix=suffix, use_ext=False
        )
    return os.path.abspath(outfile)
