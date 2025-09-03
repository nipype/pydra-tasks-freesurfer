import glob
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import (
    ensure_list,
    simplify_list,
)
import os
from pydra.compose import python
from pydra.utils.typing import MultiOutputFile
from fileformats.generic import Directory, File


logger = logging.getLogger(__name__)


def _get_files(inputs, path, key, dirval, altkey=None):

    globsuffix = ""
    if dirval == "mri":
        globsuffix = ".mgz"
    elif dirval == "stats":
        globsuffix = ".stats"
    globprefix = ""
    if dirval in ("surf", "label", "stats"):
        if inputs["hemi"] != "both":
            globprefix: inputs = python.arg["hemi"] + "."
        else:
            globprefix = "?h."
        if key in ("aseg_stats", "wmparc_stats"):
            globprefix = ""
    elif key == "ribbon":
        if inputs["hemi"] != "both":
            globprefix: inputs = python.arg["hemi"] + "."
        else:
            globprefix = "*"
    keys = ensure_list(altkey) if altkey else [key]
    globfmt = os.path.join(path, dirval, f"{globprefix}{{}}{globsuffix}")
    return [os.path.abspath(f) for key in keys for f in glob.glob(globfmt.format(key))]


def _list_outputs(inputs):

    subjects_dir = inputs["subjects_dir"]
    subject_path = os.path.join(subjects_dir, inputs["subject_id"])
    output_traits = {}
    outputs = output_traits.get()
    for k in list(outputs.keys()):
        val: _get_files = python.arg(
            inputs,
            subject_path,
            k,
            output_traits.traits()[k].loc,
            output_traits.traits()[k].altkey,
        )
        if val:
            outputs[k] = simplify_list(val)
    return outputs


