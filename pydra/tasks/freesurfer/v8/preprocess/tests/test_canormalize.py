from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.ca_normalize import CANormalize
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_canormalize_1():
    task = CANormalize()
    task.in_file = MghGz.sample(seed=0)
    task.atlas = File.sample(seed=2)
    task.transform = TextMatrix.sample(seed=3)
    task.mask = File.sample(seed=4)
    task.long_file = File.sample(seed=6)
    task.subjects_dir = Directory.sample(seed=7)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_canormalize_2():
    task = CANormalize()
    task.in_file = MghGz.sample(seed=0)
    task.transform = TextMatrix.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
