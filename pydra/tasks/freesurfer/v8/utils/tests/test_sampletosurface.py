from fileformats.generic import Directory, File
from fileformats.medimage import NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.sample_to_surface import SampleToSurface
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_sampletosurface_1():
    task = SampleToSurface()
    task.source_file = NiftiGz.sample(seed=0)
    task.reference_file = File.sample(seed=1)
    task.reg_file = File.sample(seed=4)
    task.mask_label = File.sample(seed=18)
    task.subjects_dir = Directory.sample(seed=35)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_sampletosurface_2():
    task = SampleToSurface()
    task.source_file = NiftiGz.sample(seed=0)
    task.hemi = "lh"
    task.sampling_method = "average"
    task.sampling_units = "frac"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
