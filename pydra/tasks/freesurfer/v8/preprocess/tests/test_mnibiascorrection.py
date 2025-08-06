from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.mni_bias_correction import MNIBiasCorrection
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mnibiascorrection_1():
    task = MNIBiasCorrection()
    task.in_file = MghGz.sample(seed=0)
    task.iterations = 4
    task.mask = File.sample(seed=6)
    task.transform = File.sample(seed=7)
    task.subjects_dir = Directory.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mnibiascorrection_2():
    task = MNIBiasCorrection()
    task.in_file = MghGz.sample(seed=0)
    task.protocol_iterations = 1000
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
