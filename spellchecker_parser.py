import sys
import subprocess

def parse_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    in_error_section = False
    current_file = ""
    errors = {}

    for line in lines:
        if line.startswith('> Processing:'):
            current_file = line.split(': ', 1)[1].strip()
        elif line.startswith('Misspelled words:'):
            in_error_section = True
            if current_file not in errors:
                errors[current_file] = []
        elif in_error_section:
            if line.strip() == '--------------------------------------------------------------------------------':
                in_error_section = False
            elif not line.startswith('<text>'):
                errors[current_file].append(line.strip())

    return errors

def format_errors(errors):
    formatted_errors = {}

    for file, errs in errors.items():
        # Split path to determine if it should be grouped under root or subfolder
        if '/' in file:
            parts = file.split('/')
            folder = parts[0]
            rest_of_path = '/'.join(parts[1:])
            if folder not in formatted_errors:
                formatted_errors[folder] = []
            formatted_errors[folder].append(f'/{rest_of_path} :\n' + "\n".join(errs))
        else:
            if 'root' not in formatted_errors:
                formatted_errors['root'] = []
            formatted_errors['root'].append(f'/{file} :\n' + "\n".join(errs))

    result = []
    for folder, entries in formatted_errors.items():
        result.append(f"{folder}:")
        result.extend(entries)

    return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        return

    input_filename = sys.argv[1]
    errors = parse_file(input_filename)
    formatted_errors = format_errors(errors)

    output_filename = 'errors_output.txt'
    with open(output_filename, 'w') as outfile:
        for error in formatted_errors:
            outfile.write(error + '\n')

if __name__ == "__main__":
    main()
