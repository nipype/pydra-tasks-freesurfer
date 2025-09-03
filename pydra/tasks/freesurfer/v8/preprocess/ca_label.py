import attrs
from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.abspath(inputs["out_file"])
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


@shell.define
class CALabel(shell.Task["CALabel.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.ca_label import CALabel

    >>> task = CALabel()
    >>> task.in_file = MghGz.mock("norm.mgz")
    >>> task.transform = TextMatrix.mock("trans.mat")
    >>> task.template = File.mock()
    >>> task.in_vol = File.mock()
    >>> task.intensities = File.mock()
    >>> task.label = File.mock()
    >>> task.aseg = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_ca_label"
    in_file: MghGz = shell.arg(
        help="Input volume for CALabel", argstr="{in_file}", position=-4
    )
    out_file: Path = shell.arg(
        help="Output file for CALabel", argstr="{out_file}", position=-1
    )
    transform: TextMatrix = shell.arg(
        help="Input transform for CALabel", argstr="{transform}", position=-3
    )
    template: File = shell.arg(
        help="Input template for CALabel", argstr="{template}", position=-2
    )
    in_vol: File = shell.arg(help="set input volume", argstr="-r {in_vol}")
    intensities: File = shell.arg(
        help="input label intensities file(used in longitudinal processing)",
        argstr="-r {intensities}",
    )
    no_big_ventricles: bool = shell.arg(
        help="No big ventricles", argstr="-nobigventricles"
    )
    align: bool = shell.arg(help="Align CALabel", argstr="-align")
    prior: float = shell.arg(help="Prior for CALabel", argstr="-prior {prior:.1}")
    relabel_unlikely: ty.Any = shell.arg(
        help="Reclassify voxels at least some std devs from the mean using some size Gaussian window",
        argstr="-relabel_unlikely {relabel_unlikely[0]} {relabel_unlikely[1]:.1}",
    )
    label: File = shell.arg(
        help="Undocumented flag. Autorecon3 uses ../label/{hemisphere}.cortex.label as input file",
        argstr="-l {label}",
    )
    aseg: File = shell.arg(
        help="Undocumented flag. Autorecon3 uses ../mri/aseg.presurf.mgz as input file",
        argstr="-aseg {aseg}",
    )
    num_threads: int = shell.arg(help="allows for specifying more threads")
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="Output volume from CALabel", callable=out_file_callable
        )
