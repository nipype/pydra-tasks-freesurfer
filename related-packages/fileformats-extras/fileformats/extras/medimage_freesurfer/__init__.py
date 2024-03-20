from ._version import __version__  # noqa: F401
from pathlib import Path
import typing as ty
from random import Random
from fileformats.core import FileSet, SampleFileGenerator
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



@FileSet.generate_sample_data.register
def gen_sample_label_data(label: Label, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_lta_data(lta: Lta, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_orig_data(orig: Orig, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_reg_data(reg: Reg, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_annot_data(annot: Annot, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_pial_data(pial: Pial, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_nofix_data(nofix: Nofix, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_ctab_data(ctab: Ctab, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_xfm_data(xfm: Xfm, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_area_data(area: Area, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_m3z_data(m3z: M3z, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_stats_data(stats: Stats, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_white_data(white: White, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_thickness_data(thickness: Thickness, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_inflated_data(inflated: Inflated, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_out_data(out: Out, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError
