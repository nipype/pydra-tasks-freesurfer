import attrs
from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
import os
import os.path
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _format_arg(opt, val, inputs, argstr):
    if val is None:
        return ""

    if opt == "curv":
        return argstr

    return argstr.format(**inputs)


def curv_formatter(field, inputs):
    return _format_arg("curv", field, inputs, argstr="-curv")


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(in_surf=inputs["in_surf"], out_file=inputs["out_file"])[
            name
        ]
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class Register(shell.Task["Register.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.registration.register import Register

    >>> task = Register()
    >>> task.in_surf = Pial.mock("lh.pial")
    >>> task.target = File.mock()
    >>> task.in_sulc = Pial.mock("lh.pial")
    >>> task.out_file = "lh.pial.reg"
    >>> task.in_smoothwm = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_register"
    in_surf: Pial = shell.arg(
        help="Surface to register, often {hemi}.sphere",
        argstr="{in_surf}",
        position=-3,
        copy_mode="File.CopyMode.copy",
    )
    target: File = shell.arg(
        help="The data to register to. In normal recon-all usage, this is a template file for average surface.",
        argstr="{target}",
        position=-2,
    )
    in_sulc: Pial = shell.arg(
        help="Undocumented mandatory input file ${SUBJECTS_DIR}/surf/{hemisphere}.sulc ",
        copy_mode="File.CopyMode.copy",
    )
    curv: bool = shell.arg(
        help="Use smoothwm curvature for final alignment",
        requires=["in_smoothwm"],
        formatter="curv_formatter",
    )
    in_smoothwm: File = shell.arg(
        help="Undocumented input file ${SUBJECTS_DIR}/surf/{hemisphere}.smoothwm ",
        copy_mode="File.CopyMode.copy",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Output surface file to capture registration",
            argstr="{out_file}",
            position=-1,
            path_template='"lh.pial.reg"',
        )


def _list_outputs(in_surf=None, out_file=None):
    outputs = {}
    if out_file is not attrs.NOTHING:
        outputs["out_file"] = os.path.abspath(out_file)
    else:
        outputs["out_file"] = os.path.abspath(in_surf) + ".reg"
    return outputs
