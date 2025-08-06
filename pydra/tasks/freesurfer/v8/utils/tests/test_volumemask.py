from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.volume_mask import VolumeMask
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_volumemask_1():
    task = VolumeMask()
    task.lh_pial = Pial.sample(seed=4)
    task.rh_pial = File.sample(seed=5)
    task.lh_white = Pial.sample(seed=6)
    task.rh_white = File.sample(seed=7)
    task.aseg = File.sample(seed=8)
    task.subject_id = "subject_id"
    task.in_aseg = File.sample(seed=10)
    task.subjects_dir = Directory.sample(seed=13)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_volumemask_2():
    task = VolumeMask()
    task.left_whitelabel = 2
    task.right_whitelabel = 41
    task.lh_pial = Pial.sample(seed=4)
    task.lh_white = Pial.sample(seed=6)
    task.subject_id = "10335"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
