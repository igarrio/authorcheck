import configparser

cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

cfg_editors = cfg['EDITORS']['id']
admin_id = int(cfg['ADMIN']['id'])
editors = [int(num.strip()) for num in cfg_editors.split(',')]
