import attrs
from fileformats.generic import Directory, File
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    if inputs["dicom_info_file"] is not attrs.NOTHING:
        outputs["dicom_info_file"] = os.path.join(
            os.getcwd(), inputs["dicom_info_file"]
        )
    return outputs


def dicom_info_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("dicom_info_file")


@shell.define
class ParseDICOMDir(shell.Task["ParseDICOMDir.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pathlib import Path
    >>> from pydra.tasks.freesurfer.v8.preprocess.parse_dicom_dir import ParseDICOMDir

    >>> task = ParseDICOMDir()
    >>> task.dicom_dir = Directory.mock(".")
    >>> task.summarize = True
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'mri_parse_sdcmdir --d . --o dicominfo.txt --sortbyrun --summarize'


    """

    executable = "mri_parse_sdcmdir"
    dicom_dir: Directory = shell.arg(
        help="path to siemens dicom directory", argstr="--d {dicom_dir}"
    )
    dicom_info_file: Path = shell.arg(
        help="file to which results are written",
        argstr="--o {dicom_info_file}",
        default="dicominfo.txt",
    )
    sortbyrun: bool = shell.arg(help="assign run numbers", argstr="--sortbyrun")
    summarize: bool = shell.arg(
        help="only print out info for run leaders", argstr="--summarize"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        dicom_info_file: File | None = shell.out(
            help="text file containing dicom information",
            callable=dicom_info_file_callable,
        )
