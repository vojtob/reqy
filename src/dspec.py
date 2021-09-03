import shutil
import os
from pathlib import PureWindowsPath, Path
import subprocess
import re
# import unidecode

import model.model_processing as mp
import generator as docgen
# from docool.utils import mycopy
                      
def list_unsolved_requirements(args):
    processor = mp.ArchiFileProcessor(args.projectdir)
    c = 0
    reqs = processor.get_all_requirements()
    for r in sorted(reqs, key=lambda req: req.name):
        if len(r.realizations) < 1:
            print(r.name)
            c = c+1
    print('{0} requirements unsolved'.format(c))

def doit(args):
    if args.requirements or args.all or args.update:
        if args.verbose:
            print('generate requirements pages')
        docgen.generatereqs(args)
    if args.list:
        list_unsolved_requirements(args)