from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.segment_cc import SegmentCC
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_segmentcc_1():
    task = SegmentCC()
    task.in_file = MghGz.sample(seed=0)
    task.in_norm = File.sample(seed=1)
    task.subject_id = "subject_id"
    task.subjects_dir = Directory.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_segmentcc_2():
    task = SegmentCC()
    task.in_file = MghGz.sample(seed=0)
    task.out_rotation = "cc.lta"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
