from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.registration.mp_rto_mni305 import MPRtoMNI305
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mprtomni305_1():
    task = MPRtoMNI305()
    task.reference_dir = Directory.sample(seed=0)
    task.target = ""
    task.in_file = File.sample(seed=2)
    task.subjects_dir = Directory.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mprtomni305_2():
    task = MPRtoMNI305()
    task.target = "structural.nii"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
