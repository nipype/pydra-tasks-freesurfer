from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial, White
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.parcellation_stats import ParcellationStats
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_parcellationstats_1():
    task = ParcellationStats()
    task.subject_id = "subject_id"
    task.wm = MghGz.sample(seed=2)
    task.lh_white = File.sample(seed=3)
    task.rh_white = White.sample(seed=4)
    task.lh_pial = File.sample(seed=5)
    task.rh_pial = Pial.sample(seed=6)
    task.transform = File.sample(seed=7)
    task.thickness = File.sample(seed=8)
    task.brainmask = MghGz.sample(seed=9)
    task.aseg = File.sample(seed=10)
    task.ribbon = MghGz.sample(seed=11)
    task.cortex_label = File.sample(seed=12)
    task.in_cortex = File.sample(seed=15)
    task.in_annotation = File.sample(seed=16)
    task.in_label = File.sample(seed=17)
    task.subjects_dir = Directory.sample(seed=23)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_parcellationstats_2():
    task = ParcellationStats()
    task.subject_id = "10335"
    task.wm = MghGz.sample(seed=2)
    task.rh_white = White.sample(seed=4)
    task.rh_pial = Pial.sample(seed=6)
    task.brainmask = MghGz.sample(seed=9)
    task.ribbon = MghGz.sample(seed=11)
    task.surface = "white"
    task.out_color = "test.ctab"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
