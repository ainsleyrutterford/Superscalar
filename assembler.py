def strip_comments(assembly):
    stripped_assembly = ''
    for line in assembly.splitlines():
        line = line.strip()
        position = line.find(';')
        if len(line) > 0:
            if position > 0:
                stripped_assembly += line[:position].strip() + '\n'
            elif position < 0:
                stripped_assembly += line + '\n'
    return stripped_assembly


def replace_labels(assembly):
    labels = {}
    offset = 0
    final_assembly = ''
    for i, line in enumerate(assembly.splitlines()):
        if line.endswith(':'):
            labels[line[:-1]] = i - offset
            offset += 1
        else:
            final_assembly += line + '\n'
    for label, num in labels.items():
        final_assembly = final_assembly.replace("'" + label + "'", str(num))
    return final_assembly
