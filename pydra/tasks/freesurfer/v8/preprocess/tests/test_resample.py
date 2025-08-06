from fileformats.generic import Directory
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.resample import Resample
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_resample_1():
    task = Resample()
    task.in_file = Nifti1.sample(seed=0)
    task.subjects_dir = Directory.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_resample_2():
    task = Resample()
    task.in_file = Nifti1.sample(seed=0)
    task.voxel_size = (2.1, 2.1, 2.1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
