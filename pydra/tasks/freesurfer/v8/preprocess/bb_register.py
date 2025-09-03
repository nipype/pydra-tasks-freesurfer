import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import fname_presuffix
import os.path as op
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name in (
        "registered_file",
        "out_fsl_file",
        "out_lta_file",
        "init_cost_file",
    ) and isinstance(value, bool):
        value = _list_outputs()[name]

    return argstr.format(**inputs)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    self_dict = {}

    outputs = {}
    _in = self_dict["inputs"]

    if _in.out_reg_file is not attrs.NOTHING:
        outputs["out_reg_file"] = op.abspath(_in.out_reg_file)
    elif _in.source_file:
        suffix = "_bbreg_%s.dat" % _in.subject_id
        outputs["out_reg_file"] = fname_presuffix(
            _in.source_file, suffix=suffix, use_ext=False
        )

    if _in.registered_file is not attrs.NOTHING:
        if isinstance(_in.registered_file, bool):
            outputs["registered_file"] = fname_presuffix(
                _in.source_file, suffix="_bbreg"
            )
        else:
            outputs["registered_file"] = op.abspath(_in.registered_file)

    if _in.out_lta_file is not attrs.NOTHING:
        if isinstance(_in.out_lta_file, bool):
            suffix = "_bbreg_%s.lta" % _in.subject_id
            out_lta_file = fname_presuffix(
                _in.source_file, suffix=suffix, use_ext=False
            )
            outputs["out_lta_file"] = out_lta_file
        else:
            outputs["out_lta_file"] = op.abspath(_in.out_lta_file)

    if _in.out_fsl_file is not attrs.NOTHING:
        if isinstance(_in.out_fsl_file, bool):
            suffix = "_bbreg_%s.mat" % _in.subject_id
            out_fsl_file = fname_presuffix(
                _in.source_file, suffix=suffix, use_ext=False
            )
            outputs["out_fsl_file"] = out_fsl_file
        else:
            outputs["out_fsl_file"] = op.abspath(_in.out_fsl_file)

    if _in.init_cost_file is not attrs.NOTHING:
        if isinstance(_in.out_fsl_file, bool):
            outputs["init_cost_file"] = outputs["out_reg_file"] + ".initcost"
        else:
            outputs["init_cost_file"] = op.abspath(_in.init_cost_file)

    outputs["min_cost_file"] = outputs["out_reg_file"] + ".mincost"
    return outputs


def out_fsl_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_fsl_file")


def out_lta_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_lta_file")


def min_cost_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("min_cost_file")


def init_cost_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("init_cost_file")


def registered_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("registered_file")


def _gen_filename(name, inputs):
    if name == "out_reg_file":
        return _list_outputs()[name]
    return None


def out_reg_file_default(inputs):
    return _gen_filename("out_reg_file", inputs=inputs)


@shell.define(xor=[["init", "init_reg_file"], ["reg_frame", "reg_middle_frame"]])
class BBRegister(shell.Task["BBRegister.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.bb_register import BBRegister

    >>> task = BBRegister()
    >>> task.init = "header"
    >>> task.init_reg_file = File.mock()
    >>> task.subject_id = "me"
    >>> task.source_file = Nifti1.mock("structural.nii")
    >>> task.contrast_type = "t2"
    >>> task.intermediate_file = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'bbregister --t2 --init-header --reg structural_bbreg_me.dat --mov structural.nii --s me'


    """

    executable = "bbregister"
    init: ty.Any | None = shell.arg(
        help="initialize registration with mri_coreg, spm, fsl, or header",
        argstr="--init-{init}",
    )
    init_reg_file: File | None = shell.arg(
        help="existing registration file", argstr="--init-reg {init_reg_file}"
    )
    subject_id: str = shell.arg(help="freesurfer subject id", argstr="--s {subject_id}")
    source_file: Nifti1 = shell.arg(
        help="source file to be registered", argstr="--mov {source_file}"
    )
    contrast_type: ty.Any = shell.arg(
        help="contrast type of image", argstr="--{contrast_type}"
    )
    intermediate_file: File = shell.arg(
        help="Intermediate image, e.g. in case of partial FOV",
        argstr="--int {intermediate_file}",
    )
    reg_frame: int | None = shell.arg(
        help="0-based frame index for 4D source file", argstr="--frame {reg_frame}"
    )
    reg_middle_frame: bool = shell.arg(
        help="Register middle frame of 4D source file", argstr="--mid-frame"
    )
    spm_nifti: bool = shell.arg(
        help="force use of nifti rather than analyze with SPM", argstr="--spm-nii"
    )
    epi_mask: bool = shell.arg(
        help="mask out B0 regions in stages 1 and 2", argstr="--epi-mask"
    )
    dof: ty.Any = shell.arg(
        help="number of transform degrees of freedom", argstr="--{dof}"
    )
    fsldof: int = shell.arg(
        help="degrees of freedom for initial registration (FSL)",
        argstr="--fsl-dof {fsldof}",
    )
    out_fsl_file: ty.Any = shell.arg(
        help="write the transformation matrix in FSL FLIRT format",
        argstr="--fslmat {out_fsl_file}",
    )
    out_lta_file: ty.Any = shell.arg(
        help="write the transformation matrix in LTA format",
        argstr="--lta {out_lta_file}",
    )
    registered_file: ty.Any = shell.arg(
        help="output warped sourcefile either True or filename",
        argstr="--o {registered_file}",
    )
    init_cost_file: ty.Any = shell.arg(
        help="output initial registration cost file",
        argstr="--initcost {init_cost_file}",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_reg_file: Path = shell.outarg(
            help="output registration file",
            argstr="--reg {out_reg_file}",
            path_template="out_reg_file",
        )
        out_fsl_file: File | None = shell.out(
            help="Output FLIRT-style registration file", callable=out_fsl_file_callable
        )
        out_lta_file: File | None = shell.out(
            help="Output LTA-style registration file", callable=out_lta_file_callable
        )
        min_cost_file: File | None = shell.out(
            help="Output registration minimum cost file",
            callable=min_cost_file_callable,
        )
        init_cost_file: File | None = shell.out(
            help="Output initial registration cost file",
            callable=init_cost_file_callable,
        )
        registered_file: File | None = shell.out(
            help="Registered and resampled source file",
            callable=registered_file_callable,
        )
