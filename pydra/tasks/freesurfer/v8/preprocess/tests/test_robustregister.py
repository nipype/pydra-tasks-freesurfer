from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.robust_register import RobustRegister
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_robustregister_1():
    task = RobustRegister()
    task.source_file = Nifti1.sample(seed=0)
    task.target_file = File.sample(seed=1)
    task.out_reg_file = True
    task.in_xfm_file = File.sample(seed=7)
    task.mask_source = File.sample(seed=25)
    task.mask_target = File.sample(seed=26)
    task.subjects_dir = Directory.sample(seed=29)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_robustregister_2():
    task = RobustRegister()
    task.source_file = Nifti1.sample(seed=0)
    task.auto_sens = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
