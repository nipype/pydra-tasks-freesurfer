from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.registration.em_register import EMRegister
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_emregister_1():
    task = EMRegister()
    task.in_file = MghGz.sample(seed=0)
    task.template = File.sample(seed=1)
    task.mask = File.sample(seed=4)
    task.transform = File.sample(seed=6)
    task.subjects_dir = Directory.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_emregister_2():
    task = EMRegister()
    task.in_file = MghGz.sample(seed=0)
    task.out_file = "norm_transform.lta"
    task.nbrspacing = 9
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
