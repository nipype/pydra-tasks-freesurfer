from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.relabel_hypointensities import (
    RelabelHypointensities,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_relabelhypointensities_1():
    task = RelabelHypointensities()
    task.lh_white = Pial.sample(seed=0)
    task.rh_white = File.sample(seed=1)
    task.aseg = File.sample(seed=2)
    task.surf_directory = Directory.sample(seed=3)
    task.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_relabelhypointensities_2():
    task = RelabelHypointensities()
    task.lh_white = Pial.sample(seed=0)
    task.surf_directory = "."
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
