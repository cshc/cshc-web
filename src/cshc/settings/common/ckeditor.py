def get_ckeditor_config(static_url):
    return {
        'default': {
            'removePlugins': 'stylesheetparser',
            'allowedContent': True,
            'customConfig': "{}js/ckeditor-custom.js".format(static_url),
        },
    }
