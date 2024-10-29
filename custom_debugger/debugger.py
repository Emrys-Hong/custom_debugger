import pdb
import sys

import torch.distributed as dist


class _DistributedPdb(pdb.Pdb):
    """
    Supports using PDB from inside a multiprocessing child process.
    Usage:
    _DistributedPdb().set_trace()
    """

    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open("/dev/stdin")
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin


def breakpoint(rank: int = 0):
    """
    Set a breakpoint, but only on a single rank.  All other ranks will wait for you to be
    done with the breakpoint before continuing.
    Args:
        rank (int): Which rank to break on.  Default: ``0``
    """
    try:
        is_dist = dist.is_initialized()
        current_rank = dist.get_rank()
    except:
        is_dist = False
        current_rank = 0

    if is_dist:
        if current_rank == rank:
            pdb = _DistributedPdb()
            pdb.message(
                "\n!!! ATTENTION !!!\n\n"
                f"Type 'up' to get to the frame that called dist.breakpoint(rank={rank})\n"
            )
            pdb.set_trace()
        dist.barrier()
    else:
        import ipdb
        ipdb.set_trace()
