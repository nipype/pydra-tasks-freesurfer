from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.ca_register import CARegister
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_caregister_1():
    task = CARegister()
    task.in_file = MghGz.sample(seed=0)
    task.template = File.sample(seed=2)
    task.mask = File.sample(seed=3)
    task.transform = File.sample(seed=6)
    task.l_files = [File.sample(seed=10)]
    task.subjects_dir = Directory.sample(seed=12)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_caregister_2():
    task = CARegister()
    task.in_file = MghGz.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
