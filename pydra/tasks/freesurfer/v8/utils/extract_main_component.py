from fileformats.medimage_freesurfer import Pial
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define
class ExtractMainComponent(shell.Task["ExtractMainComponent.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.medimage_freesurfer import Pial
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.utils.extract_main_component import ExtractMainComponent

    >>> task = ExtractMainComponent()
    >>> task.in_file = Pial.mock("lh.pial")
    >>> task.cmdline
    'mris_extract_main_component lh.pial lh.maincmp'


    """

    executable = "mris_extract_main_component"
    in_file: Pial = shell.arg(help="input surface file", argstr="{in_file}", position=1)

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="surface containing main component",
            argstr="{out_file}",
            position=2,
            path_template="{in_file}.maincmp",
        )
