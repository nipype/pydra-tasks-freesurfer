from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.ca_label import CALabel
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_calabel_1():
    task = CALabel()
    task.in_file = MghGz.sample(seed=0)
    task.transform = TextMatrix.sample(seed=2)
    task.template = File.sample(seed=3)
    task.in_vol = File.sample(seed=4)
    task.intensities = File.sample(seed=5)
    task.label = File.sample(seed=10)
    task.aseg = File.sample(seed=11)
    task.subjects_dir = Directory.sample(seed=13)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_calabel_2():
    task = CALabel()
    task.in_file = MghGz.sample(seed=0)
    task.transform = TextMatrix.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
