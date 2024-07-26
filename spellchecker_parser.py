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
            else:
                if line.startswith('<text>'):
                    continue
                errors[current_file].append(line.strip())

    return errors

def format_errors(errors):
    formatted_errors = []
    folder_errors = {}

    for file, errs in errors.items():
        parts = file.split('/')
        if len(parts) == 1:
            root = 'root'
            folder_errors.setdefault(root, []).append(f'/{file} :\n{"\n".join(errs)}')
        else:
            folder = parts[0]
            formatted_errors.append(f"{folder}:\n{file} :\n{'\n'.join(errs)}")

    result = []
    for folder, files in folder_errors.items():
        result.append(f"{folder}:")
        result.extend(files)

    return result

def run_spell_check(filename):
    result = subprocess.run(['aspell', 'list', '--mode=markdown', filename], capture_output=True, text=True)
    return result.stdout

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

    spell_check_result = run_spell_check(output_filename)
    print(spell_check_result)

if __name__ == "__main__":
    main()
