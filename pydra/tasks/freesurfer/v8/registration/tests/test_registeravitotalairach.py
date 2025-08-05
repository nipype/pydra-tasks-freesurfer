from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
from fileformats.text import TextFile
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.registration.register_av_ito_talairach import (
    RegisterAVItoTalairach,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_registeravitotalairach_1():
    task = RegisterAVItoTalairach()
    task.in_file = MghGz.sample(seed=0)
    task.target = File.sample(seed=1)
    task.vox2vox = TextFile.sample(seed=2)
    task.out_file = "talairach.auto.xfm"
    task.subjects_dir = Directory.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registeravitotalairach_2():
    task = RegisterAVItoTalairach()
    task.in_file = MghGz.sample(seed=0)
    task.vox2vox = TextFile.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
