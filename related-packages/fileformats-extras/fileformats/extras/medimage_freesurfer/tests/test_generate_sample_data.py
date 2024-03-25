import pytest
from fileformats.medimage_freesurfer import (
    Label,
    Lta,
    Orig,
    Reg,
    Annot,
    Pial,
    Nofix,
    Ctab,
    Xfm,
    Area,
    M3z,
    Stats,
    White,
    Thickness,
    Inflated,
    Out,
)



@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_label_data():
    assert isinstance(Label.sample(), Label)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_lta_data():
    assert isinstance(Lta.sample(), Lta)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_orig_data():
    assert isinstance(Orig.sample(), Orig)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_reg_data():
    assert isinstance(Reg.sample(), Reg)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_annot_data():
    assert isinstance(Annot.sample(), Annot)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_pial_data():
    assert isinstance(Pial.sample(), Pial)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_nofix_data():
    assert isinstance(Nofix.sample(), Nofix)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_ctab_data():
    assert isinstance(Ctab.sample(), Ctab)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_xfm_data():
    assert isinstance(Xfm.sample(), Xfm)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_area_data():
    assert isinstance(Area.sample(), Area)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_m3z_data():
    assert isinstance(M3z.sample(), M3z)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_stats_data():
    assert isinstance(Stats.sample(), Stats)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_white_data():
    assert isinstance(White.sample(), White)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_thickness_data():
    assert isinstance(Thickness.sample(), Thickness)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_inflated_data():
    assert isinstance(Inflated.sample(), Inflated)


@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_out_data():
    assert isinstance(Out.sample(), Out)
