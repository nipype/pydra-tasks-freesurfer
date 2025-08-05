from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.make_surfaces import MakeSurfaces
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_makesurfaces_1():
    task = MakeSurfaces()
    task.subject_id = "subject_id"
    task.in_orig = Pial.sample(seed=2)
    task.in_wm = File.sample(seed=3)
    task.in_filled = MghGz.sample(seed=4)
    task.in_white = File.sample(seed=5)
    task.in_label = File.sample(seed=6)
    task.orig_white = File.sample(seed=7)
    task.orig_pial = File.sample(seed=8)
    task.in_aseg = File.sample(seed=12)
    task.in_T1 = MghGz.sample(seed=13)
    task.subjects_dir = Directory.sample(seed=20)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_makesurfaces_2():
    task = MakeSurfaces()
    task.hemisphere = "lh"
    task.in_orig = Pial.sample(seed=2)
    task.in_filled = MghGz.sample(seed=4)
    task.in_T1 = MghGz.sample(seed=13)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
