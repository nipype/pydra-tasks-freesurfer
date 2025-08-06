from ._version import __version__  # noqa: F401
from fileformats.generic import File


class Inflated(File):
    ext = ".inflated"
    binary = True


class Nofix(File):
    ext = ".nofix"
    binary = True


class Thickness(File):
    ext = ".thickness"
    binary = True


class Pial(File):
    ext = ".pial"
    binary = True


class Out(File):
    ext = ".out"
    binary = True


class Xfm(File):
    ext = ".xfm"
    binary = True


class Ctab(File):
    ext = ".ctab"
    binary = True


class M3z(File):
    ext = ".m3z"
    binary = True


class Reg(File):
    ext = ".reg"
    binary = True


class Area(File):
    ext = ".area"
    binary = True


class Annot(File):
    ext = ".annot"
    binary = True


class Orig(File):
    ext = ".orig"
    binary = True


class Lta(File):
    ext = ".lta"
    binary = True


class Stats(File):
    ext = ".stats"
    binary = True


class White(File):
    ext = ".white"
    binary = True


class Label(File):
    ext = ".label"
    binary = True


class Dat(File):
    ext = ".label"
    binary = True
