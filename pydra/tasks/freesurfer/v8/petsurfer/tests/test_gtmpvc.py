from fileformats.generic import Directory, File
from fileformats.medimage import NiftiGz
from fileformats.medimage_freesurfer import Lta
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.petsurfer.gtmpvc import GTMPVC
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_gtmpvc_1():
    task = GTMPVC()
    task.in_file = NiftiGz.sample(seed=0)
    task.segmentation = File.sample(seed=3)
    task.reg_file = Lta.sample(seed=4)
    task.mask_file = File.sample(seed=8)
    task.contrast = [File.sample(seed=12)]
    task.color_table_file = File.sample(seed=21)
    task.subjects_dir = Directory.sample(seed=55)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_gtmpvc_2():
    task = GTMPVC()
    task.in_file = NiftiGz.sample(seed=0)
    task.psf = 4
    task.reg_file = Lta.sample(seed=4)
    task.auto_mask = (1, 0.1)
    task.km_hb = ["11 12 50 51"]
    task.save_input = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_gtmpvc_3():
    task = GTMPVC()
    task.in_file = NiftiGz.sample(seed=0)
    task.regheader = True
    task.mg = (0.5, ["ROI1", "ROI2"])
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
