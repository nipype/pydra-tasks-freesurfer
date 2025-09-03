import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "in_files":
        cmd = ""
        for i, file in enumerate(value):
            if inputs["tr_list"] is not attrs.NOTHING:
                cmd = " ".join((cmd, "-tr %.1f" % inputs["tr_list"][i]))
            if inputs["te_list"] is not attrs.NOTHING:
                cmd = " ".join((cmd, "-te %.3f" % inputs["te_list"][i]))
            if inputs["flip_list"] is not attrs.NOTHING:
                cmd = " ".join((cmd, "-fa %.1f" % inputs["flip_list"][i]))
            if inputs["xfm_list"] is not attrs.NOTHING:
                cmd = " ".join((cmd, "-at %s" % inputs["xfm_list"][i]))
            cmd = f"{cmd} {file}"
        return cmd

    return argstr.format(**inputs)


def in_files_formatter(field, inputs):
    return _format_arg("in_files", field, inputs, argstr="{in_files}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    if inputs["out_dir"] is attrs.NOTHING:
        out_dir = _gen_filename(
            "out_dir",
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    else:
        out_dir = inputs["out_dir"]
    outputs["t1_image"] = os.path.join(out_dir, "T1.mgz")
    outputs["pd_image"] = os.path.join(out_dir, "PD.mgz")
    outputs["t2star_image"] = os.path.join(out_dir, "T2star.mgz")
    return outputs


def t1_image_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("t1_image")


def pd_image_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("pd_image")


def t2star_image_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("t2star_image")


def _gen_filename(name, inputs):
    if name == "out_dir":
        return os.getcwd()
    return None


def out_dir_default(inputs):
    return _gen_filename("out_dir", inputs=inputs)


@shell.define
class FitMSParams(shell.Task["FitMSParams.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from pydra.tasks.freesurfer.v8.preprocess.fit_ms_params import FitMSParams

    >>> task = FitMSParams()
    >>> task.in_files = [MghGz.mock("flash_05.mgz"), MghGz.mock("flash_30.mgz")]
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_ms_fitparms"
    in_files: list[MghGz] = shell.arg(
        help="list of FLASH images (must be in mgh format)",
        position=-2,
        formatter="in_files_formatter",
    )
    tr_list: list[int] = shell.arg(help="list of TRs of the input files (in msec)")
    te_list: list[float] = shell.arg(help="list of TEs of the input files (in msec)")
    flip_list: list[int] = shell.arg(help="list of flip angles of the input files")
    xfm_list: list[File] = shell.arg(
        help="list of transform files to apply to each FLASH image"
    )
    out_dir: ty.Any = shell.arg(
        help="directory to store output in", argstr="{out_dir}", position=-1
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        t1_image: File | None = shell.out(
            help="image of estimated T1 relaxation values", callable=t1_image_callable
        )
        pd_image: File | None = shell.out(
            help="image of estimated proton density values", callable=pd_image_callable
        )
        t2star_image: File | None = shell.out(
            help="image of estimated T2* values", callable=t2star_image_callable
        )
