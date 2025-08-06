from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.recon_all import ReconAll
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_reconall_1():
    task = ReconAll()
    task.directive = "all"
    task.T1_files = [File.sample(seed=3)]
    task.T2_file = File.sample(seed=4)
    task.FLAIR_file = File.sample(seed=5)
    task.expert = File.sample(seed=16)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_reconall_2():
    task = ReconAll()
    task.subject_id = "foo"
    task.subjects_dir = "."
    task.flags = ["-cw256", "-qcache"]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_reconall_3():
    task = ReconAll()
    task.flags = []
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_reconall_4():
    task = ReconAll()
    task.directive = "autorecon-hemi"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_reconall_5():
    task = ReconAll()
    task.subject_id = "foo"
    task.hippocampal_subfields_T1 = False
    task.hippocampal_subfields_T2 = ("structural.nii", "test")
    task.subjects_dir = "."
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_reconall_6():
    task = ReconAll()
    task.directive = "all"
    task.base_template_id = "sub-template"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_reconall_7():
    task = ReconAll()
    task.directive = "all"
    task.longitudinal_timepoint_id = "ses-1"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
