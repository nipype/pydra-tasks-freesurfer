import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import NiftiGz
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import (
    fname_presuffix,
    split_filename,
)
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "sampling_method":
        range = inputs["sampling_range"]
        units = inputs["sampling_units"]
        if units == "mm":
            units = "dist"
        if isinstance(range, tuple):
            range = "%.3f %.3f %.3f" % range
        else:
            range = "%.3f" % range
        method = dict(point="", max="-max", average="-avg")[value]
        return f"--proj{units}{method} {range}"

    if name == "reg_header":
        return argstr.format(**{name: inputs["subject_id"]})
    if name == "override_reg_subj":
        return argstr.format(**{name: inputs["subject_id"]})
    if name in ["hits_file", "vox_file"]:
        return argstr.format(
            **{
                name: _get_outfilename(
                    name,
                    hemi=inputs["hemi"],
                    out_type=inputs["out_type"],
                    source_file=inputs["source_file"],
                )
            }
        )
    if name == "out_type":
        if inputs["out_file"] is not attrs.NOTHING:
            _, base, ext = split_filename(
                _get_outfilename(
                    hemi=inputs["hemi"],
                    out_type=inputs["out_type"],
                    source_file=inputs["source_file"],
                )
            )
            if ext != filemap[value]:
                if ext in filemap.values():
                    raise ValueError(
                        "Cannot create {} file with extension " "{}".format(value, ext)
                    )
                else:
                    logger.warning(
                        "Creating %s file with extension %s: %s%s",
                        value,
                        ext,
                        base,
                        ext,
                    )

        if value in implicit_filetypes:
            return ""
    if name == "surf_reg":
        if value is True:
            return argstr.format(**{name: "sphere.reg"})

    return argstr.format(**inputs)


def sampling_method_formatter(field, inputs):
    return _format_arg("sampling_method", field, inputs, argstr="{sampling_method}")


def reg_header_formatter(field, inputs):
    return _format_arg("reg_header", field, inputs, argstr="--regheader {reg_header:d}")


def override_reg_subj_formatter(field, inputs):
    return _format_arg(
        "override_reg_subj", field, inputs, argstr="--srcsubject {override_reg_subj:d}"
    )


def out_type_formatter(field, inputs):
    return _format_arg("out_type", field, inputs, argstr="--out_type {out_type}")


