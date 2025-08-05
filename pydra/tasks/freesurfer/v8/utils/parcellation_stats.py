import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial, White
import logging
import os
from pathlib import Path
from pathlib._local import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name in ["out_table", "out_color"]:
        return _list_outputs(
            out_table=inputs["out_table"],
            subject_id=inputs["subject_id"],
            surface=inputs["surface"],
            in_label=inputs["in_label"],
            out_color=inputs["out_color"],
            in_annotation=inputs["in_annotation"],
            subjects_dir=inputs["subjects_dir"],
            hemisphere=inputs["hemisphere"],
        )[name]
    return None


def out_color_default(inputs):
    return _gen_filename("out_color", inputs=inputs)


def out_table_default(inputs):
    return _gen_filename("out_table", inputs=inputs)


@shell.define(
    xor=[
        ["out_color", "in_annotatoin", "in_label"],
        ["in_annotation", "in_label"],
        ["out_color", "in_label"],
    ]
)
class ParcellationStats(shell.Task["ParcellationStats.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import MghGz
    >>> from fileformats.medimage_freesurfer import Pial, White
    >>> import os
    >>> from pathlib._local import Path
    >>> from pydra.tasks.freesurfer.v8.utils.parcellation_stats import ParcellationStats

    >>> task = ParcellationStats()
    >>> task.inputs.subject_id = "10335"
    >>> task.inputs.wm = MghGz.mock("./../mri/wm.mgz" # doctest: +SKIP)
    >>> task.inputs.lh_white = File.mock()
    >>> task.inputs.rh_white = White.mock("rh.white" # doctest: +SKIP)
    >>> task.inputs.lh_pial = File.mock()
    >>> task.inputs.rh_pial = Pial.mock("lh.pial" # doctest: +SKIP)
    >>> task.inputs.transform = File.mock()
    >>> task.inputs.thickness = File.mock()
    >>> task.inputs.brainmask = MghGz.mock("./../mri/brainmask.mgz" # doctest: +SKIP)
    >>> task.inputs.aseg = File.mock()
    >>> task.inputs.ribbon = MghGz.mock("./../mri/ribbon.mgz" # doctest: +SKIP)
    >>> task.inputs.cortex_label = File.mock()
    >>> task.inputs.surface = "white"
    >>> task.inputs.in_cortex = File.mock()
    >>> task.inputs.in_annotation = File.mock()
    >>> task.inputs.in_label = File.mock()
    >>> task.inputs.out_color = "test.ctab"
    >>> task.inputs.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_anatomical_stats"
    subject_id: ty.Any | None = shell.arg(
        help="Subject being processed",
        argstr="{subject_id}",
        position=-3,
        default="subject_id",
    )
    hemisphere: ty.Any = shell.arg(
        help="Hemisphere being processed", argstr="{hemisphere}", position=-2
    )
    wm: MghGz = shell.arg(help="Input file must be <subject_id>/mri/wm.mgz")
    lh_white: File = shell.arg(help="Input file must be <subject_id>/surf/lh.white")
    rh_white: White = shell.arg(help="Input file must be <subject_id>/surf/rh.white")
    lh_pial: File = shell.arg(help="Input file must be <subject_id>/surf/lh.pial")
    rh_pial: Pial = shell.arg(help="Input file must be <subject_id>/surf/rh.pial")
    transform: File = shell.arg(
        help="Input file must be <subject_id>/mri/transforms/talairach.xfm"
    )
    thickness: File = shell.arg(
        help="Input file must be <subject_id>/surf/?h.thickness"
    )
    brainmask: MghGz = shell.arg(
        help="Input file must be <subject_id>/mri/brainmask.mgz"
    )
    aseg: File = shell.arg(help="Input file must be <subject_id>/mri/aseg.presurf.mgz")
    ribbon: MghGz = shell.arg(help="Input file must be <subject_id>/mri/ribbon.mgz")
    cortex_label: File = shell.arg(help="implicit input file {hemi}.cortex.label")
    surface: ty.Any = shell.arg(
        help="Input surface (e.g. 'white')", argstr="{surface}", position=-1
    )
    mgz: bool = shell.arg(help="Look for mgz files", argstr="-mgz")
    in_cortex: File = shell.arg(help="Input cortex label", argstr="-cortex {in_cortex}")
    in_annotation: File | None = shell.arg(
        help="compute properties for each label in the annotation file separately",
        argstr="-a {in_annotation}",
    )
    in_label: File | None = shell.arg(
        help="limit calculations to specified label", argstr="-l {in_label}"
    )
    tabular_output: bool = shell.arg(help="Tabular output", argstr="-b")
    copy_inputs: bool = shell.arg(
        help="If running as a node, set this to True. This will copy the input files to the node directory."
    )
    th3: bool = shell.arg(
        help="turns on new vertex-wise volume calc for mris_anat_stats",
        argstr="-th3",
        requires=["cortex_label"],
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_table: Path = shell.outarg(
            help="Table output to tablefile",
            argstr="-f {out_table}",
            requires=["tabular_output"],
            path_template="out_table",
        )
        out_color: Path | None = shell.outarg(
            help="Output annotation files's colortable to text file",
            argstr="-c {out_color}",
            path_template='"test.ctab"',
        )


def _list_outputs(
    out_table=None,
    subject_id=None,
    surface=None,
    in_label=None,
    out_color=None,
    in_annotation=None,
    subjects_dir=None,
    hemisphere=None,
):
    outputs = {}
    if out_table is not attrs.NOTHING:
        outputs["out_table"] = os.path.abspath(out_table)
    else:

        stats_dir = os.path.join(subjects_dir, subject_id, "stats")
        if in_annotation is not attrs.NOTHING:

            if surface == "pial":
                basename = os.path.basename(in_annotation).replace(
                    ".annot", ".pial.stats"
                )
            else:
                basename = os.path.basename(in_annotation).replace(".annot", ".stats")
        elif in_label is not attrs.NOTHING:

            if surface == "pial":
                basename = os.path.basename(in_label).replace(".label", ".pial.stats")
            else:
                basename = os.path.basename(in_label).replace(".label", ".stats")
        else:
            basename = str(hemisphere) + ".aparc.annot.stats"
        outputs["out_table"] = os.path.join(stats_dir, basename)
    if out_color is not attrs.NOTHING:
        outputs["out_color"] = os.path.abspath(out_color)
    else:

        out_dir = os.path.join(subjects_dir, subject_id, "label")
        if in_annotation is not attrs.NOTHING:

            basename = os.path.basename(in_annotation)
            for item in ["lh.", "rh.", "aparc.", "annot"]:
                basename = basename.replace(item, "")
            annot = basename

            if "BA" in annot:
                outputs["out_color"] = os.path.join(out_dir, annot + "ctab")
            else:
                outputs["out_color"] = os.path.join(
                    out_dir, "aparc.annot." + annot + "ctab"
                )
        else:
            outputs["out_color"] = os.path.join(out_dir, "aparc.annot.ctab")
    return outputs
