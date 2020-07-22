from abc import ABC

from ..utils import get_augmentation
from .dataset import (
    DHP3DJointsDataset,
    DHP19AutoEncoderDataset,
    DHP19ClassificationDataset,
    DHPHeatmapDataset,
    DHPJointsDataset,
)
from .params_utils import get_dataset_params

__all__ = [
    'ClassificationConstructor', 'AutoEncoderConstructor',
    'Joints3DConstructor', 'JointsConstructor', 'HeatmapConstructor'
]


class BaseConstructor(ABC):
    def __init__(self, hparams, dataset_class):
        self.dataset_class = dataset_class
        self.train_params = {}
        self.val_params = {}
        self.test_params = {}
        self.set_base(hparams)

    def _set_for_all(self, key, value):
        self._set_for_train(key, value)
        self._set_for_val(key, value)
        self._set_for_test(key, value)

    def _set_for_train(self, key, value):
        self.train_params[key] = value

    def _set_for_val(self, key, value):
        self.val_params[key] = value

    def _set_for_test(self, key, value):
        self.test_params[key] = value

    def set_base(self, hparams):
        preprocess_train, self.train_aug_info = get_augmentation(
            hparams.augmentation_train)
        preprocess_val, self.val_aug_info = get_augmentation(
            hparams.augmentation_test)

        self.params = get_dataset_params(hparams.dataset)
        self._set_for_all('file_paths', self.params['file_paths'])
        self._set_for_train('indexes', self.params['train_indexes'])
        self._set_for_val('indexes', self.params['val_indexes'])
        self._set_for_test('indexes', self.params['test_indexes'])

        self._set_for_train('transform', preprocess_train)
        self._set_for_val('transform', preprocess_val)
        self._set_for_test('transform', preprocess_val)

    def get_datasets(self):
        return self.dataset_class(**self.train_params), self.dataset_class(
            **self.val_params), self.dataset_class(**self.test_params)


class ClassificationConstructor(BaseConstructor):
    def __init__(self, hparams):
        super(ClassificationConstructor, self).__init__(hparams)

    def get_datasets(self):
        return DHP19ClassificationDataset(
            **self.train_params), DHP19ClassificationDataset(
                **self.val_params), DHP19ClassificationDataset(
                    **self.test_params)


class JointsConstructor(BaseConstructor):
    def __init__(self, hparams):
        super(JointsConstructor, self).__init__(hparams, DHPJointsDataset)
        self._set_for_all('n_joints', hparams.dataset.n_joints)
        self._set_for_all('labels_dir', hparams.dataset.joints_dir)


class Joints3DConstructor(BaseConstructor):
    def __init__(self, hparams):
        super(Joints3DConstructor, self).__init__(hparams, DHP3DJointsDataset)

        self._set_for_all('n_joints', hparams.dataset.n_joints)
        self._set_for_all('labels_dir', hparams.dataset.joints_dir)
        self._set_for_train('height', self.train_aug_info.height)
        self._set_for_train('width', self.train_aug_info.width)
        self._set_for_val('height', self.val_aug_info.height)
        self._set_for_val('width', self.val_aug_info.width)
        self._set_for_test('height', self.val_aug_info.height)
        self._set_for_test('width', self.val_aug_info.width)


class HeatmapConstructor(BaseConstructor):
    def __init__(self, hparams):
        super(HeatmapConstructor, self).__init__(hparams, DHPHeatmapDataset)

        self._set_for_all('n_joints', hparams.dataset.n_joints)
        self._set_for_all('labels_dir', hparams.dataset.joints_dir)


class AutoEncoderConstructor(BaseConstructor):
    def __init__(self, hparams):
        super(AutoEncoderConstructor, self).__init__(hparams,
                                                     DHP19AutoEncoderDataset)

        self._set_for_all('n_joints', hparams.dataset.n_joints)
        self._set_for_all('labels_dir', hparams.dataset.joints_dir)