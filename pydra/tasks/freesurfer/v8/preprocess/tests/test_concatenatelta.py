from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Lta
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.concatenate_lta import ConcatenateLTA
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_concatenatelta_1():
    task = ConcatenateLTA()
    task.in_lta1 = Lta.sample(seed=0)
    task.tal_source_file = File.sample(seed=7)
    task.tal_template_file = File.sample(seed=8)
    task.subjects_dir = Directory.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_concatenatelta_2():
    task = ConcatenateLTA()
    task.in_lta1 = Lta.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_concatenatelta_3():
    task = ConcatenateLTA()
    task.in_lta2 = "identity.nofile"
    task.out_file = "inv1.lta"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_concatenatelta_4():
    task = ConcatenateLTA()
    task.out_type = "RAS2RAS"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
