from fileformats.generic import Directory, File
import logging
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


@shell.define
class DICOMConvert(shell.Task["DICOMConvert.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.v8.preprocess.dicom_convert import DICOMConvert

    """

    executable = "mri_convert"
    dicom_dir: Directory = shell.arg(
        help="dicom directory from which to convert dicom files"
    )
    base_output_dir: Directory = shell.arg(
        help="directory in which subject directories are created"
    )
    subject_dir_template: str = shell.arg(
        help="template for subject directory name", default="S.%04d"
    )
    subject_id: ty.Any = shell.arg(help="subject identifier to insert into template")
    file_mapping: list[ty.Any] = shell.arg(
        help="defines the output fields of interface"
    )
    out_type: ty.Any = shell.arg(
        help="defines the type of output file produced", default="niigz"
    )
    dicom_info: File = shell.arg(
        help="File containing summary information from mri_parse_sdcmdir"
    )
    seq_list: list[str] = shell.arg(
        help="list of pulse sequence names to be converted.", requires=["dicom_info"]
    )
    ignore_single_slice: bool = shell.arg(
        help="ignore volumes containing a single slice", requires=["dicom_info"]
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        pass
