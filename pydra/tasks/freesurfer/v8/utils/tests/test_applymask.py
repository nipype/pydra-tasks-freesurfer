from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.apply_mask import ApplyMask
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applymask_1():
    task = ApplyMask()
    task.in_file = File.sample(seed=0)
    task.mask_file = File.sample(seed=1)
    task.xfm_file = File.sample(seed=3)
    task.xfm_source = File.sample(seed=5)
    task.xfm_target = File.sample(seed=6)
    task.subjects_dir = Directory.sample(seed=11)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
