import os
import sys
import logging
from tqdm import tqdm
import warnings
import torch

class VerboseTqdm(tqdm):
    def __init__(self, *args, **kwargs):
        verbose = os.environ.get('VERBOSE_OUTPUT', 'true').lower() == 'true'
        if not verbose:
            kwargs['disable'] = True
        super().__init__(*args, **kwargs)

def verbose_print(*args, **kwargs):
    verbose = os.environ.get('VERBOSE_OUTPUT', 'true').lower() == 'true'
    if verbose:
        print(*args, **kwargs)

def suppress_all_output():
    # Suppress stdout/stderr
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    
    # Suppress warnings
    warnings.filterwarnings('ignore')
    
    # Suppress logging
    logging.getLogger().setLevel(logging.CRITICAL)
    
    # Suppress torch messages
    os.environ['PYTORCH_IGNORE_WARNINGS'] = '1'
    logging.getLogger("torch").setLevel(logging.CRITICAL)
    
    # Suppress CUDA messages
    os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
    
    # Suppress tqdm
    os.environ['TQDM_DISABLE'] = '1'

def setup_logging(verbose=True):
    if not verbose:
        suppress_all_output()
    else:
        logging.getLogger().setLevel(logging.INFO)

# Monkey patch torch.nn.Module.__repr__ to respect verbose setting
original_repr = torch.nn.Module.__repr__
def new_repr(self):
    verbose = os.environ.get('VERBOSE_OUTPUT', 'true').lower() == 'true'
    if verbose:
        return original_repr(self)
    return ""
torch.nn.Module.__repr__ = new_repr