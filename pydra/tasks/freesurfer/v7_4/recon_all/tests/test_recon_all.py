from pydra.tasks.freesurfer.v7_4.recon_all import recon_all


def test_executable():
    assert recon_all.ReconAll.executable == "recon-all"
