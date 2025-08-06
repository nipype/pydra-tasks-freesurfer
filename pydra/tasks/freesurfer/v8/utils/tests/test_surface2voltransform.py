from fileformats.generic import File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.surface_2_vol_transform import Surface2VolTransform
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_surface2voltransform_1():
    task = Surface2VolTransform()
    task.source_file = MghGz.sample(seed=0)
    task.reg_file = File.sample(seed=3)
    task.template_file = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_surface2voltransform_2():
    task = Surface2VolTransform()
    task.source_file = MghGz.sample(seed=0)
    task.hemi = "lh"
    task.subjects_dir = "."
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
