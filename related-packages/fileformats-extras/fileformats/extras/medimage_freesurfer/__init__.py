from pathlib import Path
import typing as ty
from random import Random
from fileformats.core import FileSet
from fileformats.medimage_freesurfer import (
    Inflated,
    Nofix,
    White,
    Lta,
    Pial,
    Label,
    Reg,
    Thickness,
    Area,
    Xfm,
    M3z,
    Annot,
    Stats,
    Out,
    Avg_curv,
    Orig,
    Ctab,
)



@FileSet.generate_sample_data.register
def gen_sample_inflated_data(inflated: Inflated, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_nofix_data(nofix: Nofix, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_white_data(white: White, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_lta_data(lta: Lta, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_pial_data(pial: Pial, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_label_data(label: Label, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_reg_data(reg: Reg, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_thickness_data(thickness: Thickness, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_area_data(area: Area, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_xfm_data(xfm: Xfm, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_m3z_data(m3z: M3z, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_annot_data(annot: Annot, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_stats_data(stats: Stats, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_out_data(out: Out, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_avg_curv_data(avg_curv: Avg_curv, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_orig_data(orig: Orig, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError


@FileSet.generate_sample_data.register
def gen_sample_ctab_data(ctab: Ctab, dest_dir: Path, seed: ty.Union[int, Random] = 0, stem: ty.Optional[str] = None) -> ty.Iterable[Path]:
    raise NotImplementedError
