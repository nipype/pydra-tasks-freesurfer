from fileformats.generic import Directory
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.parse_dicom_dir import ParseDICOMDir
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_parsedicomdir_1():
    task = ParseDICOMDir()
    task.dicom_dir = Directory.sample(seed=0)
    task.dicom_info_file = "dicominfo.txt"
    task.subjects_dir = Directory.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_parsedicomdir_2():
    task = ParseDICOMDir()
    task.dicom_dir = "."
    task.summarize = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
