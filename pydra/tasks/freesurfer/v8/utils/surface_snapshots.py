import attrs
from fileformats.generic import Directory, File
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import fname_presuffix
from pydra.compose import shell
import re
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "tcl_script":
        if value is attrs.NOTHING:
            return "-tcl snapshots.tcl"
        else:
            return "-tcl %s" % value
    elif name == "overlay_range":
        if isinstance(value, float):
            return "-fthresh %.3f" % value
        else:
            if len(value) == 2:
                return "-fminmax %.3f %.3f" % value
            else:
                return "-fminmax {:.3f} {:.3f} -fmid {:.3f}".format(
                    value[0],
                    value[2],
                    value[1],
                )
    elif name == "annot_name" and (value is not attrs.NOTHING):

        if value.endswith(".annot"):
            value = value[:-6]
        if re.match(r"%s[\.\-_]" % inputs["hemi"], value[:3]):
            value = value[3:]
        return "-annotation %s" % value

    return argstr.format(**inputs)


def tcl_script_formatter(field, inputs):
    return _format_arg("tcl_script", field, inputs, argstr="{tcl_script}")


def overlay_range_formatter(field, inputs):
    return _format_arg("overlay_range", field, inputs, argstr="{overlay_range}")


def annot_name_formatter(field, inputs):
    return _format_arg("annot_name", field, inputs, argstr="-annotation {annot_name}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    self_dict = {}

    outputs = {}
    if inputs["screenshot_stem"] is attrs.NOTHING:
        stem = "{}_{}_{}".format(
            inputs["subject_id"],
            inputs["hemi"],
            inputs["surface"],
        )
    else:
        stem = inputs["screenshot_stem"]
        stem_args = inputs["stem_template_args"]
        if stem_args is not attrs.NOTHING:
            args = tuple(getattr(self_dict["inputs"], arg) for arg in stem_args)
            stem = stem % args
    snapshots = ["%s-lat.tif", "%s-med.tif", "%s-dor.tif", "%s-ven.tif"]
    if inputs["six_images"]:
        snapshots.extend(["%s-pos.tif", "%s-ant.tif"])
    snapshots = [
        _gen_fname(
            f % stem,
            suffix="",
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
        for f in snapshots
    ]
    outputs["snapshots"] = snapshots
    return outputs


def snapshots_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("snapshots")


def _gen_filename(name, inputs):
    if name == "tcl_script":
        return "snapshots.tcl"
    return None


def tcl_script_default(inputs):
    return _gen_filename("tcl_script", inputs=inputs)


@shell.define(
    xor=[
        ["annot_file", "annot_name"],
        ["identity_reg", "mni152_reg", "overlay_reg"],
        ["label_file", "label_name"],
        ["show_curv", "show_gray_curv"],
    ]
)
class SurfaceSnapshots(shell.Task["SurfaceSnapshots.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.v8.utils.surface_snapshots import SurfaceSnapshots

    """

    executable = "tksurfer"
    subject_id: ty.Any = shell.arg(
        help="subject to visualize", argstr="{subject_id}", position=1
    )
    hemi: ty.Any = shell.arg(
        help="hemisphere to visualize", argstr="{hemi}", position=2
    )
    surface: ty.Any = shell.arg(
        help="surface to visualize", argstr="{surface}", position=3
    )
    show_curv: bool = shell.arg(help="show curvature", argstr="-curv")
    show_gray_curv: bool = shell.arg(help="show curvature in gray", argstr="-gray")
    overlay: File | None = shell.arg(
        help="load an overlay volume/surface",
        argstr="-overlay {overlay}",
        requires=["overlay_range"],
    )
    overlay_reg: File | None = shell.arg(
        help="registration matrix file to register overlay to surface",
        argstr="-overlay-reg {overlay_reg}",
    )
    identity_reg: bool = shell.arg(
        help="use the identity matrix to register the overlay to the surface",
        argstr="-overlay-reg-identity",
    )
    mni152_reg: bool = shell.arg(
        help="use to display a volume in MNI152 space on the average subject",
        argstr="-mni152reg",
    )
    overlay_range: ty.Any = shell.arg(
        help="overlay range--either min, (min, max) or (min, mid, max)",
        formatter="overlay_range_formatter",
    )
    overlay_range_offset: float = shell.arg(
        help="overlay range will be symmetric around offset value",
        argstr="-foffset {overlay_range_offset:.3}",
    )
    truncate_overlay: bool = shell.arg(
        help="truncate the overlay display", argstr="-truncphaseflag 1"
    )
    reverse_overlay: bool = shell.arg(
        help="reverse the overlay display", argstr="-revphaseflag 1"
    )
    invert_overlay: bool = shell.arg(
        help="invert the overlay display", argstr="-invphaseflag 1"
    )
    demean_overlay: bool = shell.arg(help="remove mean from overlay", argstr="-zm")
    annot_file: File | None = shell.arg(
        help="path to annotation file to display", argstr="-annotation {annot_file}"
    )
    annot_name: ty.Any | None = shell.arg(
        help="name of annotation to display (must be in $subject/label directory",
        formatter="annot_name_formatter",
    )
    label_file: File | None = shell.arg(
        help="path to label file to display", argstr="-label {label_file}"
    )
    label_name: ty.Any | None = shell.arg(
        help="name of label to display (must be in $subject/label directory",
        argstr="-label {label_name}",
    )
    colortable: File = shell.arg(
        help="load colortable file", argstr="-colortable {colortable}"
    )
    label_under: bool = shell.arg(
        help="draw label/annotation under overlay", argstr="-labels-under"
    )
    label_outline: bool = shell.arg(
        help="draw label/annotation as outline", argstr="-label-outline"
    )
    patch_file: File = shell.arg(help="load a patch", argstr="-patch {patch_file}")
    orig_suffix: ty.Any = shell.arg(
        help="set the orig surface suffix string", argstr="-orig {orig_suffix}"
    )
    sphere_suffix: ty.Any = shell.arg(
        help="set the sphere.reg suffix string", argstr="-sphere {sphere_suffix}"
    )
    show_color_scale: bool = shell.arg(
        help="display the color scale bar", argstr="-colscalebarflag 1"
    )
    show_color_text: bool = shell.arg(
        help="display text in the color scale bar", argstr="-colscaletext 1"
    )
    six_images: bool = shell.arg(help="also take anterior and posterior snapshots")
    screenshot_stem: ty.Any = shell.arg(help="stem to use for screenshot file names")
    stem_template_args: list[ty.Any] = shell.arg(
        help="input names to use as arguments for a string-formated stem template",
        requires=["screenshot_stem"],
    )
    tcl_script: File = shell.arg(
        help="override default screenshot script", formatter="tcl_script_formatter"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        snapshots: list[File] | None = shell.out(
            help="tiff images of the surface from different perspectives",
            callable=snapshots_callable,
        )


def _gen_fname(
    basename,
    fname=None,
    cwd=None,
    suffix="_fs",
    use_ext=True,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    """Define a generic mapping for a single outfile

    The filename is potentially autogenerated by suffixing inputs.infile

    Parameters
    ----------
    basename : string (required)
        filename to base the new filename on
    fname : string
        if not None, just use this fname
    cwd : string
        prefix paths with cwd, otherwise output_dir
    suffix : string
        default suffix
    """
    if basename == "":
        msg = "Unable to generate filename for command %s. " % "tksurfer"
        msg += "basename is not set!"
        raise ValueError(msg)
    if cwd is None:
        cwd = output_dir
    fname = fname_presuffix(basename, suffix=suffix, use_ext=use_ext, newpath=cwd)
    return fname
