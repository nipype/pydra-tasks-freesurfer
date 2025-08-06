from fileformats.generic import Directory
from fileformats.medimage import Nifti1
from fileformats.medimage_freesurfer import Dat
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.smooth import Smooth
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_smooth_1():
    task = Smooth()
    task.in_file = Nifti1.sample(seed=0)
    task.reg_file = Dat.sample(seed=1)
    task.subjects_dir = Directory.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_smooth_2():
    task = Smooth()
    task.in_file = Nifti1.sample(seed=0)
    task.reg_file = Dat.sample(seed=1)
    task.smoothed_file = "foo_out.nii"
    task.surface_fwhm = 10
    task.vol_fwhm = 6
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
