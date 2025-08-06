from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.model.seg_stats_recon_all import SegStatsReconAll
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_segstatsreconall_1():
    task = SegStatsReconAll()
    task.subject_id = "subject_id"
    task.ribbon = MghGz.sample(seed=1)
    task.presurf_seg = MghGz.sample(seed=2)
    task.transform = File.sample(seed=3)
    task.lh_orig_nofix = File.sample(seed=4)
    task.rh_orig_nofix = Pial.sample(seed=5)
    task.lh_white = File.sample(seed=6)
    task.rh_white = Pial.sample(seed=7)
    task.lh_pial = File.sample(seed=8)
    task.rh_pial = Pial.sample(seed=9)
    task.aseg = File.sample(seed=10)
    task.segmentation_file = File.sample(seed=12)
    task.partial_volume_file = File.sample(seed=16)
    task.in_file = File.sample(seed=17)
    task.color_table_file = File.sample(seed=22)
    task.gca_color_table = File.sample(seed=24)
    task.mask_file = File.sample(seed=32)
    task.brainmask_file = File.sample(seed=39)
    task.in_intensity = File.sample(seed=50)
    task.subjects_dir = Directory.sample(seed=52)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_segstatsreconall_2():
    task = SegStatsReconAll()
    task.ribbon = MghGz.sample(seed=1)
    task.presurf_seg = MghGz.sample(seed=2)
    task.rh_orig_nofix = Pial.sample(seed=5)
    task.rh_white = Pial.sample(seed=7)
    task.rh_pial = Pial.sample(seed=9)
    task.annot = ("PWS04", "lh", "aparc")
    task.summary_file = "summary.stats"
    task.cortex_vol_from_surf = True
    task.brain_vol = "brain-vol-from-seg"
    task.etiv = True
    task.supratent = True
    task.euler = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
