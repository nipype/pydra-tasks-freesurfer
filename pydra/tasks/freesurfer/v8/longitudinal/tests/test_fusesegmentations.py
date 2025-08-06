from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.longitudinal.fuse_segmentations import FuseSegmentations
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fusesegmentations_1():
    task = FuseSegmentations()
    task.in_segmentations = [File.sample(seed=3)]
    task.in_segmentations_noCC = [MghGz.sample(seed=4)]
    task.in_norms = [File.sample(seed=5)]
    task.subjects_dir = Directory.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fusesegmentations_2():
    task = FuseSegmentations()
    task.subject_id = "tp.long.A.template"
    task.out_file = "aseg.fused.mgz"
    task.in_segmentations_noCC = [MghGz.sample(seed=4)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
