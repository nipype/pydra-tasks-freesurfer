from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.synthesize_flash import SynthesizeFLASH
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_synthesizeflash_1():
    task = SynthesizeFLASH()
    task.t1_image = MghGz.sample(seed=4)
    task.pd_image = File.sample(seed=5)
    task.subjects_dir = Directory.sample(seed=7)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_synthesizeflash_2():
    task = SynthesizeFLASH()
    task.tr = 20
    task.flip_angle = 30
    task.te = 3
    task.t1_image = MghGz.sample(seed=4)
    task.out_file = "flash_30syn.mgz"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
