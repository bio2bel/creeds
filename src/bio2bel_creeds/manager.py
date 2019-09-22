# -*- coding: utf-8 -*-

"""Manager for Bio2BEL CREEDS."""

import logging
from typing import Mapping

from bio2bel import AbstractManager
from bio2bel.manager.flask_manager import FlaskMixin
from .constants import MODULE_NAME
from .models import Base, SingleGenePerturbation, SingleGenePerturbationExperiment
from .parser import get_gene_perturbations_metadata_preprocessed_df, get_gene_perturbations_preprocessed_df

__all__ = [
    'Manager',
]

logger = logging.getLogger(__name__)


class Manager(AbstractManager, FlaskMixin):
    """Manages the Bio2BEL CREEDS database."""

    module_name = MODULE_NAME
    flask_admin_models = [SingleGenePerturbationExperiment, SingleGenePerturbation]
    _base = Base

    def count_gene_perturbation_experiments(self) -> int:
        """Count the number of single gene perturbation experiments in the database."""
        return self._count_model(SingleGenePerturbationExperiment)

    def count_gene_perturbations(self) -> int:
        """Count the number of single gene perturbations in the database."""
        return self._count_model(SingleGenePerturbation)

    def is_populated(self) -> bool:
        """Check if the Bio2BEL CREEDS database is populated."""
        return 0 < self.count_gene_perturbation_experiments()

    def summarize(self) -> Mapping[str, int]:
        """Summarize the contents of the Bio2BEL CREEDS database."""
        return dict(
            gene_perturbation_experiments=self.count_gene_perturbation_experiments(),
            gene_perturbations=self.count_gene_perturbations(),
        )

    def populate(self) -> None:
        """Populate the Bio2BEL CREEDS database."""
        gene_perturbations_metadata_df = get_gene_perturbations_metadata_preprocessed_df(())
        gene_perturbations_metadata_df.to_sql(
            SingleGenePerturbationExperiment.__tablename__, self.engine,
            if_exists='append', index=False,
        )
        self.session.commit()

        logger.info('Getting mapping from experiment ids to database ids')
        experiment_id_to_id = dict(self.session.query(
            SingleGenePerturbationExperiment.experiment_id,
            SingleGenePerturbationExperiment.id,
        ).all())

        logger.info('Getting perturbation data')
        gene_perturbations_df = get_gene_perturbations_preprocessed_df()

        logger.info('Keeping only experiments that have been stored')
        gene_perturbations_df = gene_perturbations_df[
            gene_perturbations_df['single_gene_perturbation_experiment_id'].isin(experiment_id_to_id)]

        logger.info('Mapping experiments')
        gene_perturbations_df['single_gene_perturbation_experiment_id'] = \
            gene_perturbations_df['single_gene_perturbation_experiment_id'].map(experiment_id_to_id.get)

        gene_perturbations_df.to_sql(
            SingleGenePerturbation.__tablename__, self.engine,
            if_exists='append', index=False,
        )
        self.session.commit()
