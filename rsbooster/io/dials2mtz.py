#!/usr/bin/env python
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from reciprocalspaceship.io import dials


def get_parser():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "dirnames",
        type=str,
        nargs="+",
        help="diffBragg.stills_process output folder(s) with *integrated.refls",
    )
    parser.add_argument("mtz", type=str, help="output mtz name")
    parser.add_argument(
        "--ucell",
        default=None,
        nargs=6,
        type=float,
        help="unit cell params (default will be average experiment crystal)",
    )
    parser.add_argument("--symbol", type=str, default=None)
    return parser


def _write(ds, mtzname):
    """write the RS dataset to mtz file"""
    ds.write_mtz(mtzname)
    print("Wrote %s." % mtzname)
    print("Done!")


def ray_main():
    parser = get_parser()
    parser.add_argument("--nj", default=10, type=int, help="number of workers!")
    args = parser.parse_args()
    assert args.ucell is not None
    assert args.symbol is not None

    ds = dials.read_dials_stills(args.dirnames, ucell=args.ucell, symbol=args.symbol, nj=args.nj)
    _write(ds, args.mtz)


def mpi_main():
    parser = get_parser()
    args = parser.parse_args()
    assert args.ucell is not None
    assert args.symbol is not None
    from mpi4py import MPI
    COMM = MPI.COMM_WORLD
    from reciprocalspaceship.io.dials_mpi import read_dials_stills_mpi
    ds = read_dials_stills_mpi(args.dirnames, ucell=args.ucell, symbol=args.symbol)
    if COMM.rank==0:
        _write(ds, args.mtz)


if __name__ == "__main__":
    ray_main()
