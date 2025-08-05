from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.aparc_2_aseg import Aparc2Aseg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_aparc2aseg_1():
    task = Aparc2Aseg()
    task.subject_id = "subject_id"
    task.lh_white = Pial.sample(seed=2)
    task.rh_white = File.sample(seed=3)
    task.lh_pial = Pial.sample(seed=4)
    task.rh_pial = File.sample(seed=5)
    task.lh_ribbon = MghGz.sample(seed=6)
    task.rh_ribbon = File.sample(seed=7)
    task.ribbon = MghGz.sample(seed=8)
    task.lh_annotation = File.sample(seed=9)
    task.rh_annotation = Pial.sample(seed=10)
    task.filled = File.sample(seed=11)
    task.aseg = File.sample(seed=12)
    task.ctxseg = File.sample(seed=14)
    task.subjects_dir = Directory.sample(seed=20)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_aparc2aseg_2():
    task = Aparc2Aseg()
    task.lh_white = Pial.sample(seed=2)
    task.lh_pial = Pial.sample(seed=4)
    task.lh_ribbon = MghGz.sample(seed=6)
    task.ribbon = MghGz.sample(seed=8)
    task.rh_annotation = Pial.sample(seed=10)
    task.label_wm = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
