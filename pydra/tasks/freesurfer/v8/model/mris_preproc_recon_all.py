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


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "surfreg_files":
        basename = os.path.basename(value[0])
        return argstr.format(**{name: basename.lstrip("rh.").lstrip("lh.")})
    if name == "surf_measure_file":
        basename = os.path.basename(value)
        return argstr.format(**{name: basename.lstrip("rh.").lstrip("lh.")})

    return argstr.format(**inputs)


def surfreg_files_formatter(field, inputs):
    return _format_arg(
        "surfreg_files", field, inputs, argstr="--surfreg {surfreg_files}"
    )


def surf_measure_file_formatter(field, inputs):
    return _format_arg(
        "surf_measure_file", field, inputs, argstr="--meas {surf_measure_file}"
    )


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
        ["fsgd_file", "subject_file", "subject_id", "subjects"],
        ["fsgd_file", "subject_file", "subjects"],
        ["fwhm", "num_iters"],
        ["fwhm_source", "num_iters_source"],
        ["surf_area", "surf_measure", "surf_measure_file"],
    ]
)
class MRISPreprocReconAll(shell.Task["MRISPreprocReconAll.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.model.mris_preproc_recon_all import MRISPreprocReconAll
    >>> from pydra.utils.typing import MultiInputObj

    >>> task = MRISPreprocReconAll()
    >>> task.surf_measure_file = File.mock()
    >>> task.lh_surfreg_target = File.mock()
    >>> task.rh_surfreg_target = File.mock()
    >>> task.target = "fsaverage"
    >>> task.fsgd_file = File.mock()
    >>> task.subject_file = File.mock()
    >>> task.vol_measure_file = [("cont1.nii", "register.dat"),                                            ("cont1a.nii", "register.dat")]
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mris_preproc"
    surf_measure_file: File | None = shell.arg(
        help="file necessary for surfmeas", formatter="surf_measure_file_formatter"
    )
    surfreg_files: list[File] = shell.arg(
        help="lh and rh input surface registration files",
        requires=["lh_surfreg_target", "rh_surfreg_target"],
        formatter="surfreg_files_formatter",
    )
    lh_surfreg_target: File | None = shell.arg(
        help="Implicit target surface registration file", requires=["surfreg_files"]
    )
    rh_surfreg_target: File | None = shell.arg(
        help="Implicit target surface registration file", requires=["surfreg_files"]
    )
    subject_id: ty.Any | None = shell.arg(
        help="subject from whom measures are calculated",
        argstr="--s {subject_id}",
        default="subject_id",
    )
    copy_inputs: bool = shell.arg(
        help="If running as a node, set this to True this will copy some implicit inputs to the node directory."
    )
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
