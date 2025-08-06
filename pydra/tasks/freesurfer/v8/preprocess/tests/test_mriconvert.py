from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.mri_convert import MRIConvert
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mriconvert_1():
    task = MRIConvert()
    task.autoalign_matrix = File.sample(seed=37)
    task.apply_transform = File.sample(seed=39)
    task.apply_inv_transform = File.sample(seed=40)
    task.in_file = Nifti1.sample(seed=54)
    task.reslice_like = File.sample(seed=62)
    task.in_like = File.sample(seed=72)
    task.color_file = File.sample(seed=76)
    task.status_file = File.sample(seed=78)
    task.sdcm_list = File.sample(seed=79)
    task.subjects_dir = Directory.sample(seed=83)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mriconvert_2():
    task = MRIConvert()
    task.out_type = "mgz"
    task.in_file = Nifti1.sample(seed=54)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
