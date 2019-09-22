# -*- coding: utf-8 -*-

"""Parsers and downloaders for Bio2BEL CREEDS."""

import itertools as itt

import pandas as pd
from tqdm import tqdm

import bio2bel_hgnc
import bio2bel_mgi
import bio2bel_rgd
from bio2bel.downloading import make_df_getter, make_json_getter
from .constants import (
    GENE_PERTURBATIONS_DATA_PATH, GENE_PERTURBATIONS_DATA_URL, GENE_PERTURBATIONS_METADATA_PATH,
    GENE_PERTURBATIONS_METADATA_URL,
)

__all__ = [
    'get_gene_perturbations_metadata_df',
    'get_gene_perturbations_json',
    'get_gene_perturbations_metadata_preprocessed_df',
    'get_gene_perturbations_preprocessed_df',
]

get_gene_perturbations_metadata_df = make_df_getter(
    GENE_PERTURBATIONS_METADATA_URL,
    GENE_PERTURBATIONS_METADATA_PATH,
)

get_gene_perturbations_json = make_json_getter(
    GENE_PERTURBATIONS_DATA_URL,
    GENE_PERTURBATIONS_DATA_PATH,
)

hgnc_gene_symbol_update = {
    'PARK2': 'PRKN',
    'ERO1L': 'ERO1A',
    'RFWD2': 'COP1',
    'CYR61': 'CCN1',
    'FAM60A': 'SINHCAF',
    'PRKCDBP': 'CAVIN3',
    'VPRBP': 'DCAF1',
    'H3F3A': 'H3-3A',
    'WHSC1': 'NSD2',
}

mgi_gene_symbol_update = {
    'Mut': 'Mmut',
    'Gm10480': 'Bnip3l-ps',
    'Ptrf': 'Cavin1',
    'Mgea5': 'Oga',
    'Mkl2': 'Mrtfb',
    'Ssfa2': 'Itprid2',
    'Rfwd2': 'Cop1',
}


def _get_mappings():
    hgnc_manager = bio2bel_hgnc.Manager()
    if not hgnc_manager.is_populated():
        hgnc_manager.populate()
    hgnc_gene_symbol_to_hgnc_id = hgnc_manager.build_hgnc_symbol_id_mapping()

    mgi_manager = bio2bel_mgi.Manager()
    if not mgi_manager.is_populated():
        mgi_manager.populate()
    mgi_gene_symbol_to_mgi_id = mgi_manager.build_mgi_gene_symbol_to_mgi_id_mapping()

    rgd_manager = bio2bel_rgd.Manager()
    if not rgd_manager.is_populated():
        rgd_manager.populate()
    rgd_gene_symbol_to_rgd_id = rgd_manager.build_rgd_gene_symbol_to_rgd_id_mapping()
    return hgnc_gene_symbol_to_hgnc_id, mgi_gene_symbol_to_mgi_id, rgd_gene_symbol_to_rgd_id


def get_gene_perturbations_preprocessed_df():
    """Get a preprocessed dataframe with all gene perturbations."""
    rows = []
    hgnc_gene_symbol_to_hgnc_id, mgi_gene_symbol_to_mgi_id, rgd_gene_symbol_to_rgd_id = _get_mappings()
    entries = get_gene_perturbations_json()

    entries = tqdm(entries)
    for entry in entries:
        experiment_id = entry['id']
        organism = entry['organism']
        if organism == 'mouse':
            namespace = 'mgi'
            d = mgi_gene_symbol_to_mgi_id
        elif organism == 'rat':
            namespace = 'rgd'
            d = rgd_gene_symbol_to_rgd_id
        elif organism == 'human':
            namespace = 'hgnc'
            d = hgnc_gene_symbol_to_hgnc_id
        else:
            raise ValueError

        it = itt.chain(
            zip(itt.repeat('down'), entry['down_genes']),
            zip(itt.repeat('up'), entry['up_genes']),
        )

        for direction, (gene_symbol, exp) in it:
            gene_id = d.get(gene_symbol)
            if gene_id is None:
                entries.write(
                    f"{experiment_id} ({organism}): can't find {namespace} id for gene symbol {gene_symbol}",
                )
                continue

            rows.append((
                experiment_id,
                namespace,
                gene_id,
                gene_symbol,
                direction,
                exp,
            ))

    return pd.DataFrame(rows, columns=[
        'single_gene_perturbation_experiment_id', 'gene_namespace,' 'gene_id', 'gene_name', 'direction', 'value',
    ])


