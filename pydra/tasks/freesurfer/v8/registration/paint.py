import attrs
from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _format_arg(opt, val, inputs, argstr):
    if val is None:
        return ""

    if opt == "template":
        if inputs["template_param"] is not attrs.NOTHING:
            return argstr % (val + "#" + str(inputs["template_param"]))

    return argstr.format(**inputs)


def template_formatter(field, inputs):
    return _format_arg("template", field, inputs, argstr="{template}")


@shell.define
class Paint(shell.Task["Paint.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.registration.paint import Paint

    >>> task = Paint()
    >>> task.inputs.in_surf = Pial.mock("lh.pial")
    >>> task.inputs.template = File.mock()
    >>> task.inputs.averages = 5
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mrisp_paint"
    in_surf: Pial = shell.arg(
        help="Surface file with grid (vertices) onto which the template data is to be sampled or 'painted'",
        argstr="{in_surf}",
        position=-2,
    )
    template: File = shell.arg(
        help="Template file", position=-3, formatter="template_formatter"
    )
    template_param: int = shell.arg(help="Frame number of the input template")
    averages: int = shell.arg(help="Average curvature patterns", argstr="-a {averages}")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="File containing a surface-worth of per-vertex values, saved in 'curvature' format.",
            argstr="{out_file}",
            position=-1,
            path_template="{in_surf}.avg_curv",
        )
