# -*- coding: utf-8 -*-

"""Constants for Bio2BEL CREEDS."""

import os

from bio2bel import get_data_dir

__all__ = [
    'MODULE_NAME',
    'DATA_DIR',
    'GENE_PERTURBATIONS_METADATA_URL',
    'GENE_PERTURBATIONS_METADATA_PATH',
    'GENE_PERTURBATIONS_DATA_URL',
    'GENE_PERTURBATIONS_DATA_PATH',
]

MODULE_NAME = 'creeds'
DATA_DIR = get_data_dir(MODULE_NAME)

# Manual single gene perturbations
GENE_PERTURBATIONS_METADATA_URL = 'http://amp.pharm.mssm.edu/CREEDS/download/single_gene_perturbations-v1.0.csv'
GENE_PERTURBATIONS_METADATA_PATH = os.path.join(DATA_DIR, GENE_PERTURBATIONS_METADATA_URL.split('/')[-1])

GENE_PERTURBATIONS_DATA_URL = 'http://amp.pharm.mssm.edu/CREEDS/download/single_gene_perturbations-v1.0.json'
GENE_PERTURBATIONS_DATA_PATH = os.path.join(DATA_DIR, GENE_PERTURBATIONS_DATA_URL.split('/')[-1])
