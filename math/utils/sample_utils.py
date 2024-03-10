import shutil
import numpy as np

from utils.file_utils import *


def sample_data(filepath, sample_size=100):
    data = read_data(filepath)
    if type(data) == dict:
        return data
    elif type(data) == list:
        return np.random.choice(data, size=sample_size, replace=False)


def sample_files(input_dir, output_dir, sample_size=100):
    # Sample `sample_size` question files from parent topic directory
    question_files = list(input_dir.glob("*.json"))
    sample = np.random.choice(question_files, size=sample_size, replace=False)

    # Clear and Create output directory for sampled question files
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    # Copy the sampled question files to the output directory
    for question_file in sample:
        shutil.copy(question_file, output_dir / question_file.name)
