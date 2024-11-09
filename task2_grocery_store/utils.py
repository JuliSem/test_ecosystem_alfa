import os


def generic_image_path(instance, filename):
    '''Генерация нового пути для изображений.'''

    model_name = instance._meta.model_name
    extension = filename.split('.')[-1]
    new_filename = f'{instance.slug}.{extension}'
    return os.path.join(model_name, new_filename)
