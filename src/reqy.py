import argparse
from pathlib import Path
import generator

def log(args, message):
    message_format = '{args.projectname}: {message}'
    if hasattr(args, 'file') and args.file is not None:
        message_format = message_format + ' for file {args.file}'
    print(message_format.format(args=args, message=message))

def __add_project(args):
    if args.projectdir is None:
        args.projectdir = Path.cwd().parent
    else:
        args.projectdir = Path(args.projectdir)
    args.modeldir = args.projectdir / 'src_doc' / 'model'
    args.projectname = args.projectdir.stem
    args.modelfile = args.modeldir / (args.projectname+'.archimate')
    args.reqypath = Path(__file__).parent.parent
    args.problems = []

    if args.verbose:
        print('{args.projectname}: {args.projectdir}'.format(args=args))
    if args.debug:
        print(args)

    return args

if __name__ == '__main__':
    print('reqy: START\n')    
    
    parser = argparse.ArgumentParser(description='práca s požiadavkami')
    parser.add_argument('-pd', '--projectdir', help='set project explicitly')
    parser.add_argument('-v', '--verbose', help='to be more verbose', action='store_true')
    parser.add_argument('-d', '--debug', help='add debug info, very low level', action='store_true')
    parser.add_argument('-f', '--file', help='process only this one file')

    args = parser.parse_args()
    if args.debug:
        args.verbose = True
    args = __add_project(args)

    # process requirements
    generator.generatereqs(args)

    if args.problems:
        print('\nreqy: DONE ... with PROBLEMS !!')
        for p in args.problems:
            print('  ', p)
    else:
        print('\reqy: DONE ... OK')