@python.define
class FreeSurferSource(python.Task["FreeSurferSource.Outputs"]):
    """Generates freesurfer subject info from their directories.

    Examples
    --------
    >>> from nipype.interfaces.io import FreeSurferSource
    >>> fs = FreeSurferSource()
    >>> #fs.inputs.subjects_dir = '.'
    >>> fs.inputs.subject_id = 'PWS04'
    >>> res = fs.run() # doctest: +SKIP

    >>> fs.inputs.hemi = 'lh'
    >>> res = fs.run() # doctest: +SKIP

    """

    subjects_dir: Directory = python.arg(help="Freesurfer subjects directory.")
    subject_id: str = python.arg(help="Subject name for whom to retrieve data")
    hemi: str = python.arg(
        allowed_values=["both", "lh", "rh"], help="Selects hemisphere specific outputs"
    )

    class Outputs(python.Outputs):
        T1: File = python.arg(
            help="Intensity normalized whole-head volume",
            # loc="mri"
        )
        aseg: File = python.arg(
            #  loc=(.*)
            help="Volumetric map of regions from automatic segmentation",
        )
        brain: File = python.arg(
            help="Intensity normalized brain-only volume",
            # loc="mri"
        )
        brainmask: File = python.arg(
            help="Skull-stripped (brain-only) volume",
            # loc="mri"
        )
        filled: File = python.arg(
            help="Subcortical mass volume",
            # loc="mri"
        )
        norm: File = python.arg(
            help="Normalized skull-stripped volume",
            # loc="mri"
        )
        nu: File = python.arg(
            help="Non-uniformity corrected whole-head volume",
            # loc="mri"
        )
        orig: File = python.arg(
            help="Base image conformed to Freesurfer space",
            # loc="mri"
        )
        rawavg: File = python.arg(
            help="Volume formed by averaging input images",
            # loc="mri"
        )
        ribbon: MultiOutputFile = python.arg(
            help="Volumetric maps of cortical ribbons",
            #  loc=(.*)
            # altkey="*ribbon",
        )
        wm: File = python.arg(
            help="Segmented white-matter volume",
            # loc="mri"
        )
        wmparc: File = python.arg(
            #  loc=(.*)
            help="Aparc parcellation projected into subcortical white matter",
        )
        curv: MultiOutputFile = python.arg(
            help="Maps of surface curvature",
            # loc="surf"
        )
        avg_curv: MultiOutputFile = python.arg(
            help="Average atlas curvature, sampled to subject",
            #  loc=(.*)
        )
        inflated: MultiOutputFile = python.arg(
            help="Inflated surface meshes",
            # loc="surf"
        )
        pial: MultiOutputFile = python.arg(
            help="Gray matter/pia matter surface meshes",
            # loc="surf"
        )
        area_pial: MultiOutputFile = python.arg(
            help="Mean area of triangles each vertex on the pial surface is "
            "associated with",
            #  loc=(.*)
            # altkey="area.pial",
        )
        curv_pial: MultiOutputFile = python.arg(
            help="Curvature of pial surface",
            #  loc=(.*)
            # altkey="curv.pial",
        )
        smoothwm: MultiOutputFile = python.arg(
            #  loc=(.*)
        )
        sphere: MultiOutputFile = python.arg(
            help="Spherical surface meshes",
            # loc="surf"
        )
        sulc: MultiOutputFile = python.arg(
            help="Surface maps of sulcal depth",
            # loc="surf"
        )
        thickness: MultiOutputFile = python.arg(
            #  loc=(.*)
        )
        volume: MultiOutputFile = python.arg(
            help="Surface maps of cortical volume",
            # loc="surf"
        )
        white: MultiOutputFile = python.arg(
            help="White/gray matter surface meshes",
            # loc="surf"
        )
        jacobian_white: MultiOutputFile = python.arg(
            help="Distortion required to register to spherical atlas",
            #  loc=(.*)
        )
        graymid: MultiOutputFile = python.arg(
            help="Graymid/midthickness surface meshes",
            #  loc=(.*)
            # altkey=["graymid", "midthickness"],
        )
        label: MultiOutputFile = python.arg(
            help="Volume and surface label files",
            #  loc=(.*)
            # altkey="*label",
        )
        annot: MultiOutputFile = python.arg(
            help="Surface annotation files",
            #  loc=(.*)
            # altkey="*annot",
        )
        aparc_aseg: MultiOutputFile = python.arg(
            #  loc=(.*)
            # altkey="aparc*aseg",
            help="Aparc parcellation projected into aseg volume",
        )
        sphere_reg: MultiOutputFile = python.arg(
            #  loc=(.*)
            # altkey="sphere.reg",
            help="Spherical registration file",
        )
        aseg_stats: MultiOutputFile = python.arg(
            #  loc=(.*)
            #  altkey="aseg",
            help="Automated segmentation statistics file",
        )
        wmparc_stats: MultiOutputFile = python.arg(
            #  loc=(.*)
            #  altkey="wmparc",
            help="White matter parcellation statistics file",
        )
        aparc_stats: MultiOutputFile = python.arg(
            #  loc=(.*)
            #  altkey="aparc",
            help="Aparc parcellation statistics files",
        )
        BA_stats: MultiOutputFile = python.arg(
            #  loc=(.*)
            #  altkey="BA",
            help="Brodmann Area statistics files",
        )
        aparc_a2009s_stats: MultiOutputFile = python.arg(
            #  loc=(.*)
            # altkey="aparc.a2009s",
            help="Aparc a2009s parcellation statistics files",
        )
        curv_stats: MultiOutputFile = python.arg(
            #  loc=(.*)
            #  altkey="curv",
            help="Curvature statistics files",
        )
        entorhinal_exvivo_stats: MultiOutputFile = python.arg(
            #  loc=(.*)
            #  altkey="entorhinal_exvivo",
            help="Entorhinal exvivo statistics files",
        )

    @staticmethod
    def function():
        raise NotImplementedError(
            "FreeSurferSource does not implement a function, "
            "it is used to generate outputs from the subject directory."
        )