def surf_reg_formatter(field, inputs):
    return _format_arg("surf_reg", field, inputs, argstr="--surfreg {surf_reg}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.abspath(
        _get_outfilename(
            hemi=inputs["hemi"],
            out_type=inputs["out_type"],
            source_file=inputs["source_file"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    )
    hitsfile = inputs["hits_file"]
    if hitsfile is not attrs.NOTHING:
        outputs["hits_file"] = hitsfile
        if isinstance(hitsfile, bool):
            hitsfile = _get_outfilename(
                "hits_file",
                hemi=inputs["hemi"],
                out_type=inputs["out_type"],
                source_file=inputs["source_file"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
    voxfile = inputs["vox_file"]
    if voxfile is not attrs.NOTHING:
        if isinstance(voxfile, bool):
            voxfile = fname_presuffix(
                inputs["source_file"],
                newpath=os.getcwd(),
                prefix=inputs["hemi"] + ".",
                suffix="_vox.txt",
                use_ext=False,
            )
        outputs["vox_file"] = voxfile
    return outputs


def hits_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("hits_file")


def vox_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("vox_file")


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            hemi=inputs["hemi"],
            hits_file=inputs["hits_file"],
            out_type=inputs["out_type"],
            source_file=inputs["source_file"],
            vox_file=inputs["vox_file"],
        )[name]
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define(
    xor=[
        ["cortex_mask", "mask_label"],
        ["mni152reg", "reg_file", "reg_header"],
        ["no_reshape", "reshape"],
        ["projection_stem", "sampling_method"],
    ]
)
class SampleToSurface(shell.Task["SampleToSurface.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import NiftiGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.sample_to_surface import SampleToSurface

    >>> task = SampleToSurface()
    >>> task.source_file = NiftiGz.mock("cope1.nii.gz")
    >>> task.reference_file = File.mock()
    >>> task.hemi = "lh"
    >>> task.reg_file = File.mock()
    >>> task.sampling_method = "average"
    >>> task.sampling_units = "frac"
    >>> task.mask_label = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_vol2surf --hemi lh --o ...lh.cope1.mgz --reg register.dat --projfrac-avg 1.000 --mov cope1.nii.gz'


    """

    executable = "mri_vol2surf"
    source_file: NiftiGz = shell.arg(
        help="volume to sample values from", argstr="--mov {source_file}"
    )
    reference_file: File = shell.arg(
        help="reference volume (default is orig.mgz)", argstr="--ref {reference_file}"
    )
    hemi: ty.Any = shell.arg(help="target hemisphere", argstr="--hemi {hemi}")
    surface: ty.Any = shell.arg(
        help="target surface (default is white)", argstr="--surf {surface}"
    )
    reg_file: File | None = shell.arg(
        help="source-to-reference registration file", argstr="--reg {reg_file}"
    )
    reg_header: bool = shell.arg(
        help="register based on header geometry",
        requires=["subject_id"],
        formatter="reg_header_formatter",
    )
    mni152reg: bool = shell.arg(
        help="source volume is in MNI152 space", argstr="--mni152reg"
    )
    apply_rot: ty.Any = shell.arg(
        help="rotation angles (in degrees) to apply to reg matrix",
        argstr="--rot {apply_rot[0]:.3} {apply_rot[1]:.3} {apply_rot[2]:.3}",
    )
    apply_trans: ty.Any = shell.arg(
        help="translation (in mm) to apply to reg matrix",
        argstr="--trans {apply_trans[0]:.3} {apply_trans[1]:.3} {apply_trans[2]:.3}",
    )
    override_reg_subj: bool = shell.arg(
        help="override the subject in the reg file header",
        requires=["subject_id"],
        formatter="override_reg_subj_formatter",
    )
    sampling_method: ty.Any | None = shell.arg(
        help="how to sample -- at a point or at the max or average over a range",
        requires=["sampling_range", "sampling_units"],
        formatter="sampling_method_formatter",
    )
    sampling_range: ty.Any = shell.arg(
        help="sampling range - a point or a tuple of (min, max, step)"
    )
    sampling_units: ty.Any = shell.arg(
        help="sampling range type -- either 'mm' or 'frac'"
    )
    projection_stem: ty.Any | None = shell.arg(
        help="stem for precomputed linear estimates and volume fractions"
    )
    smooth_vol: float = shell.arg(
        help="smooth input volume (mm fwhm)", argstr="--fwhm {smooth_vol:.3}"
    )
    smooth_surf: float = shell.arg(
        help="smooth output surface (mm fwhm)", argstr="--surf-fwhm {smooth_surf:.3}"
    )
    interp_method: ty.Any = shell.arg(
        help="interpolation method", argstr="--interp {interp_method}"
    )
    cortex_mask: bool = shell.arg(
        help="mask the target surface with hemi.cortex.label", argstr="--cortex"
    )
    mask_label: File | None = shell.arg(
        help="label file to mask output with", argstr="--mask {mask_label}"
    )
    float2int_method: ty.Any = shell.arg(
        help="method to convert reg matrix values (default is round)",
        argstr="--float2int {float2int_method}",
    )
    fix_tk_reg: bool = shell.arg(
        help="make reg matrix round-compatible", argstr="--fixtkreg"
    )
    subject_id: ty.Any = shell.arg(help="subject id")
    target_subject: ty.Any = shell.arg(
        help="sample to surface of different subject than source",
        argstr="--trgsubject {target_subject}",
    )
    surf_reg: ty.Any = shell.arg(
        help="use surface registration to target subject",
        requires=["target_subject"],
        formatter="surf_reg_formatter",
    )
    ico_order: int = shell.arg(
        help="icosahedron order when target_subject is 'ico'",
        argstr="--icoorder {ico_order}",
        requires=["target_subject"],
    )
    reshape: bool = shell.arg(
        help="reshape surface vector to fit in non-mgh format", argstr="--reshape"
    )
    no_reshape: bool = shell.arg(
        help="do not reshape surface vector (default)", argstr="--noreshape"
    )
    reshape_slices: int = shell.arg(
        help="number of 'slices' for reshaping", argstr="--rf {reshape_slices}"
    )
    scale_input: float = shell.arg(
        help="multiple all intensities by scale factor",
        argstr="--scale {scale_input:.3}",
    )
    frame: int = shell.arg(
        help="save only one frame (0-based)", argstr="--frame {frame}"
    )
    out_type: ty.Any = shell.arg(
        help="output file type", formatter="out_type_formatter"
    )
    hits_file: ty.Any = shell.arg(
        help="save image with number of hits at each voxel",
        argstr="--srchit {hits_file}",
    )
    hits_type: ty.Any = shell.arg(help="hits file type", argstr="--srchit_type")
    vox_file: ty.Any = shell.arg(
        help="text file with the number of voxels intersecting the surface",
        argstr="--nvox {vox_file}",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="surface file to write",
            argstr="--o {out_file}",
            path_template="out_file",
        )
        hits_file: File | None = shell.out(
            help="image with number of hits at each voxel", callable=hits_file_callable
        )
        vox_file: File | None = shell.out(
            help="text file with the number of voxels intersecting the surface",
            callable=vox_file_callable,
        )


def _get_outfilename(
    opt="out_file",
    hemi=None,
    out_type=None,
    source_file=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    self_dict = {}
    outfile = getattr(self_dict["inputs"], opt)
    if (outfile is attrs.NOTHING) or isinstance(outfile, bool):
        if out_type is not attrs.NOTHING:
            if opt == "hits_file":
                suffix = "_hits." + filemap[out_type]
            else:
                suffix = "." + filemap[out_type]
        elif opt == "hits_file":
            suffix = "_hits.mgz"
        else:
            suffix = ".mgz"
        outfile = fname_presuffix(
            source_file,
            newpath=output_dir,
            prefix=hemi + ".",
            suffix=suffix,
            use_ext=False,
        )
    return outfile


filemap = dict(
    cor="cor",
    mgh="mgh",
    mgz="mgz",
    minc="mnc",
    afni="brik",
    brik="brik",
    bshort="bshort",
    spm="img",
    analyze="img",
    analyze4d="img",
    bfloat="bfloat",
    nifti1="img",
    nii="nii",
    niigz="nii.gz",
    gii="gii",
)

implicit_filetypes = ["gii"]

logger = logging.getLogger("nipype.interface")
