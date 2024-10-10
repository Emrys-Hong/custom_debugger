import sys
from IPython.core.debugger import Pdb
import ipdb

class _IPdb(Pdb):
    """
    Supports using IPDB from inside a multiprocessing child process.
    Usage:
    _IPdb().set_trace()
    """
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            # Redirect stdin to ensure it works in child processes
            sys.stdin = open('/dev/stdin')
            super().interaction(*args, **kwargs)
        finally:
            sys.stdin = _stdin

def breakpoint(rank: int = 0):
    """
    Set a breakpoint using IPDB, but only on a single rank in a distributed environment.
    All other ranks will wait for the breakpoint to be released before continuing.
    In a normal environment, it sets a breakpoint directly.

    Args:
        rank (int): Which rank to break on. Default: 0
    """
    try:
        import torch.distributed as dist
        is_dist = dist.is_initialized()
        current_rank = dist.get_rank()
    except (ImportError, RuntimeError):
        # If torch.distributed is not available or not initialized, default to non-distributed
        is_dist = False
        current_rank = 0

    if is_dist:
        if current_rank == rank:
            pdb_instance = _IPdb()
            pdb_instance.message(
                "\n!!! ATTENTION !!!\n\n"
                f"Type 'up' to get to the frame that called breakpoint(rank={rank})\n"
            )
            pdb_instance.set_trace()
        # Synchronize all processes; others will wait here
        dist.barrier()
    else:
        # In a normal environment, just set a breakpoint directly
        ipdb.set_trace()
