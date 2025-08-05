from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.mri_fill import MRIFill
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrifill_1():
    task = MRIFill()
    task.in_file = MghGz.sample(seed=0)
    task.segmentation = File.sample(seed=2)
    task.transform = File.sample(seed=3)
    task.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mrifill_2():
    task = MRIFill()
    task.in_file = MghGz.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
