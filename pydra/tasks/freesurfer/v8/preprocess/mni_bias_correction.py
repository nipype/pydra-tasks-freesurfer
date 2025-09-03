from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define
class MNIBiasCorrection(shell.Task["MNIBiasCorrection.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.mni_bias_correction import MNIBiasCorrection

    >>> task = MNIBiasCorrection()
    >>> task.in_file = MghGz.mock("norm.mgz")
    >>> task.protocol_iterations = 1000
    >>> task.mask = File.mock()
    >>> task.transform = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_nu_correct.mni"
    in_file: MghGz = shell.arg(
        help="input volume. Input can be any format accepted by mri_convert.",
        argstr="--i {in_file}",
    )
    iterations: int = shell.arg(
        help="Number of iterations to run nu_correct. Default is 4. This is the number of times that nu_correct is repeated (ie, using the output from the previous run as the input for the next). This is different than the -iterations option to nu_correct.",
        argstr="--n {iterations}",
        default=4,
    )
    protocol_iterations: int = shell.arg(
        help="Passes Np as argument of the -iterations flag of nu_correct. This is different than the --n flag above. Default is not to pass nu_correct the -iterations flag.",
        argstr="--proto-iters {protocol_iterations}",
    )
    distance: int = shell.arg(
        help="N3 -distance option", argstr="--distance {distance}"
    )
    no_rescale: bool = shell.arg(
        help="do not rescale so that global mean of output == input global mean",
        argstr="--no-rescale",
    )
    mask: File = shell.arg(
        help="brainmask volume. Input can be any format accepted by mri_convert.",
        argstr="--mask {mask}",
    )
    transform: File = shell.arg(
        help="tal.xfm. Use mri_make_uchar instead of conforming",
        argstr="--uchar {transform}",
    )
    stop: float = shell.arg(
        help="Convergence threshold below which iteration stops (suggest 0.01 to 0.0001)",
        argstr="--stop {stop}",
    )
    shrink: int = shell.arg(
        help="Shrink parameter for finer sampling (default is 4)",
        argstr="--shrink {shrink}",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="output volume. Output can be any format accepted by mri_convert. If the output format is COR, then the directory must exist.",
            argstr="--o {out_file}",
            path_template="{in_file}_output",
        )
