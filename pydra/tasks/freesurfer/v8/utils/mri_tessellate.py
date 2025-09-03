import attrs
from fileformats.generic import Directory, File
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import split_filename
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["surface"] = os.path.abspath(
        _gen_outfilename(
            in_file=inputs["in_file"],
            label_value=inputs["label_value"],
            out_file=inputs["out_file"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    )
    return outputs


def surface_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("surface")


def _gen_filename(name, inputs):
    if name == "out_file":
        return _gen_outfilename(
            in_file=inputs["in_file"],
            label_value=inputs["label_value"],
            out_file=inputs["out_file"],
        )
    else:
        return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class MRITessellate(shell.Task["MRITessellate.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.mri_tessellate import MRITessellate

    """

    executable = "mri_tessellate"
    in_file: File = shell.arg(
        help="Input volume to tessellate voxels from.", argstr="{in_file}", position=-3
    )
    label_value: int = shell.arg(
        help='Label value which to tessellate from the input volume. (integer, if input is "filled.mgz" volume, 127 is rh, 255 is lh)',
        argstr="{label_value}",
        position=-2,
    )
    out_file: Path = shell.arg(
        help="output filename or True to generate one", argstr="{out_file}", position=-1
    )
    tesselate_all_voxels: bool = shell.arg(
        help="Tessellate the surface of all voxels with different labels", argstr="-a"
    )
    use_real_RAS_coordinates: bool = shell.arg(
        help="Saves surface with real RAS coordinates where c_(r,a,s) != 0", argstr="-n"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        surface: File | None = shell.out(
            help="binary surface of the tessellation ", callable=surface_callable
        )


def _gen_outfilename(
    in_file=None,
    label_value=None,
    out_file=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    if out_file is not attrs.NOTHING:
        return out_file
    else:
        _, name, ext = split_filename(in_file)
        return name + ext + "_" + str(label_value)
