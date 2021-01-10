import os
import glob
import json
from configparser import ConfigParser

class EasyConfig:
    def __init__(self, config_file = None, default_config = None, confdir = 'conf.d', workdir = None, debug = False):
        
        load_default_config = True
        config = ConfigParser()
        
        run_config = ConfigParser()
        run_config['default'] = {}
        run_config['running'] = {}
        default_config_items = run_config['default']
        running_config_items = run_config['running']

        self.confdir = confdir

        if workdir is None:
            self.workdir = os.getcwd() + '/gsheetapi'
        else:
            self.workdir = workdir

        if default_config is None:
            self.default_config = {}
            print("WARNING: No 'default_config' parameter given")
        else:
            self.default_config = default_config

        config_files = glob.glob('{}/{}/*.conf'.format(self.workdir, self.confdir))
        config_files.sort()

        if config_file is None:
            default_config_file = "{}/config.conf".format(self.workdir)
            config_files.insert(0, default_config_file)
            self.config_file = config_files
            if not os.path.isfile(default_config_file):
                print ("Default config ({}) not exist! creating...".format(default_config_file))
                try:
                    with open(default_config_file, 'w') as create_config_file:
                        config['DEFAULT'] = default_config
                        config['DEFAULT']['pve_cacert'] = './certs/pve-root-ca.pem'
                        config['pve_config'] = default_config
                        config.write(create_config_file)

                except Exception as ei:
                    print('Exception > {}'.format(ei))
        else:
            if config_file.startswith('/'):
                self.configFile = config_file
            elif config_file.startswith('~/'):
                try:
                    self.config_file = os.getenv('HOME') + config_file
                except Exception as ei:
                    print('Exception > {}'.format(ei))
            else:
                self.config_file = "{}/{}".format(self.workdir, config_file)
            
            if not os.path.isfile(self.config_file):
                print ("Configuration file ({}) not exist! Proccess aborted!".format(self.config_file))
                os.sys.exit(1)
        
        config.read(self.config_file)

        for section in config.keys():
            if debug:
                print(config[section])
            if not load_default_config:
                break
            for config_item in default_config.keys():
                if section == 'DEFAULT':
                    if config_item in config[section]:
                        default_config_items[config_item] = config[section][config_item]
                        if debug:
                            print('  - {} = {}'.format(config_item, config[section][config_item]))
                    else:
                        if debug:
                            print("No DEFAULT Config for '{}'".format(config_item))
                            print("Set DEAFULT {} = {}".format(config_item, default_config_items[config_item]))
                        default_config[config_item] = default_config_items[config_item]
                else:
                    if len(running_config_items) == 0:
                        running_config_items = running_config_items
                    if config_item in config[section]:
                        running_config_items[config_item] = config[section][config_item]
                        if debug:
                            print('  - {} = {}'.format(config_item, config[section][config_item]))
                    else:
                        if debug:
                            print("No pve_config for '{}'".format(config_item))
                            print("Set {} = {} [DEFAULT]".format(config_item, default_config_items[config_item]))
                        running_config_items[config_item] = default_config_items[config_item]
        
        self.user = None
        self.ticket = None
        self.token = None
        self.cookies = None
        # self.session = requests.Session()
