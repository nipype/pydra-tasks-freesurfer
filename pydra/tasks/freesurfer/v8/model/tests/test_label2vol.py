from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
from fileformats.medimage_freesurfer import Dat, Label
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.model.label_2_vol import Label2Vol
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_label2vol_1():
    task = Label2Vol()
    task.label_file = [Label.sample(seed=0)]
    task.annot_file = File.sample(seed=1)
    task.seg_file = File.sample(seed=2)
    task.template_file = Nifti1.sample(seed=4)
    task.reg_file = Dat.sample(seed=5)
    task.reg_header = File.sample(seed=6)
    task.label_hit_file = File.sample(seed=16)
    task.map_label_stat = File.sample(seed=17)
    task.subjects_dir = Directory.sample(seed=19)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_label2vol_2():
    task = Label2Vol()
    task.label_file = [Label.sample(seed=0)]
    task.template_file = Nifti1.sample(seed=4)
    task.reg_file = Dat.sample(seed=5)
    task.fill_thresh = 0.5
    task.vol_label_file = "foo_out.nii"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
