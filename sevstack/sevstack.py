#
# sevstack ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#
import sys
from .inference import Inference
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
            [--imagefile]                                               \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                jonocameron/pl-sevstack sevstack                        \
                --imagefile sample.png /incoming /outgoing

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

        [--imagefile]
        Image file needed to run analysis on.
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
        self.add_argument('--metaname', 
                    dest         = 'metaname', 
                    type         = str, 
                    optional     = True,
                    help         = 'Name of ckpt meta file',
                    default      = 'model.meta')
        self.add_argument('--imagefile', 
                    dest         = 'imagefile', 
                    type         = str, 
                    optional     = False,
                    help         = 'Name of image file to infer from')
        self.add_argument('--in_tensorname', 
                    dest         = 'in_tensorname', 
                    type         = str, 
                    optional     = True,
                    help         = 'Name of input tensor to graph',
                    default      = 'input_1:0')
        self.add_argument('--out_tensorname', 
                    dest         = 'out_tensorname', 
                    type         = str, 
                    optional     = True,
                    help         = 'Name of output tensor from graph',
                    default      = 'norm_dense_1/Softmax:0')
        self.add_argument('--input_size', 
                    dest         = 'input_size', 
                    type         = int, 
                    optional     = True,
                    help         = 'Size of input (ex: if 480x480, --input_size 480)',
                    default      = 480)
        self.add_argument('--top_percent', 
                    dest         = 'top_percent', 
                    type         = float, 
                    optional     = True,
                    help         = 'Percent top crop from top of image',
                    default      = 0.08)

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        # python covidnet.py inputimage output --imagefile ex-covid.jpeg
        print(Gstr_title)
        print("Developing own pl-covidnet")
        print('Version: %s' % self.get_version())
        all_three_models = [
            # {
            #     'weightspath':'/models/COVIDNet-CXR3-A',
            #     'ckptname':'model-2856',
            #     'modelused':'modelA'
            # }, 
            {
                'weightspath':'/usr/local/lib/covidnet/COVIDNet-CXR4-B',
                'ckptname':'model-1545',
                'modelused':'modelB'
            },
            # {
            #     'weightspath': '/models/COVIDNet-CXR3-C',
            #     'ckptname':'model-0',
            #     'modelused':'modelC'
            # }
        ]
        for model in all_three_models:
            options.weightspath = model['weightspath']
            options.ckptname = model['ckptname']
            options.modelused = model['modelused']
            infer_obj = Inference(options)
            infer_obj.infer()


    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
