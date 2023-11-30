from unidecode import unidecode


def convert_to_ascii_on_unicode_error(string):
    unicode_string = string.decode('utf-8')
    try:
        str(unicode_string)
    
    except UnicodeError:
        print "Encountered unicode to string error in {}. Converting to closest ASCII representation".format(string)
        string = unidecode(unicode_string)
    
    return string


def remove_non_unicode_characters(path_to_file):
    lines = []
    with open(path_to_file, 'r') as f:
        for line in f:
            line = convert_to_ascii_on_unicode_error(line)
            lines.append(line)
    
    with open(path_to_file, 'w') as f:
        for line in lines:
            f.write(line)
