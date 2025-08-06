from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.mr_is_ca_label import MRIsCALabel
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mriscalabel_1():
    task = MRIsCALabel()
    task.subject_id = "subject_id"
    task.canonsurf = Pial.sample(seed=2)
    task.classifier = File.sample(seed=3)
    task.smoothwm = Pial.sample(seed=4)
    task.curv = File.sample(seed=5)
    task.sulc = Pial.sample(seed=6)
    task.label = File.sample(seed=8)
    task.aseg = File.sample(seed=9)
    task.subjects_dir = Directory.sample(seed=13)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mriscalabel_2():
    task = MRIsCALabel()
    task.subject_id = "test"
    task.canonsurf = Pial.sample(seed=2)
    task.smoothwm = Pial.sample(seed=4)
    task.sulc = Pial.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
