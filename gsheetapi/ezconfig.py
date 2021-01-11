import os
import glob
import json
from configparser import ConfigParser

class EZConfig:
    def __init__(self, config_file = None, default_config = None, confdir = 'conf.d', workdir = None, debug = False):

        print('localtion: {}'.format(os.path.dirname(os.path.abspath(__file__))))
        
        load_default_section = False
        loaded_config = ConfigParser()
        
        self.config = ConfigParser()
        self.confdir = confdir

        if workdir is None:
            self.workdir = os.path.dirname(os.path.abspath(__file__))
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
                        loaded_config = default_config
                        loaded_config.write(create_config_file)

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
        
        loaded_config.read(self.config_file)
        self.config = loaded_config

        for config_section in self.default_config.keys():
            
            if debug:
                print(config_section)
            if not load_default_section:
                if config_section == 'DEFAULT':
                    if debug:
                        print('LOAD_DEFAULT_SECTION = False')
                    continue
            for config_item in self.default_config[config_section]:
                if config_item in loaded_config[config_section]:
                    self.config[config_section][config_item] = loaded_config[config_section][config_item]
                    # if debug:
                    #     print('  - {} = {}'.format(config_item, loaded_config[config_section][config_item]))
                else:
                    self.config[config_section][config_item] = default_config[config_section][config_item]
                    if debug:
                        print("No loaded_config item for '{}'".format(config_item))
                        print("Set default {} = {}".format(config_item, default_config[config_section][config_item]))
                
                if debug:
                    print('  - {} = {}'.format(config_item, self.config[config_section][config_item]))
    
    def get(self, section = None, item = None, debug = False):
        value = None
        if section in self.config.sections():
            if item in self.config[section]:
                value = self.config[section][item]
            else:
                value = None
        else:
            value = None
        
        return value
    
def main():
    
    workdir = os.path.dirname(os.path.abspath(__file__))
    print('main workdir: {}'.format(workdir))

    default_config = ConfigParser()
    default_config.read_string("""
    [PVE_CONFIG]
    pve_node = pve
    pve_host = https://localhost
    pve_port = 8006
    pve_user = root
    pve_pass = admin
    pve_realm = pam
    pve_cacert = certs/pve-root-ca.pem
    pve_endpoint = /api2/json/access/ticket
    verify_ssl = True

    [GOOGLE_SHEET]
    scope = https://www.googleapis.com/auth/spreadsheets.readonly
    spreadsheet_id = 0123456789AbCdEfGhIjKlMnOpQrStUvWxyz
    sheet_id = 1234567890
    range_name = Sheet1!A2:A3
    """)

    ec = EZConfig(default_config = default_config, debug = True)
    print(ec.config['PVE_CONFIG']['pve_node'])

if __name__ == "__main__":
    main()