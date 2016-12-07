import os
import ConfigParser
import constants

def readconf():
    config = ConfigParser.ConfigParser()
    config.read('/etc/ansibengine.conf')
    return config


def project_path(type):
    config = readconf()
    if type == 'project':
        path = config.get('paths', 'project_path')
    elif type == 'play':
        path = config.get('paths', 'project_path')
    elif type == 'resultout':
        path = config.get('paths', 'result_path')
    return os.listdir(path)

def get_vars(type):
    config = readconf()
    if type == 'project':
        vars = config.get(constants.ENVIRONMENT, 'project_path')
    elif type == 'play':
        vars = config.get(constants.ENVIRONMENT, 'project_path')
    elif type == 'resultout':
        vars = config.get(constants.ENVIRONMENT, 'result_path')
    elif type == 'baseurl':
        vars = config.get(constants.ENVIRONMENT, 'baseurl')
    elif type == 'basepath':
        vars = config.get(constants.ENVIRONMENT, 'basepath')
    elif type == 'tracerouterusername':
	vars = config.get(constants.ENVIRONMENT, 'tracerouterusername')
    elif type == 'tracerouterpass':
	vars = config.get(constants.ENVIRONMENT, 'tracerouterpass')
    elif type == 'orionusername':
        vars = config.get(constants.ENVIRONMENT, 'orionusername')
    elif type == 'orionpass':
        vars = config.get(constants.ENVIRONMENT, 'orionpass')
    elif type == 'orionurl':
        vars = config.get(constants.ENVIRONMENT, 'orionurl')
    elif type == 'ipamsource':
        vars = config.get(constants.ENVIRONMENT, 'ipamsource')
    elif type == 'ipamrouterusername':
        vars = config.get(constants.ENVIRONMENT, 'ipamrouterusername')
    elif type == 'ipamrouterpass':
        vars = config.get(constants.ENVIRONMENT, 'ipamrouterpass')
    elif type == 'sourcerouterusername':
        vars = config.get(constants.ENVIRONMENT, 'sourcerouterusername')
    elif type == 'sourcerouterpass':
        vars = config.get(constants.ENVIRONMENT, 'sourcerouterpass')
    elif type == 'sourcerouterip':
        vars = config.get(constants.ENVIRONMENT, 'sourcerouterip')
    return vars
