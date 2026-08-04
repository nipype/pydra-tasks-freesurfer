import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
from fileformats.vendor.freesurfer.medimage import Dat, Label
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import fname_presuffix
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "vol_label_file":
        return _list_outputs(
            aparc_aseg=inputs["aparc_aseg"], vol_label_file=inputs["vol_label_file"]
        )[name]
    return None


def vol_label_file_default(inputs):
    return _gen_filename("vol_label_file", inputs=inputs)


@shell.define(
    xor=[
        ["annot_file", "aparc_aseg", "label_file", "seg_file"],
        ["identity", "reg_file", "reg_header"],
    ]
)
class Label2Vol(shell.Task["Label2Vol.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.vendor.freesurfer.medimage import Dat, Label
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.model.label_2_vol import Label2Vol

    >>> task = Label2Vol()
    >>> task.label_file = [Label.mock("c"), Label.mock("o"), Label.mock("r"), Label.mock("t"), Label.mock("e"), Label.mock("x"), Label.mock("."), Label.mock("l"), Label.mock("a"), Label.mock("b"), Label.mock("e"), Label.mock("l")]
    >>> task.annot_file = File.mock()
    >>> task.seg_file = File.mock()
    >>> task.template_file = Nifti1.mock("structural.nii")
    >>> task.reg_file = Dat.mock("register.dat")
    >>> task.reg_header = File.mock()
    >>> task.fill_thresh = 0.5
    >>> task.vol_label_file = "foo_out.nii"
    >>> task.label_hit_file = File.mock()
    >>> task.map_label_stat = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mri_label2vol"
    label_file: list[Label] | None = shell.arg(
        help="list of label files", default=None, argstr="--label {label_file}..."
    )
    annot_file: ty.Any | None = shell.arg(
        help="surface annotation file",
        argstr="--annot {annot_file}",
        requires=["subject_id", "hemi"],
        default=None,
    )
    seg_file: ty.Any = shell.arg(help="segmentation file", argstr="--seg {seg_file}")
    aparc_aseg: bool | None = shell.arg(
        help="use aparc+aseg.mgz in subjectdir as seg",
        argstr="--aparc+aseg",
        default=False,
    )
    template_file: ty.Any = shell.arg(
        help="output template volume", argstr="--temp {template_file}"
    )
    reg_file: ty.Any | None = shell.arg(
        help="tkregister style matrix VolXYZ = R*LabelXYZ",
        argstr="--reg {reg_file}",
        default=None,
    )
    reg_header: ty.Any = shell.arg(
        help="label template volume",
        argstr="--regheader {reg_header}",
        default=None,
    )
    identity: bool | None = shell.arg(
        help="set R=I",
        argstr="--identity",
        default=False,
    )
    invert_mtx: bool | None = shell.arg(
        help="Invert the registration matrix",
        argstr="--invertmtx",
        default=False,
    )
    fill_thresh: ty.Any | None = shell.arg(
        help="thresh : between 0 and 1",
        argstr="--fillthresh {fill_thresh}",
        default=None,
    )
    label_voxel_volume: float | None = shell.arg(
        help="volume of each label point (def 1mm3)",
        argstr="--labvoxvol {label_voxel_volume}",
        default=None,
    )
    proj: ty.Any | None = shell.arg(
        help="project along surface normal",
        default=None,
        argstr="--proj {proj[0]} {proj[1]} {proj[2]} {proj[3]}",
        requires=["subject_id", "hemi"],
    )
    subject_id: str | None = shell.arg(
        help="subject id",
        argstr="--subject {subject_id}",
        default=None,
    )
    hemi: ty.Any | None = shell.arg(
        help="hemisphere to use lh or rh",
        argstr="--hemi {hemi}",
        default=None,
    )
    surface: str | None = shell.arg(
        help="use surface instead of white",
        argstr="--surf {surface}",
        default=None,
    )
    label_hit_file: ty.Any | None = shell.arg(
        help="file with each frame is nhits for a label",
        default=None,
        argstr="--hits {label_hit_file}",
    )
    map_label_stat: ty.Any | None = shell.arg(
        help="map the label stats field into the vol",
        default=None,
        argstr="--label-stat {map_label_stat}",
    )
    native_vox2ras: bool | None = shell.arg(
        help="use native vox2ras xform instead of  tkregister-style",
        default=None,
        argstr="--native-vox2ras",
    )
    # subjects_dir: Directory | None = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        vol_label_file: File | bool = shell.outarg(
            help="output volume",
            argstr="--o {vol_label_file}",
            path_template="vol_label_file.nii.gz",
            default=True,
        )


def _list_outputs(aparc_aseg=None, vol_label_file=None):
    self_dict = {}
    outputs = {}
    outfile = vol_label_file
    if outfile is attrs.NOTHING:
        for key in ["label_file", "annot_file", "seg_file"]:
            if getattr(self_dict["inputs"], key) is not attrs.NOTHING:
                path = getattr(self_dict["inputs"], key)
                if isinstance(path, list):
                    path = path[0]
                _, src = os.path.split(path)
        if aparc_aseg is not attrs.NOTHING:
            src = "aparc+aseg.mgz"
        outfile = fname_presuffix(
            src, suffix="_vol.nii.gz", newpath=output_dir, use_ext=False
        )
    outputs["vol_label_file"] = outfile
    return outputs
