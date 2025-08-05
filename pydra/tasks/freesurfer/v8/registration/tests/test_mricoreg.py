from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.registration.mri_coreg import MRICoreg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mricoreg_1():
    task = MRICoreg()
    task.source_file = Nifti1.sample(seed=0)
    task.reference_file = File.sample(seed=1)
    task.out_lta_file = True
    task.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mricoreg_2():
    task = MRICoreg()
    task.source_file = Nifti1.sample(seed=0)
    task.subjects_dir = "."
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mricoreg_3():
    task = MRICoreg()
    task.source_file = Nifti1.sample(seed=0)
    task.subject_id = "fsaverage"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mricoreg_4():
    task = MRICoreg()
    task.sep = [4]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mricoreg_5():
    task = MRICoreg()
    task.sep = [4, 5]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
