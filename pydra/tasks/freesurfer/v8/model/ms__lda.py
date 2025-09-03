import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.text import TextFile
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "use_weights":
        if inputs["use_weights"] is True:
            _verify_weights_file_exists(weight_file=inputs["weight_file"])
        else:
            return ""

    return argstr.format(**inputs)


def use_weights_formatter(field, inputs):
    return _format_arg("use_weights", field, inputs, argstr="-W")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    if inputs["output_synth"] is not attrs.NOTHING:
        outputs["vol_synth_file"] = os.path.abspath(inputs["output_synth"])
    else:
        outputs["vol_synth_file"] = os.path.abspath(inputs["vol_synth_file"])
    if (inputs["use_weights"] is attrs.NOTHING) or inputs["use_weights"] is False:
        outputs["weight_file"] = os.path.abspath(inputs["weight_file"])
    return outputs


def weight_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("weight_file")


def vol_synth_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("vol_synth_file")


def _gen_filename(name, inputs):
    pass


@shell.define
class MS_LDA(shell.Task["MS_LDA.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.text import TextFile
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.model.ms__lda import MS_LDA

    >>> task = MS_LDA()
    >>> task.lda_labels = [grey_label, white_label]
    >>> task.weight_file = "weights.txt"
    >>> task.vol_synth_file = "synth_out.mgz"
    >>> task.label_file = MghGz.mock("label.mgz")
    >>> task.mask_file = File.mock()
    >>> task.shift = zero_value
    >>> task.conform = True
    >>> task.use_weights = True
    >>> task.images = [MghGz.mock("FLASH1.mgz"), MghGz.mock("FLASH2.mgz"), MghGz.mock("FLASH3.mgz")]
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_ms_LDA"
    lda_labels: list[int] = shell.arg(
        help="pair of class labels to optimize", argstr="-lda {lda_labels}", sep=" "
    )
    weight_file: Path = shell.arg(
        help="filename for the LDA weights (input or output)",
        argstr="-weight {weight_file}",
    )
    vol_synth_file: Path = shell.arg(
        help="filename for the synthesized output volume",
        argstr="-synth {vol_synth_file}",
    )
    label_file: MghGz = shell.arg(
        help="filename of the label volume", argstr="-label {label_file}"
    )
    mask_file: File = shell.arg(
        help="filename of the brain mask volume", argstr="-mask {mask_file}"
    )
    shift: int = shell.arg(
        help="shift all values equal to the given value to zero",
        argstr="-shift {shift}",
    )
    conform: bool = shell.arg(
        help="Conform the input volumes (brain mask typically already conformed)",
        argstr="-conform",
    )
    use_weights: bool = shell.arg(
        help="Use the weights from a previously generated weight file",
        formatter="use_weights_formatter",
    )
    images: list[MghGz] = shell.arg(
        help="list of input FLASH images", argstr="{images}", position=-1
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        weight_file: TextFile | None = shell.out(callable=weight_file_callable)
        vol_synth_file: MghGz | None = shell.out(callable=vol_synth_file_callable)


def _verify_weights_file_exists(weight_file=None):
    if not os.path.exists(os.path.abspath(weight_file)):
        raise traits.KeyError(
            "MS_LDA: use_weights must accompany an existing weights file"
        )
