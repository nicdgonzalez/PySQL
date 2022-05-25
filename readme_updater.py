from typing import List

file: str = 'README.md'
terminator: str = '```'

with open(file, 'r') as f:

    # Storing a copy of the original content:
    file_name, ext = file.rsplit('.', maxsplit=1)
    with open(f'{file_name}.copy.{ext}', 'w+') as copy:
        copy.write(open(file, 'r').read())

    content: List[str] = []
    is_skipping_line: bool = False

    for line in f.readlines():

        if (is_skipping_line) and (line.strip() == terminator):
            content.append(line.strip('\n'))
            is_skipping_line = False

        elif is_skipping_line:
            continue

        elif ('file::' in line.lower()):
            is_skipping_line = True
            content.append(line.strip())
            content_file = [
                x.strip() for x
                in line.rsplit(':', maxsplit=1)
            ][1]

            with open(content_file, 'r') as f:
                content.append(
                    '\n'.join(
                        [line.strip('\n') for line in f.readlines()]
                    )
                )

        else:
            content.append(line.strip('\n'))

    content: str = '\n'.join(content)

    with open(file, 'w+') as f:
        f.write(content)
