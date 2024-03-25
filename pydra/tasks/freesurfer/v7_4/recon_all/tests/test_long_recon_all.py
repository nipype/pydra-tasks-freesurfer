from pydra.tasks.freesurfer.v7_4.recon_all.long_recon_all import LongReconAll


def test_executable():
    assert LongReconAll.executable == "recon-all"
