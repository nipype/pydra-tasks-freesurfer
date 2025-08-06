from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.model.spherical_average import SphericalAverage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_sphericalaverage_1():
    task = SphericalAverage()
    task.in_surf = Pial.sample(seed=2)
    task.in_orig = File.sample(seed=8)
    task.subjects_dir = Directory.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_sphericalaverage_2():
    task = SphericalAverage()
    task.out_file = "test.out"
    task.in_surf = Pial.sample(seed=2)
    task.fname = "lh.entorhinal"
    task.subject_id = "10335"
    task.threshold = 5
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
