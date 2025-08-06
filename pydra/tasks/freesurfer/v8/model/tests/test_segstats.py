from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.model.seg_stats import SegStats
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_segstats_1():
    task = SegStats()
    task.segmentation_file = File.sample(seed=0)
    task.partial_volume_file = File.sample(seed=4)
    task.in_file = File.sample(seed=5)
    task.color_table_file = File.sample(seed=10)
    task.gca_color_table = File.sample(seed=12)
    task.mask_file = File.sample(seed=20)
    task.brainmask_file = File.sample(seed=27)
    task.in_intensity = File.sample(seed=38)
    task.subjects_dir = Directory.sample(seed=40)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_segstats_2():
    task = SegStats()
    task.annot = ("PWS04", "lh", "aparc")
    task.summary_file = "summary.stats"
    task.subjects_dir = "."
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
