from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.dicom_convert import DICOMConvert
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_dicomconvert_1():
    task = DICOMConvert()
    task.dicom_dir = Directory.sample(seed=0)
    task.base_output_dir = Directory.sample(seed=1)
    task.subject_dir_template = "S.%04d"
    task.out_type = "niigz"
    task.dicom_info = File.sample(seed=6)
    task.subjects_dir = Directory.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
