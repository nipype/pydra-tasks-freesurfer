from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.model.glm_fit import GLMFit
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_glmfit_1():
    task = GLMFit()
    task.in_file = Nifti1.sample(seed=1)
    task.design = File.sample(seed=3)
    task.contrast = [File.sample(seed=4)]
    task.per_voxel_reg = [File.sample(seed=7)]
    task.weighted_ls = File.sample(seed=9)
    task.fixed_fx_var = File.sample(seed=10)
    task.fixed_fx_dof_file = File.sample(seed=12)
    task.weight_file = File.sample(seed=13)
    task.mask_file = File.sample(seed=20)
    task.label_file = File.sample(seed=21)
    task.surf_geo = "white"
    task.sim_done_file = File.sample(seed=58)
    task.subjects_dir = Directory.sample(seed=61)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_glmfit_2():
    task = GLMFit()
    task.in_file = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
