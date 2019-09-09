import pathlib
import re

import exifread

SIMULATE = True
path_to_folder = r'U:\Fotos'

extensions = ['.jpg']  #, '.mp4']
count = 0


def get_new_name(file):
    new_name = None
    ext = pathlib.Path(file).suffix
    filename = pathlib.Path(file).stem
    filename_ext = pathlib.Path(file).name
    # print(f'filename: {filename}')
    with open(file, 'rb') as f:
        tags = exifread.process_file(f, details=False)

    if tags:
        exif_time = str(tags['Image DateTime'])
        new_name = exif_time.replace(':', '-')  # 2019-07-08 17-33-52
    elif re.match('\d{8}_\d{6}\.', filename_ext):
        date = filename[0:4] + '-' + filename[4:6] + '-' + filename[6:8]
        time = filename[9:11] + '-' + filename[11:13] + '-' + filename[13:15]
        new_name = date + ' ' + time

    # print(f'new_name: {new_name}')

    if new_name:
        if SIMULATE:
            return f'{new_name}{ext}'
        already_exists = (pathlib.Path(path_to_folder) / f'{new_name}{ext}').exists()
        if not already_exists:
            new_name = f'{new_name}{ext}'
            return f'{new_name}'
        else:
            while already_exists:
                new_name_parts = new_name.split('-')
                index = str(int(new_name_parts[-1]) + 1)
                if len(index) == 1:
                    index = '0' + index
                new_name = '-'.join([*new_name_parts[:-1], index])

                already_exists = (pathlib.Path(path_to_folder) / f'{new_name}{ext}').exists()

        new_name = f'{new_name}{ext}'
        return f'{new_name}'


for extension in extensions:
    print(f'working on {extension}')
    for file in pathlib.Path(path_to_folder).rglob(f'*{extension}'):
        f = pathlib.Path(file)
        file_folder = f.parent
        filename_ext = f.name
        if not SIMULATE:
            if re.match('\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}.', filename_ext):
                continue

        new_file = get_new_name(file)

        if SIMULATE:
            s = ''
            if filename_ext[:11] != new_file[:11]:
                # s = '\tXXX'
                print(f'filename old: {filename_ext}')
                print(f'filename new: {new_file}{s}')
                print(f'{file_folder}')
                print('-------------------------------------')

        if not SIMULATE:
            if new_file:
                # print(file)
                new_name_path = pathlib.Path(file_folder) / f'{new_file}'
                pathlib.Path(file).replace(new_name_path)

print('done')
