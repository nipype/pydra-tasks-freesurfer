from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.model.concatenate import Concatenate
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_concatenate_1():
    task = Concatenate()
    task.in_files = [Nifti1.sample(seed=0)]
    task.multiply_matrix_file = File.sample(seed=9)
    task.mask_file = File.sample(seed=14)
    task.subjects_dir = Directory.sample(seed=17)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_concatenate_2():
    task = Concatenate()
    task.in_files = [Nifti1.sample(seed=0)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
