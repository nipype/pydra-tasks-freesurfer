from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.segment_wm import SegmentWM
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_segmentwm_1():
    task = SegmentWM()
    task.in_file = MghGz.sample(seed=0)
    task.subjects_dir = Directory.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_segmentwm_2():
    task = SegmentWM()
    task.in_file = MghGz.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
