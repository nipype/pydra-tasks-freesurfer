from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.petsurfer.logan import Logan
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_logan_1():
    task = Logan()
    task.in_file = Nifti1.sample(seed=2)
    task.design = File.sample(seed=4)
    task.contrast = [File.sample(seed=5)]
    task.per_voxel_reg = [File.sample(seed=8)]
    task.weighted_ls = File.sample(seed=10)
    task.fixed_fx_var = File.sample(seed=11)
    task.fixed_fx_dof_file = File.sample(seed=13)
    task.weight_file = File.sample(seed=14)
    task.mask_file = File.sample(seed=21)
    task.label_file = File.sample(seed=22)
    task.surf_geo = "white"
    task.sim_done_file = File.sample(seed=58)
    task.subjects_dir = Directory.sample(seed=61)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_logan_2():
    task = Logan()
    task.glm_dir = "logan"
    task.in_file = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
