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

    if name == "count_file":
        if isinstance(value, bool):
            fname = _list_outputs(
                binary_file=inputs["binary_file"],
                count_file=inputs["count_file"],
                in_file=inputs["in_file"],
                out_type=inputs["out_type"],
            )[name]
        else:
            fname = value
        return argstr.format(**{name: fname})
    if name == "out_type":
        return ""

    return argstr.format(**inputs)


def count_file_formatter(field, inputs):
    return _format_arg("count_file", field, inputs, argstr="--count {count_file}")


def out_type_formatter(field, inputs):
    return _format_arg("out_type", field, inputs, argstr="")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outfile = inputs["binary_file"]
    if outfile is attrs.NOTHING:
        if inputs["out_type"] is not attrs.NOTHING:
            outfile = fname_presuffix(
                inputs["in_file"],
                newpath=os.getcwd(),
                suffix=f"_thresh.{inputs['out_type']}",
                use_ext=False,
            )
        else:
            outfile = fname_presuffix(
                inputs["in_file"], newpath=os.getcwd(), suffix="_thresh"
            )
    outputs["binary_file"] = os.path.abspath(outfile)
    value = inputs["count_file"]
    if value is not attrs.NOTHING:
        if isinstance(value, bool):
            if value:
                outputs["count_file"] = fname_presuffix(
                    inputs["in_file"],
                    suffix="_count.txt",
                    newpath=os.getcwd(),
                    use_ext=False,
                )
        else:
            outputs["count_file"] = value
    return outputs


def count_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("count_file")


def _gen_filename(name, inputs):
    if name == "binary_file":
        return _list_outputs(
            binary_file=inputs["binary_file"],
            count_file=inputs["count_file"],
            in_file=inputs["in_file"],
            out_type=inputs["out_type"],
        )[name]
    return None


def binary_file_default(inputs):
    return _gen_filename("binary_file", inputs=inputs)


@shell.define(
    xor=[["max", "min", "wm_ven_csf"], ["max", "wm_ven_csf"], ["min", "wm_ven_csf"]]
)
class Binarize(shell.Task["Binarize.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.model.binarize import Binarize

    >>> task = Binarize()
    >>> task.in_file = Nifti1.mock("structural.nii")
    >>> task.min = 10
    >>> task.binary_file = "foo_out.nii"
    >>> task.merge_file = File.mock()
    >>> task.mask_file = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_binarize"
    in_file: Nifti1 = shell.arg(help="input volume", argstr="--i {in_file}")
    min: float | None = shell.arg(help="min thresh", argstr="--min {min}")
    max: float | None = shell.arg(help="max thresh", argstr="--max {max}")
    rmin: float = shell.arg(
        help="compute min based on rmin*globalmean", argstr="--rmin {rmin}"
    )
    rmax: float = shell.arg(
        help="compute max based on rmax*globalmean", argstr="--rmax {rmax}"
    )
    match: list[int] = shell.arg(
        help="match instead of threshold", argstr="--match {match}..."
    )
    wm: bool = shell.arg(
        help="set match vals to 2 and 41 (aseg for cerebral WM)", argstr="--wm"
    )
    ventricles: bool = shell.arg(
        help="set match vals those for aseg ventricles+choroid (not 4th)",
        argstr="--ventricles",
    )
    wm_ven_csf: bool = shell.arg(
        help="WM and ventricular CSF, including choroid (not 4th)", argstr="--wm+vcsf"
    )
    out_type: ty.Any = shell.arg(
        help="output file type", formatter="out_type_formatter"
    )
    count_file: ty.Any = shell.arg(
        help="save number of hits in ascii file (hits, ntotvox, pct)",
        formatter="count_file_formatter",
    )
    bin_val: int = shell.arg(
        help="set vox within thresh to val (default is 1)", argstr="--binval {bin_val}"
    )
    bin_val_not: int = shell.arg(
        help="set vox outside range to val (default is 0)",
        argstr="--binvalnot {bin_val_not}",
    )
    invert: bool = shell.arg(help="set binval=0, binvalnot=1", argstr="--inv")
    frame_no: int = shell.arg(
        help="use 0-based frame of input (default is 0)", argstr="--frame {frame_no}"
    )
    merge_file: File = shell.arg(
        help="merge with mergevol", argstr="--merge {merge_file}"
    )
    mask_file: File = shell.arg(help="must be within mask", argstr="--mask maskvol")
    mask_thresh: float = shell.arg(
        help="set thresh for mask", argstr="--mask-thresh {mask_thresh}"
    )
    abs: bool = shell.arg(
        help="take abs of invol first (ie, make unsigned)", argstr="--abs"
    )
    bin_col_num: bool = shell.arg(
        help="set binarized voxel value to its column number", argstr="--bincol"
    )
    zero_edges: bool = shell.arg(help="zero the edge voxels", argstr="--zero-edges")
    zero_slice_edge: bool = shell.arg(
        help="zero the edge slice voxels", argstr="--zero-slice-edges"
    )
    dilate: int = shell.arg(
        help="niters: dilate binarization in 3D", argstr="--dilate {dilate}"
    )
    erode: int = shell.arg(
        help="nerode: erode binarization in 3D (after any dilation)",
        argstr="--erode  {erode}",
    )
    erode2d: int = shell.arg(
        help="nerode2d: erode binarization in 2D (after any 3D erosion)",
        argstr="--erode2d {erode2d}",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        binary_file: Path = shell.outarg(
            help="binary output volume",
            argstr="--o {binary_file}",
            path_template='"foo_out.nii"',
        )
        count_file: File | None = shell.out(
            help="ascii file containing number of hits", callable=count_file_callable
        )
