import attrs
from fileformats.generic import Directory, File
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
from pydra.utils.typing import MultiInputObj
import typing as ty


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            hemi=inputs["hemi"], out_file=inputs["out_file"], target=inputs["target"]
        )[name]
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define(
    xor=[
        ["fsgd_file", "subject_file", "subjects"],
        ["fwhm", "num_iters"],
        ["fwhm_source", "num_iters_source"],
        ["surf_area", "surf_measure", "surf_measure_file"],
    ]
)
class MRISPreproc(shell.Task["MRISPreproc.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.model.mris_preproc import MRISPreproc
    >>> from pydra.utils.typing import MultiInputObj

    >>> task = MRISPreproc()
    >>> task.target = "fsaverage"
    >>> task.fsgd_file = File.mock()
    >>> task.subject_file = File.mock()
    >>> task.vol_measure_file = [("cont1.nii", "register.dat"),                                            ("cont1a.nii", "register.dat")]
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_preproc"
    target: str = shell.arg(help="target subject name", argstr="--target {target}")
    hemi: ty.Any = shell.arg(
        help="hemisphere for source and target", argstr="--hemi {hemi}"
    )
    surf_measure: str = shell.arg(
        help="Use subject/surf/hemi.surf_measure as input",
        argstr="--meas {surf_measure}",
    )
    surf_area: str = shell.arg(
        help="Extract vertex area from subject/surf/hemi.surfname to use as input.",
        argstr="--area {surf_area}",
    )
    subjects: list[ty.Any] = shell.arg(
        help="subjects from who measures are calculated", argstr="--s {subjects}..."
    )
    fsgd_file: File | None = shell.arg(
        help="specify subjects using fsgd file", argstr="--fsgd {fsgd_file}"
    )
    subject_file: File | None = shell.arg(
        help="file specifying subjects separated by white space",
        argstr="--f {subject_file}",
    )
    surf_measure_file: list[File] = shell.arg(
        help="file alternative to surfmeas, still requires list of subjects",
        argstr="--is {surf_measure_file}...",
    )
    source_format: str = shell.arg(
        help="source format", argstr="--srcfmt {source_format}"
    )
    surf_dir: str = shell.arg(
        help="alternative directory (instead of surf)", argstr="--surfdir {surf_dir}"
    )
    vol_measure_file: MultiInputObj = shell.arg(
        help="list of volume measure and reg file tuples",
        argstr="--iv {vol_measure_file[0]} {vol_measure_file[1]}...",
    )
    proj_frac: float = shell.arg(
        help="projection fraction for vol2surf", argstr="--projfrac {proj_frac}"
    )
    fwhm: float | None = shell.arg(
        help="smooth by fwhm mm on the target surface", argstr="--fwhm {fwhm}"
    )
    num_iters: int | None = shell.arg(
        help="niters : smooth by niters on the target surface",
        argstr="--niters {num_iters}",
    )
    fwhm_source: float | None = shell.arg(
        help="smooth by fwhm mm on the source surface",
        argstr="--fwhm-src {fwhm_source}",
    )
    num_iters_source: int | None = shell.arg(
        help="niters : smooth by niters on the source surface",
        argstr="--niterssrc {num_iters_source}",
    )
    smooth_cortex_only: bool = shell.arg(
        help="only smooth cortex (ie, exclude medial wall)",
        argstr="--smooth-cortex-only",
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="output filename", argstr="--out {out_file}", path_template="out_file"
        )


def _list_outputs(hemi=None, out_file=None, target=None):
    outputs = {}
    outfile = out_file
    outputs["out_file"] = outfile
    if outfile is attrs.NOTHING:
        outputs["out_file"] = os.path.join(output_dir, f"concat_{hemi}_{target}.mgz")
    return outputs
