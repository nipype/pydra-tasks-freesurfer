from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.apply_vol_transform import ApplyVolTransform
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applyvoltransform_1():
    task = ApplyVolTransform()
    task.source_file = Nifti1.sample(seed=0)
    task.target_file = File.sample(seed=2)
    task.reg_file = File.sample(seed=6)
    task.lta_file = File.sample(seed=7)
    task.lta_inv_file = File.sample(seed=8)
    task.fsl_reg_file = File.sample(seed=9)
    task.xfm_reg_file = File.sample(seed=10)
    task.m3z_file = File.sample(seed=17)
    task.subjects_dir = Directory.sample(seed=20)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_applyvoltransform_2():
    task = ApplyVolTransform()
    task.source_file = Nifti1.sample(seed=0)
    task.transformed_file = "struct_warped.nii"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
