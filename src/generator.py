# import os
from pathlib import Path
# import re
import model.model_processing as mp

def __get_header(title, level):
    return '{0} {1}'.format(level*'#', title)

def __writerealization(args, fout, realization):
    # Realization by product type is used for general remarks, only realization relationship is displayed, no reference to element
    if realization.type == 'Product':
        fout.write('Vyjadrenie k realizácii požiadavky: {0}\n'.format(realization.realization_relationship.desc))
        return

    # Capability means only simple description is displayed, no reference to element
    if realization.type == 'Capability':
        fout.write('Vyjadrenie k realizácii požiadavky: {capability_name}: {realization_description}\n'.format(
            capability_name=realization.name, 
            realization_description=realization.desc))
        return
    
    # realization by element
    fout.write('Požiadavku realizuje {element_type}: {realization_name}'.format(
        realization_name=realization.name,
        element_type=mp.Element.type2sk(realization.type))
    )    
    if realization.realization_relationship.desc is not None:
        # add specific description
        fout.write('. ' + realization.realization_relationship.desc)
    fout.write('\n')

def __writereq(args, fout, req):
    if args.debug:
        print('    process requirement', req.name)
    
    # requirement header
    fout.write(req.name)  
    fout.write('\n')  

    # requirement realizations
    if len(req.realizations) == 0:
        # fout.write('<font color="red">XXXXXX TODO: Ziadna realizacia poziadavky</font>\n\n')
        fout.write('XXXXXX TODO: Ziadna realizacia poziadavky\n\n')
        return
    # sort realizations, product is the first, than capabilities, other last
    for realization in sorted(req.realizations, key = lambda x: x.weight()):
        __writerealization(args, fout, realization)
    fout.write('\n')

def __process_req_folder(args, processor, fout, processedfolder, parentpath, depth):
    if args.debug:
        print('process folder {0} in {1}'.format(processedfolder, parentpath))

    # folder header
    fout.write(__get_header('Adresár {0}'.format(processedfolder), depth))
    fout.write('\n\n')

    # process requirements
    reqs = processor.get_requirements(processedfolder)
    # fout.write('{0} requirements\n\n'.format(len(reqs)))
    for req in reqs:
        __writereq(args, fout, req)

    # process subfolders
    for w, subfolder in enumerate(sorted(processor.get_folders(processedfolder))):
        __process_req_folder(args, processor, fout, subfolder, parentpath/processedfolder, depth+1)
    

def generatereqs(args):
    processor = mp.ArchiFileProcessor(args.projectdir)

    # generate map of archilinks to pages
    # emap = generate_elements_map(args, processor)
    # print(emap)

    # generate requirements
    # reqpath = hugo.getlocalpath(args) / 'content'
    with open('requirements.txt', 'w', encoding='utf8') as fout:
        __process_req_folder(args, processor, fout, 'Requirements', Path(args.projectname), 1)