def get_gene_perturbations_metadata_preprocessed_df(*args, **kwargs):
    """Get a preprocessed dataframe with all gene perturbation experiments' metadata."""
    df = get_gene_perturbations_metadata_df(*args, **kwargs)

    del df['ctrl_ids']
    del df['pert_ids']
    del df['platform']
    del df['chdir_norm']
    del df['version']

    df = df.rename(columns={'id': 'experiment_id'})

    df['pert_type'] = df['pert_type'].map(_update_pert_type)

    # Remove anything missing cell type information (only one as of 2019-09-22)
    df = df[df.cell_type.notna()]

    # Remove human experiments missing human genes (none as of 2019-09-22)
    human_missing_symbol_idx = (df.organism == 'human') & (df.hs_gene_symbol.isna())
    df = df[~human_missing_symbol_idx]

    # Remove mouse experiments missing mouse genes
    mouse_missing_symbol_idx = (df.organism == 'mouse') & (df.mm_gene_symbol.isna())
    df = df[~mouse_missing_symbol_idx]

    # Remove rat experiments missing rat genes (none as of 2019-09-22)
    rat_missing_symbol_idx = (df.organism == 'rat') & (df.mm_gene_symbol.isna())
    df = df[~rat_missing_symbol_idx]

    hgnc_gene_symbol_to_hgnc_id, mgi_gene_symbol_to_mgi_id, rgd_gene_symbol_to_rgd_id = _get_mappings()

    gene_namespaces = []
    gene_ids = []
    gene_symbols = []

    columns = ['hs_gene_symbol', 'mm_gene_symbol', 'organism']
    for human_gene_symbol, mouse_gene_symbol, organism in df[columns].values:
        if organism == 'human':
            gene_namespace = 'hgnc'
            gene_symbol = hgnc_gene_symbol_update.get(human_gene_symbol, human_gene_symbol)
            gene_id = hgnc_gene_symbol_to_hgnc_id.get(gene_symbol)
            if gene_id is None:
                print(f'Could not find hgnc gene symbol: {gene_symbol}')
        elif organism == 'mouse':
            gene_namespace = 'mgi'
            gene_symbol = mgi_gene_symbol_update.get(mouse_gene_symbol, mouse_gene_symbol)
            gene_id = mgi_gene_symbol_to_mgi_id.get(gene_symbol)
            if gene_id is None:
                print(f'Could not find mgi gene symbol: {gene_symbol}')
        elif organism == 'rat':
            gene_namespace = 'rgd'
            gene_symbol = mouse_gene_symbol
            gene_id = rgd_gene_symbol_to_rgd_id.get(gene_symbol)
            if gene_id is None:
                print(f'Could not find rgd gene symbol: {gene_symbol}')
        else:
            raise ValueError(f'Unhandled organism: {organism}')

        gene_namespaces.append(gene_namespace)
        gene_ids.append(gene_id)
        gene_symbols.append(gene_symbol)

    df['gene_namespace'] = gene_namespaces
    df['gene_id'] = gene_ids
    df['gene_symbol'] = gene_symbols
    del df['mm_gene_symbol']
    del df['hs_gene_symbol']

    assert 0 == df.experiment_id.isna().sum()
    assert 0 == df.cell_type.isna().sum()
    assert 0 == df.geo_id.isna().sum()
    assert 0 == df.pert_type.isna().sum()
    assert 0 == df.organism.isna().sum()
    assert 0 == df.gene_namespace.isna().sum()
    assert 0 == df.gene_symbol.isna().sum()
    assert 0 == df.gene_id.isna().sum()

    return df


def _update_pert_type(pert_type):
    if pd.isna(pert_type) or pert_type is None:
        return ''
    if pert_type == 'KO':
        return 'knockout'
    if pert_type == 'KD':
        return 'knockdown'
    if pert_type == 'OE':
        return 'overexpression'
    return pert_type.lower().replace('-', '')
