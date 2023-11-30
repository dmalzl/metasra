**This is a fork of the original [MetaSRA-pipeline repository](https://github.com/deweylab/MetaSRA-pipeline) where I fixed a couple of installation and execution issues like missing packages, outdated download links, wrong import statements, disagreement between CVCL ontology versions (the installation loads the current ontology version while the classifier relies on an older one that is pickled with it) and a problem with non-unicode characters in ontologies and the specialist lexicon (essentially I used the [`unidecode`](https://pypi.org/project/Unidecode/) package to map those terms that contain characters that result in a UnicodeDecodeError (mostly synonyms) to their closest ASCII representation. This happens during setup and might affect your mapping if your data contains such characters. Therefore make sure to process your data similarly). I also added support of an outputfile and a key, value style JSON input to support indexing with an ID key for in- and output. Furthermore, prediction is sped up by loading the classifier and vectorizer only once and replacing the CVCL ontology tree in the classifier to ensure all keys are present during prediction (otherwise raises KeyError due to new additions in newer versions of the ontology)**

# MetaSRA: normalized human sample-specific metadata for the Sequence Read Archive

This repository contains the code implementing the pipeline used to construct the MetaSRA database described in our publication: https://doi.org/10.1093/bioinformatics/btx334.

This pipeline re-annotates key-value descriptions of biological samples using biomedical ontologies.

The MetaSRA can be searched and downloaded from: http://metasra.biostat.wisc.edu/

## Dependencies

This project requires the following Python libraries:
- numpy (http://www.numpy.org)
- scipy (https://www.scipy.org/scipylib/)
- scikit-learn (http://scikit-learn.org/stable/)
- setuptools (https://pypi.python.org/pypi/setuptools)
- marisa-trie (https://pypi.python.org/pypi/marisa-trie)
- nltk (https://www.nltk.org/)
- dill (https://pypi.org/project/dill/)

## Setup

In order to run the pipeline, a few external resources must be downloaded and configured.  First, set up the PYTHONPATH environment variable to point to the directory containing the map_sra_to_ontology directory as well as to the bktree directory.  Then, to set up the pipeline, run the following commands:
  
    cd ./setup_map_sra_to_ontology
    ./setup.sh

This script will download the latest ontology OBO files, the SPECIALIST Lexicon files, and configure the ontologies to work with the pipeline.

## Usage

The pipeline can be run on a set of sample-specific key-value pairs
using the run_pipeline.py script. This script is used as follows:

    python run_pipeline.py <input key-value pairs JSON file> <name of output JSON file>

The script accepts as input a JSON file storing a list of sets of key-value pairs.
For example, the pipeline will accept a file with the following content:

    {
      "P352_141": {   
        "age": "48",
        "bmi": "24",
        "gender": "female",
        "source_name": "vastus lateralis muscle_female",
        "tissue": "vastus lateralis muscle"
      },
      "P352_141": {   
        "age": "29",
        "bmi": "30",
        "gender": "male",
        "source_name": "vastus lateralis muscle_female",
        "tissue": "vastus lateralis muscle"
      }
    }
