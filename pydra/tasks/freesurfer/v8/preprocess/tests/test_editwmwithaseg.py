from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.edit_w_mwith_aseg import EditWMwithAseg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_editwmwithaseg_1():
    task = EditWMwithAseg()
    task.in_file = MghGz.sample(seed=0)
    task.brain_file = File.sample(seed=1)
    task.seg_file = MghGz.sample(seed=2)
    task.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_editwmwithaseg_2():
    task = EditWMwithAseg()
    task.in_file = MghGz.sample(seed=0)
    task.seg_file = MghGz.sample(seed=2)
    task.keep_in = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
