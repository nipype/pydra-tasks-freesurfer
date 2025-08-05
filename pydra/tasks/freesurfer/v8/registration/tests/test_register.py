from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.registration.register import Register
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_register_1():
    task = Register()
    task.in_surf = Pial.sample(seed=0)
    task.target = File.sample(seed=1)
    task.in_sulc = Pial.sample(seed=2)
    task.in_smoothwm = File.sample(seed=5)
    task.subjects_dir = Directory.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_register_2():
    task = Register()
    task.in_surf = Pial.sample(seed=0)
    task.in_sulc = Pial.sample(seed=2)
    task.out_file = "lh.pial.reg"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
