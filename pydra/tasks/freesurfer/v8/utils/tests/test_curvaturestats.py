from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.curvature_stats import CurvatureStats
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_curvaturestats_1():
    task = CurvatureStats()
    task.surface = File.sample(seed=0)
    task.curvfile1 = File.sample(seed=1)
    task.curvfile2 = Pial.sample(seed=2)
    task.subject_id = "subject_id"
    task.subjects_dir = Directory.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_curvaturestats_2():
    task = CurvatureStats()
    task.curvfile2 = Pial.sample(seed=2)
    task.hemisphere = "lh"
    task.out_file = "lh.curv.stats"
    task.min_max = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
