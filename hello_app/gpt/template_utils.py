from ._arm import CREATE_APP_TEMPLATE

def create_app_template():
    template = CREATE_APP_TEMPLATE
    return template

def create_connection_template():
    template = CREATE_APP_TEMPLATE
    return template

get_template = {
    'create resource': {
        'web app': create_app_template,
    },
    'connect resources':create_connection_template
}
