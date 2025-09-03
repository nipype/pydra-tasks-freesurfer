import attrs
from fileformats.generic import Directory, File
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import split_filename
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "out_file" and not os.path.isabs(value):
        value = os.path.abspath(value)

    return argstr.format(**inputs)


def out_file_formatter(field, inputs):
    return _format_arg("out_file", field, inputs, argstr="{out_file}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["converted"] = os.path.abspath(
        _gen_outfilename(
            annot_file=inputs["annot_file"],
            functional_file=inputs["functional_file"],
            in_file=inputs["in_file"],
            label_file=inputs["label_file"],
            out_datatype=inputs["out_datatype"],
            out_file=inputs["out_file"],
            parcstats_file=inputs["parcstats_file"],
            scalarcurv_file=inputs["scalarcurv_file"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    )
    return outputs


def converted_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("converted")


def _gen_filename(name, inputs):
    if name == "out_file":
        return os.path.abspath(
            _gen_outfilename(
                annot_file=inputs["annot_file"],
                functional_file=inputs["functional_file"],
                in_file=inputs["in_file"],
                label_file=inputs["label_file"],
                out_datatype=inputs["out_datatype"],
                out_file=inputs["out_file"],
                parcstats_file=inputs["parcstats_file"],
                scalarcurv_file=inputs["scalarcurv_file"],
            )
        )
    else:
        return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define(xor=[["out_datatype", "out_file"]])
class MRIsConvert(shell.Task["MRIsConvert.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.mr_is_convert import MRIsConvert

    """

    executable = "mris_convert"
    annot_file: File = shell.arg(
        help="input is annotation or gifti label data", argstr="--annot {annot_file}"
    )
    parcstats_file: File = shell.arg(
        help="infile is name of text file containing label/val pairs",
        argstr="--parcstats {parcstats_file}",
    )
    label_file: File = shell.arg(
        help="infile is .label file, label is name of this label",
        argstr="--label {label_file}",
    )
    scalarcurv_file: File = shell.arg(
        help="input is scalar curv overlay file (must still specify surface)",
        argstr="-c {scalarcurv_file}",
    )
    functional_file: File = shell.arg(
        help="input is functional time-series or other multi-frame data (must specify surface)",
        argstr="-f {functional_file}",
    )
    labelstats_outfile: File = shell.arg(
        help="outfile is name of gifti file to which label stats will be written",
        argstr="--labelstats {labelstats_outfile}",
    )
    patch: bool = shell.arg(help="input is a patch, not a full surface", argstr="-p")
    rescale: bool = shell.arg(
        help="rescale vertex xyz so total area is same as group average", argstr="-r"
    )
    normal: bool = shell.arg(
        help="output is an ascii file where vertex data", argstr="-n"
    )
    xyz_ascii: bool = shell.arg(
        help="Print only surface xyz to ascii file", argstr="-a"
    )
    vertex: bool = shell.arg(
        help="Writes out neighbors of a vertex in each row", argstr="-v"
    )
    scale: float = shell.arg(help="scale vertex xyz by scale", argstr="-s {scale:.3}")
    dataarray_num: int = shell.arg(
        help="if input is gifti, 'num' specifies which data array to use",
        argstr="--da_num {dataarray_num}",
    )
    talairachxfm_subjid: ty.Any = shell.arg(
        help="apply talairach xfm of subject to vertex xyz",
        argstr="-t {talairachxfm_subjid}",
    )
    origname: ty.Any = shell.arg(help="read orig positions", argstr="-o {origname}")
    in_file: File = shell.arg(
        help="File to read/convert", argstr="{in_file}", position=-2
    )
    out_file: Path | None = shell.arg(
        help="output filename or True to generate one",
        position=-1,
        formatter="out_file_formatter",
    )
    out_datatype: ty.Any | None = shell.arg(
        help="These file formats are supported:  ASCII:       .ascICO: .ico, .tri GEO: .geo STL: .stl VTK: .vtk GIFTI: .gii MGH surface-encoded 'volume': .mgh, .mgz"
    )
    to_scanner: bool = shell.arg(
        help="convert coordinates from native FS (tkr) coords to scanner coords",
        argstr="--to-scanner",
    )
    to_tkr: bool = shell.arg(
        help="convert coordinates from scanner coords to native FS (tkr) coords",
        argstr="--to-tkr",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        converted: File | None = shell.out(
            help="converted output surface", callable=converted_callable
        )


def _gen_outfilename(
    annot_file=None,
    functional_file=None,
    in_file=None,
    label_file=None,
    out_datatype=None,
    out_file=None,
    parcstats_file=None,
    scalarcurv_file=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    if out_file is not attrs.NOTHING:
        return out_file
    elif annot_file is not attrs.NOTHING:
        _, name, ext = split_filename(annot_file)
    elif parcstats_file is not attrs.NOTHING:
        _, name, ext = split_filename(parcstats_file)
    elif label_file is not attrs.NOTHING:
        _, name, ext = split_filename(label_file)
    elif scalarcurv_file is not attrs.NOTHING:
        _, name, ext = split_filename(scalarcurv_file)
    elif functional_file is not attrs.NOTHING:
        _, name, ext = split_filename(functional_file)
    elif in_file is not attrs.NOTHING:
        _, name, ext = split_filename(in_file)

    return name + ext + "_converted." + out_datatype
