'''
A few utility functions.

Author: Cody Lewis
Date: 2019-03-30
'''


def print_progress(current_epoch, total_epochs, progress_len=31, prefix="", suffix=""):
    '''
    Print a progress bar about how far a process has went through it's epochs.
    '''
    progress = int(100 * current_epoch / total_epochs)

    progress_bar_progress = int(progress_len * progress * 0.01)
    if progress_bar_progress != 0:
        unprogressed = progress_len - progress_bar_progress
    else:
        unprogressed = progress_len - 1
    progress_bar = "["
    progress_bar += "".join(
        ["=" for _ in range(progress_bar_progress - 2)] + [">" if unprogressed > 0 else "="]
    )
    progress_bar += "".join(["." for _ in range(unprogressed)])
    progress_bar += "]"
    print(f"\r{prefix} {progress_bar} {progress}% {suffix}", end="\r")
