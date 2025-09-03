import attrs
from fileformats.generic import Directory, File
import logging
from pydra.compose import shell
import re
import typing as ty


logger = logging.getLogger(__name__)


def aggregate_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    needed_outputs = [
        "info",
        "out_file",
        "data_type",
        "file_format",
        "TE",
        "TR",
        "TI",
        "dimensions",
        "vox_sizes",
        "orientation",
        "ph_enc_dir",
    ]

    outputs = {}
    info = stdout
    outputs["info"] = info

    for field in ["TE", "TR", "TI"]:
        fieldval = info_regexp(
            info,
            field,
            ", ",
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
        if fieldval.endswith(" msec"):
            fieldval = fieldval[:-5]
        outputs[field] = fieldval

    vox = info_regexp(
        info,
        "voxel sizes",
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    vox = tuple(vox.split(", "))
    outputs["vox_sizes"] = vox
    dim = info_regexp(
        info,
        "dimensions",
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    dim = tuple(int(d) for d in dim.split(" x "))
    outputs["dimensions"] = dim

    outputs["orientation"] = info_regexp(
        info,
        "Orientation",
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    outputs["ph_enc_dir"] = info_regexp(
        info,
        "PhEncDir",
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )

    ftype, dtype = re.findall(r"%s\s*:\s+(.+?)\n" % "type", info)
    outputs["file_format"] = ftype
    outputs["data_type"] = dtype

    return outputs


def info_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("info")


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


def data_type_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("data_type")


def file_format_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("file_format")


def TE_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("TE")


def TR_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("TR")


def TI_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("TI")


def dimensions_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("dimensions")


def vox_sizes_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("vox_sizes")


def orientation_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("orientation")


def ph_enc_dir_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("ph_enc_dir")


@shell.define
class ImageInfo(shell.Task["ImageInfo.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.v8.utils.image_info import ImageInfo

    """

    executable = "mri_info"
    in_file: File = shell.arg(help="image to query", argstr="{in_file}", position=1)
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        info: ty.Any | None = shell.out(
            help="output of mri_info", callable=info_callable
        )
        out_file: File | None = shell.out(
            help="text file with image information", callable=out_file_callable
        )
        data_type: ty.Any | None = shell.out(
            help="image data type", callable=data_type_callable
        )
        file_format: ty.Any | None = shell.out(
            help="file format", callable=file_format_callable
        )
        TE: ty.Any | None = shell.out(help="echo time (msec)", callable=TE_callable)
        TR: ty.Any | None = shell.out(
            help="repetition time(msec)", callable=TR_callable
        )
        TI: ty.Any | None = shell.out(
            help="inversion time (msec)", callable=TI_callable
        )
        dimensions: ty.Any | None = shell.out(
            help="image dimensions (voxels)", callable=dimensions_callable
        )
        vox_sizes: ty.Any | None = shell.out(
            help="voxel sizes (mm)", callable=vox_sizes_callable
        )
        orientation: ty.Any | None = shell.out(
            help="image orientation", callable=orientation_callable
        )
        ph_enc_dir: ty.Any | None = shell.out(
            help="phase encode direction", callable=ph_enc_dir_callable
        )


def info_regexp(info, field, delim="\n"):
    m = re.search(rf"{field}\s*:\s+(.+?){delim}", info)
    if m:
        return m.group(1)
    else:
        return None
