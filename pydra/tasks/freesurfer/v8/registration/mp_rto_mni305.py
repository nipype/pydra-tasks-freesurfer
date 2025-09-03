import attrs
from fileformats.generic import Directory, File
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import (
    copyfile,
    split_filename,
)
import os
import os.path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(opt, val, inputs, argstr):
    if val is None:
        return ""

    if opt in ["target", "reference_dir"]:
        return ""
    elif opt == "in_file":
        _, retval, ext = split_filename(val)

        copyfile(val, os.path.abspath(retval + ext), copy=True, hashmethod="content")
        return retval

    return argstr.format(**inputs)


def in_file_formatter(field, inputs):
    return _format_arg("in_file", field, inputs, argstr="{in_file}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["log_file"] = os.path.abspath("output.nipype")
    fullname = "_".join(
        [
            _get_fname(
                inputs["in_file"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            ),
            "to",
            inputs["target"],
            "t4",
            "vox2vox.txt",
        ]
    )
    outputs["out_file"] = os.path.abspath(fullname)
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


def log_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("log_file")


@shell.define
class MPRtoMNI305(shell.Task["MPRtoMNI305.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.v8.registration.mp_rto_mni305 import MPRtoMNI305

    >>> task = MPRtoMNI305()
    >>> task.reference_dir = Directory.mock()
    >>> task.target = "structural.nii"
    >>> task.in_file = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mpr2mni305"
    reference_dir: Directory | None = shell.arg(help="TODO", default="")
    target: ty.Any | None = shell.arg(help="input atlas file", default="")
    in_file: File = shell.arg(
        help="the input file prefix for MPRtoMNI305", formatter="in_file_formatter"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="The output file '<in_file>_to_<target>_t4_vox2vox.txt'",
            callable=out_file_callable,
        )
        log_file: File | None = shell.out(
            help="The output log", callable=log_file_callable
        )


def _get_fname(fname, inputs=None, output_dir=None, stderr=None, stdout=None):
    return split_filename(fname)[1]
