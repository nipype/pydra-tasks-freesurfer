from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Annot, White
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.contrast import Contrast
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_contrast_1():
    task = Contrast()
    task.subject_id = "subject_id"
    task.thickness = File.sample(seed=2)
    task.white = White.sample(seed=3)
    task.annotation = Annot.sample(seed=4)
    task.cortex = File.sample(seed=5)
    task.orig = File.sample(seed=6)
    task.rawavg = MghGz.sample(seed=7)
    task.subjects_dir = Directory.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_contrast_2():
    task = Contrast()
    task.subject_id = "10335"
    task.white = White.sample(seed=3)
    task.annotation = Annot.sample(seed=4)
    task.rawavg = MghGz.sample(seed=7)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
