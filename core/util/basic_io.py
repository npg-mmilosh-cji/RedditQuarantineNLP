import os
import json
import csv
import gensim


def read_json_to_dict(file_path):
    """"
    read json file to dict obj

    input:
        (str) file_path: path to file
    output:
        (dict) data read from file
    """
    with open(file_path) as f:
        data_dict = json.load(f)
    return data_dict


def write_dict_to_json(output_file_path, data):
    """
    write dictionary to file

    input:
        (str) output_file_path: path to output file
        (dict) data: data to write
    """
    with open(output_file_path, 'w') as outfile:
        json.dump(data, outfile)


def read_csv_to_list(file_path):
    """"
    read csv to list of list

    input:
        (str) file_path: path to file

    output:
        list of list containing data from file

    """
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        return list(reader)


def write_list_to_csv(lines, file_name):
    """
    write list to csv
    :param lines: list of data to write to csv
    :param file_name: output file name
    """
    with open(file_name, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)


def load_lda_models(path_to_model_directory):
    """
    Read saved lda models from a directory
    Returns a dict with key number of topics, value trained model
    """
    trained_models = dict()
    for num_topics in range(5, 30, 2):
        model_path = os.path.join(path_to_model_directory ,('lda_models/lda_' + str(num_topics) + '_topics'))
        print("Loading LDA(k=%d) from %s" % (num_topics, model_path))
        trained_models[num_topics] = gensim.models.LdaMulticore.load(model_path)
    return trained_models

