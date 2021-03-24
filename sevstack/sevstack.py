#
# sevstack ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from chrisapp.base import ChrisApp
import os
import numpy as np

Gstr_title = """
                    _             _    
                   | |           | |   
 ___  _____   _____| |_ __ _  ___| | __
/ __|/ _ \ \ / / __| __/ _` |/ __| |/ /
\__ \  __/\ V /\__ \ || (_| | (__|   < 
|___/\___| \_/ |___/\__\__,_|\___|_|\_\
                                       
                                       
"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       sevstack.py 

    SYNOPSIS

        python sevstack.py                                         \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-sevstack sevstack                        \
                /incoming /outgoing

    DESCRIPTION

        `sevstack.py` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 
"""


class Sevstack(ChrisApp):
    """
    A ChRIS plugin to produce ranked list of severity scores
    """
    PACKAGE                 = __package__
    TITLE                   = 'Ranked severity scores'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = '' # url of an icon image
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        #--inputfile
        #--outputfile

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """

        print(Gstr_title)
        print('Version: %s\n\n\n\n' % self.get_version())

        arr = np.array([])

        with open ('{}/randomnumbers.txt'.format(options.inputdir)) as file:
            for each in file:
                each = each.rstrip("\n")
                each = int(each)
                arr = np.append(arr, each)
        
        file.close()

        arr = np.sort(arr)
        print(arr)

    
        file = open('{}/sortednumbers.txt'.format(options.outputdir), 'w')
        for each in arr:
            file.write(str(each) + "\n")

        file.close()

        print('done')


    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
