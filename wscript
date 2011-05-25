# -*- python -*- 

import os
import glob
import fnmatch

VERSION = '0.0'
APPNAME = 'osworkflows'

top = '.'
out = 'build'

def configure(conf):
    conf.check_tool('gnu_dirs')

    inkscape = conf.find_program('inkscape')
    conf.define('INKSCAPE', inkscape)
    conf.define('VERSION', VERSION)
    conf.define('prefix', conf.env["PREFIX"])
    conf.define('PACKAGE', APPNAME)

def options(opt):
    opt.tool_options("gnu_dirs")

def build(bld):
    rules = [
        ('${INKSCAPE} -z -b "#FFFFFF" -e ${TGT} ${SRC} > /dev/null' , "png"),
        ('${INKSCAPE} -z -b "#FFFFFF" -A ${TGT} ${SRC} > /dev/null' , "pdf")
        ]
    
    for path, dirs, files in os.walk(os.path.relpath(top)) :
        for filename in fnmatch.filter(files, "*.svg"):
            if path.startswith("./build/") :
                continue
            
            for transform_rule, out_ext in rules :
                bld(rule=transform_rule,
                    source=os.path.join(path, filename),
                    target=os.path.join(path, filename).replace(".svg", 
                                                                "." + out_ext),
                    install_path=os.path.join('${DATADIR}', 
                                              'osweb', 'media',
                                              'workflows',
                                              path[2:]),
                    )
            
            bld.install_as(os.path.join('${DATADIR}', 
                                        'osweb', 'media',
                                        'workflows',
                                        path[2:], filename),
                           os.path.join(path[2:],  filename),
                           chmod=0640)
                

def dist(ctx):
    ctx.excl = ' **/.waf-1* **/*~ **/*.pyc **/*.swp **/.lock-w* **/debian/* **/.git/* **/.gitignore' 

