from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.tkregister_2 import Tkregister2
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_tkregister2_1():
    task = Tkregister2()
    task.target_image = File.sample(seed=0)
    task.moving_image = Nifti1.sample(seed=2)
    task.fsl_in_matrix = File.sample(seed=3)
    task.xfm = File.sample(seed=4)
    task.lta_in = File.sample(seed=5)
    task.noedit = True
    task.reg_file = "register.dat"
    task.subjects_dir = Directory.sample(seed=16)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tkregister2_2():
    task = Tkregister2()
    task.moving_image = Nifti1.sample(seed=2)
    task.reg_file = "T1_to_native.dat"
    task.reg_header = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_tkregister2_3():
    task = Tkregister2()
    task.moving_image = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
