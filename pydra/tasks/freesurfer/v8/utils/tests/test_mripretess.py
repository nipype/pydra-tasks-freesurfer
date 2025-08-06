from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.mri_pretess import MRIPretess
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mripretess_1():
    task = MRIPretess()
    task.in_filled = MghGz.sample(seed=0)
    task.label = "wm"
    task.in_norm = File.sample(seed=2)
    task.subjects_dir = Directory.sample(seed=7)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mripretess_2():
    task = MRIPretess()
    task.in_filled = MghGz.sample(seed=0)
    task.nocorners = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
