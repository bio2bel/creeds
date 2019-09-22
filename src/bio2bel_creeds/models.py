# -*- coding: utf-8 -*-

"""SQLAlchemy models for Bio2BEL CREEDS."""

import logging

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import relationship

from .constants import MODULE_NAME

__all__ = [
    'Base',
]

logger = logging.getLogger(__name__)

Base: DeclarativeMeta = declarative_base()

SINGLE_GENE_PERTURBATION_EXPERIMENT_TABLE_NAME = f'{MODULE_NAME}_singleGenePerturbationExperiment'
SINGLE_GENE_PERTURBATION_TABLE_NAME = f'{MODULE_NAME}_singleGenePerturbation'


class SingleGenePerturbationExperiment(Base):
    """Represents a single gene perturbation experiment."""

    __tablename__ = SINGLE_GENE_PERTURBATION_EXPERIMENT_TABLE_NAME
    id = Column(Integer, primary_key=True)

    experiment_id = Column(String(255), nullable=False, doc='The CREEDS identifier for the experiment')
    cell_type = Column(Text, nullable=False, doc='The cell type used in the experiment')
    curator = Column(String(255), nullable=True, doc='The curator for the experiment')
    geo_id = Column(String(255), nullable=False, doc='The GEO identifier of the experiment')
    organism = Column(String(16), nullable=False, doc='The organism in which the experiment was conducted')
    pert_type = Column(String(255), nullable=False, doc='The type of perturbation that was used')
    gene_namespace = Column(String(255), nullable=False,
                            doc='The namespace of the gene identifier appropriate for the organism')
    gene_id = Column(String(255), nullable=False, doc='The identifier of the gene that was perturbed')
    gene_symbol = Column(String(255), nullable=False, doc='The gene symbol of the gene that was perturbed')


class SingleGenePerturbation(Base):
    """Represents a single gene perturbation."""

    __tablename__ = SINGLE_GENE_PERTURBATION_TABLE_NAME
    id = Column(Integer, primary_key=True)

    single_gene_perturbation_experiment_id = Column(
        Integer, ForeignKey(f'{SingleGenePerturbationExperiment.__tablename__}.id'), nullable=False,
    )
    single_gene_perturbation_experiment = relationship(SingleGenePerturbationExperiment)

    gene_namespace = Column(String(255), nullable=False)
    gene_id = Column(String(255), nullable=False, doc='The identifier of the gene that was measured')
    gene_symbol = Column(String(255), nullable=False, doc='The gene symbol of the gene that was measured')
    direction = Column(String(4), nullable=False)
    value = Column(Float, nullable=False)
