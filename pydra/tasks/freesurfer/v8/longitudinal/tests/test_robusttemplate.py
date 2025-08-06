from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.longitudinal.robust_template import RobustTemplate
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_robusttemplate_1():
    task = RobustTemplate()
    task.in_files = [Nifti1.sample(seed=0)]
    task.out_file = "mri_robust_template_out.mgz"
    task.initial_transforms = [File.sample(seed=12)]
    task.in_intensity_scales = [File.sample(seed=13)]
    task.subjects_dir = Directory.sample(seed=15)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_robusttemplate_2():
    task = RobustTemplate()
    task.in_files = [Nifti1.sample(seed=0)]
    task.out_file = "T1.nii"
    task.subsample_threshold = 200
    task.average_metric = "mean"
    task.fixed_timepoint = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_robusttemplate_3():
    task = RobustTemplate()
    task.transform_outputs = ["structural.lta", "functional.lta"]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_robusttemplate_4():
    task = RobustTemplate()
    task.transform_outputs = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
