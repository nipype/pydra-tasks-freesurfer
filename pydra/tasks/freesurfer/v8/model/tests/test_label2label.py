from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.model.label_2_label import Label2Label
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_label2label_1():
    task = Label2Label()
    task.subject_id = "subject_id"
    task.sphere_reg = Pial.sample(seed=2)
    task.white = File.sample(seed=3)
    task.source_sphere_reg = File.sample(seed=4)
    task.source_white = Pial.sample(seed=5)
    task.source_label = File.sample(seed=6)
    task.registration_method = "surface"
    task.subjects_dir = Directory.sample(seed=11)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_label2label_2():
    task = Label2Label()
    task.hemisphere = "lh"
    task.sphere_reg = Pial.sample(seed=2)
    task.source_white = Pial.sample(seed=5)
    task.source_subject = "fsaverage"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
