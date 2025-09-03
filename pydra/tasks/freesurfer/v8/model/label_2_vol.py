import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
from fileformats.medimage_freesurfer import Dat, Label
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
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
    >>> from fileformats.medimage_freesurfer import Dat, Label
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
    label_file: list[Label] = shell.arg(
        help="list of label files", argstr="--label {label_file}..."
    )
    annot_file: File | None = shell.arg(
        help="surface annotation file",
        argstr="--annot {annot_file}",
        requires=("subject_id", "hemi"),
    )
    seg_file: File | None = shell.arg(
        help="segmentation file", argstr="--seg {seg_file}"
    )
    aparc_aseg: bool = shell.arg(
        help="use aparc+aseg.mgz in subjectdir as seg", argstr="--aparc+aseg"
    )
    template_file: Nifti1 = shell.arg(
        help="output template volume", argstr="--temp {template_file}"
    )
    reg_file: Dat | None = shell.arg(
        help="tkregister style matrix VolXYZ = R*LabelXYZ", argstr="--reg {reg_file}"
    )
    reg_header: File | None = shell.arg(
        help="label template volume", argstr="--regheader {reg_header}"
    )
    identity: bool = shell.arg(help="set R=I", argstr="--identity")
    invert_mtx: bool = shell.arg(
        help="Invert the registration matrix", argstr="--invertmtx"
    )
    fill_thresh: ty.Any = shell.arg(
        help="thresh : between 0 and 1", argstr="--fillthresh {fill_thresh}"
    )
    label_voxel_volume: float = shell.arg(
        help="volume of each label point (def 1mm3)",
        argstr="--labvoxvol {label_voxel_volume}",
    )
    proj: ty.Any = shell.arg(
        help="project along surface normal",
        argstr="--proj {proj[0]} {proj[1]} {proj[2]} {proj[3]}",
        requires=("subject_id", "hemi"),
    )
    subject_id: str = shell.arg(help="subject id", argstr="--subject {subject_id}")
    hemi: ty.Any = shell.arg(help="hemisphere to use lh or rh", argstr="--hemi {hemi}")
    surface: str = shell.arg(
        help="use surface instead of white", argstr="--surf {surface}"
    )
    label_hit_file: File = shell.arg(
        help="file with each frame is nhits for a label",
        argstr="--hits {label_hit_file}",
    )
    map_label_stat: File = shell.arg(
        help="map the label stats field into the vol",
        argstr="--label-stat {map_label_stat}",
    )
    native_vox2ras: bool = shell.arg(
        help="use native vox2ras xform instead of  tkregister-style",
        argstr="--native-vox2ras",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        vol_label_file: Path = shell.outarg(
            help="output volume",
            argstr="--o {vol_label_file}",
            path_template='"foo_out.nii"',
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
