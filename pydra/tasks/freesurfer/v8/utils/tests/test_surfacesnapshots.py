from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.surface_snapshots import SurfaceSnapshots
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_surfacesnapshots_1():
    task = SurfaceSnapshots()
    task.overlay = File.sample(seed=5)
    task.overlay_reg = File.sample(seed=6)
    task.annot_file = File.sample(seed=15)
    task.label_file = File.sample(seed=17)
    task.colortable = File.sample(seed=19)
    task.patch_file = File.sample(seed=22)
    task.tcl_script = File.sample(seed=30)
    task.subjects_dir = Directory.sample(seed=31)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
