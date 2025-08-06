from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.bb_register import BBRegister
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_bbregister_1():
    task = BBRegister()
    task.init_reg_file = File.sample(seed=1)
    task.source_file = Nifti1.sample(seed=3)
    task.intermediate_file = File.sample(seed=5)
    task.subjects_dir = Directory.sample(seed=17)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_bbregister_2():
    task = BBRegister()
    task.init = "header"
    task.subject_id = "me"
    task.source_file = Nifti1.sample(seed=3)
    task.contrast_type = "t2"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
