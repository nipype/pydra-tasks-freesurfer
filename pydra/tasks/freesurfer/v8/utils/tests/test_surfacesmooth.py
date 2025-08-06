from fileformats.generic import Directory
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.surface_smooth import SurfaceSmooth
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_surfacesmooth_1():
    task = SurfaceSmooth()
    task.in_file = MghGz.sample(seed=0)
    task.cortex = True
    task.subjects_dir = Directory.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_surfacesmooth_2():
    task = SurfaceSmooth()
    task.in_file = MghGz.sample(seed=0)
    task.hemi = "lh"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
