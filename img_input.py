import configparser


config_object = configparser.ConfigParser()
config_object.read('input.ini')

input_parameter = config_object['INPUT']

img_folder = input_parameter['img_folder']



