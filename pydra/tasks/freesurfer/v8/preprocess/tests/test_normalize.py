from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.normalize import Normalize
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_normalize_1():
    task = Normalize()
    task.in_file = MghGz.sample(seed=0)
    task.mask = File.sample(seed=3)
    task.segmentation = File.sample(seed=4)
    task.transform = File.sample(seed=5)
    task.subjects_dir = Directory.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_normalize_2():
    task = Normalize()
    task.in_file = MghGz.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
