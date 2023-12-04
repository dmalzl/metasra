# MetaSRA: normalized human sample-specific metadata for the Sequence Read Archive

**This is a fork of the original [MetaSRA-pipeline repository](https://github.com/deweylab/MetaSRA-pipeline) where I fixed a couple of installation and execution issues like missing packages, outdated download links, wrong import statements, disagreement between CVCL ontology versions and a problem with non-unicode characters in ontologies and the specialist lexicon. I also added support of an outputfile and a key, value style JSON input to support indexing with an ID key for in- and output. Furthermore, prediction is sped up by loading the classifier and vectorizer only once and replacing the CVCL ontology tree in the classifier to ensure all keys are present during prediction. For more info please see below**

This repository contains the code implementing the pipeline used to construct the MetaSRA database described in our publication: https://doi.org/10.1093/bioinformatics/btx334.

This pipeline re-annotates key-value descriptions of biological samples using biomedical ontologies.

The MetaSRA can be searched and downloaded from: http://metasra.biostat.wisc.edu/

## Classifier holding its own copy of the CVCL ontology

The setup of the the pipeline mainly prepares the necessary data by downloading the different ontologies and processing them in a way the pipeline can read and build all the string matching tries etc. A particular one of these ontologies, the CVCL, is not only used during metadata normalisation but also during sample type prediction. When setting up the pipeline it always downloads the current version of the ontologies needed. However, the classifier comes as a pretrained model which is loaded from a pickled (actually `dill` but same same) file and unfortunately contains it's own copy of the CVCL ontology graph used during training. Checking the code, the training process is not really influenced by the ontology as it is not used for training anyway but just for prediction. Therefore, we can savely exchange the old copy with the new version. This fixed any missing ontology terms that would otherwise cause a `KeyError` during prediction.

## Pipeline fails when encountering non-unicode character

After fixing the most obvious things such as missing or wrong import statements as well as outdated download links, the pipeline seemed to fail
on a couple of samples which, after a bit of investigation, apparently contained non-unicode characters that caused one of the normalization stages
to fail. To prevent this I first tried to catch and correct the error during runtime but soon realised that the problem was also causing problems
with prediction. Therefore, I opted to simply mapping all non-unicode character contained in the ontologies as well as the specialist lexicon to their
closest unicode/ascii representation with [`unidecode`](https://pypi.org/project/Unidecode/). This happens during setup and therefore does not require
any code changes. **The caveat here is that you also need to do the same for your input data.** Comparing runs with and without non-unicode characters showed that most if not all samples are mapped to the same ontology terms without reduction of prediction accuracy and in some cases also improved prediction.

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
