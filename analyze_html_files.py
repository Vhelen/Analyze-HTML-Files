import json
import os
import pathlib
import getopt
import sys
from bs4 import BeautifulSoup


def check_args(program_name, argv):
    extensions = ['html']
    tags = ['']
    output_file = "results"
    directory = "files_to_analyze"

    try:
        opts, args = getopt.getopt(argv, "ht:e:d:o:", ["help", "tag=", "extension=", "directory=", "output="])
    except getopt.GetoptError:
        print(f'{program_name} -e <extension> -d <directory> -o <output>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print(f'{program_name} -t <tag> [-e <extension>] [-d <directory>] [-o <output>]')
            print('-t --tag         Tag name to retrieve, separate with a comma to put multiple file extensions')
            print('-e --extension   File extension to analyze, separate with a comma to put multiple file extensions')
            print('-d --directory   Directory to analyze, by default files_to_analyze')
            print('-o --output      Output file name, by default results')

            sys.exit()

        elif opt in ["-e", "--extension"]:
            if ',' in arg:
                extensions = arg.split(',')
            else:
                extensions = [arg]

        elif opt in ["-t", "--tag"]:
            if ',' in arg:
                tags = arg.split(',')
            else:
                tags = [arg]

        elif opt in ["-d", "--directory"]:
            output_file = arg

        elif opt in ["-o", "--output"]:
            output_file = arg

    if tags == ['']:
        print(f'{program_name} -t <tag> [-e <extension>] [-d <directory>] [-o <output>]')
        print("No tag was specified")

        sys.exit(2)

    return tags, extensions, directory, output_file


def add_tag(tags_dict, type_tag, tag_to_add, file_tag):
    if file_tag not in tags_dict:
        tags_dict[file_tag] = {}

    if type_tag not in tags_dict[file_tag]:
        tags_dict[file_tag][type_tag] = []

    tags_dict[file_tag][type_tag].append(tag_to_add)

    return tags_dict


if __name__ == '__main__':
    tags_to_analyze, file_extensions_to_analyze, directory_to_analyze, output_file_name = check_args(sys.argv[0], sys.argv[1:])

    files_to_analyze = []

    # Check if directory exist
    if not os.path.isdir(directory_to_analyze):
        print(f"No directory {directory_to_analyze}")
        sys.exit(2)

    # Parse the directory to find files to analyze
    for path, sub_dirs, files in os.walk(directory_to_analyze):
        for filename in files:
            file = os.path.join(path, filename)
            file_extension = pathlib.Path(file).suffix

            if file_extension[1:] in file_extensions_to_analyze:
                files_to_analyze.append(file)

    # Check if files were found
    if not files_to_analyze:
        print(f"No files found in {directory_to_analyze} for extension(s) {file_extensions_to_analyze}")
        sys.exit(2)

    results_tag = {}
    for file in files_to_analyze:
        with open(file, 'r', encoding='utf8') as f:
            file_content = f.read()
            bs_file_content = BeautifulSoup(file_content, features="html.parser")

        # Parse each tag
        for tag in tags_to_analyze:
            tag_found = bs_file_content.find_all(tag)
            if tag_found:
                for bs_tag in tag_found:
                    results_tag = add_tag(results_tag, tag, bs_tag.prettify(), file)

    with open(f'{output_file_name}.json', 'w') as fp:
        json.dump(results_tag, fp)
















