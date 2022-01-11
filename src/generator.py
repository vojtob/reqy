# import os
from pathlib import Path
# import re
import model.model_processing as mp

def __get_header(title, level):
    return '{0} {1}'.format(level*'#', title)

def __formatrealization(args, fout, realization):
    if args.outputtype == 'md':
        fout.write(realization + "\n")
    elif args.outputtype == 'short':
        fout.write(realization + "\n")
    else: # excel
        fout.write('"' + realization + '"')

def __writerealization(args, fout, realization):
    # Realization by product type is used for general remarks, only realization relationship is displayed, no reference to element
    if realization.type == 'Product':
        fout.write('{0}\n'.format(realization.realization_relationship.desc))
        return

    # Capability means only simple description is displayed, no reference to element
    if realization.type == 'Capability':
        # fout.write('Vyjadrenie k realizácii požiadavky: {capability_name}: {realization_description}\n'.format(
        fout.write('{capability_name}: {realization_description}\n'.format(
            capability_name=realization.name, 
            realization_description=realization.desc))
        return
    
    # realization by element
    fout.write('Požiadavku realizuje {element_type}: {realization_name}'.format(
        realization_name=realization.name,
        element_type=mp.Element.type2sk(realization.type))
    )    
    if args.outputtype == 'md':
        if realization.realization_relationship.desc is not None:
            # add specific description
            fout.write('. ' + realization.realization_relationship.desc)
        else:
            fout.write('. ' + realization.desc)
    fout.write('\n')

def __writereqheader(args, fout, req):
    if (args.outputtype == 'md') or (args.outputtype == 'short'):
        fout.write('#### ' + req.name)  
        fout.write('\n')  
    else: # excel
        fout.write(req.name.split()[0] + ';')

def __writenorealization(args, fout, req):
    if (args.outputtype == 'md') or (args.outputtype == 'short'):
        fout.write('XXXXXX TODO: Ziadna realizacia poziadavky\n\n')  
    else: # excel
        fout.write('"XXXXXX TODO: Ziadna realizacia poziadavky"\n')
    
def __writerealizations(args, fout, realizations):
    if args.outputtype == 'md':
        separator = False
        for realization in realizations:
            if separator:
                fout.write('\n-----\n\n')
            __writerealization(args, fout, realization)
            separator=True
        fout.write('\n')
    elif args.outputtype == 'short':
        for realization in realizations:
            __writerealization(args, fout, realization)
        fout.write('\n')
    else: # excel
        fout.write('"')
        for realization in realizations:
            __writerealization(args, fout, realization)
        fout.write('"\n')

def __writereq(args, fout, req):
    if args.debug:
        print('    process requirement', req.name)
    
    __writereqheader(args, fout, req)
    # requirement realizations
    if len(req.realizations) == 0:
        __writenorealization(args, fout, req)
    else:    
        __writerealizations(args, fout, sorted(req.realizations, key = lambda x: x.weight()))

def __process_req_folder(args, processor, fout, processedfolder, parentpath, depth):
    if args.debug:
        print('process folder {0} in {1}'.format(processedfolder, parentpath))

    # folder header
    if (args.outputtype == 'md') or (args.outputtype == 'short'):
        fout.write(__get_header('Adresár {0}'.format(processedfolder), depth))
        fout.write('\n\n')

    # process requirements
    reqs = sorted(processor.get_requirements(processedfolder), key = lambda x: x.name)
    # fout.write('{0} requirements\n\n'.format(len(reqs)))
    for req in reqs:
        __writereq(args, fout, req)

    # process subfolders
    for w, subfolder in enumerate(sorted(processor.get_folders(processedfolder))):
        __process_req_folder(args, processor, fout, subfolder, parentpath/processedfolder, depth+1)
    

def generatereqs(args):
    processor = mp.ArchiFileProcessor(args.projectdir)

    reqpath = args.projectdir / 'temp'
    if args.outputtype == 'md':
        reqpath = reqpath / 'requirements.md'
    elif args.outputtype == 'short':
        reqpath = reqpath / 'requirements.md'
    else: # excel
        reqpath = reqpath / 'requirements.csv'
    # reqpath = args.projectdir / 'temp' / 'requirements.md'

    if args.verbose:
        print('requirements file:', reqpath)
    with open(str(reqpath), 'w', encoding='utf8') as fout:
        __process_req_folder(args, processor, fout, 'Requirements', Path(args.projectname), 1)
