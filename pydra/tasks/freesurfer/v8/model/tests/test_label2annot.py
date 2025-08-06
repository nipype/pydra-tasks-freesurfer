from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.model.label_2_annot import Label2Annot
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_label2annot_1():
    task = Label2Annot()
    task.subject_id = "subject_id"
    task.orig = File.sample(seed=4)
    task.color_table = File.sample(seed=7)
    task.subjects_dir = Directory.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_label2annot_2():
    task = Label2Annot()
    task.hemisphere = "lh"
    task.in_labels = ["lh.aparc.label"]
    task.out_annot = "test"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
