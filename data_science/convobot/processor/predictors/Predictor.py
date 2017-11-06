import logging
import glob
from abc import ABCMeta
import pandas as pd
import os

from convobot.processor.Processor import Processor
from convobot.processor.manipulator import SplitDataMgr

logger = logging.getLogger(__name__)


class Predictor(Processor, metaclass=ABCMeta):
    """
    Base Predictor.
    """

    def __init__(self, name, cfg):
        """
        Create the base predictor.

        :param name: Name of the predictor
        :param cfg: Configuration parameters for the predictor
        """
        super().__init__(name, cfg)
        self._model = None
        self._split_data_mgr: SplitDataMgr = None
        self._pred_dir_path = self.configuration['pred-dir-path']

        # Get the max index for the files in the prediction directory and start the index based on that.
        # Todo: Sort out what functionality goes in the TrainPredictor and what goes in the Standalone Predictor.
        # this index really belongs with the training tracker predictor.
        pred_file_names = sorted(glob.glob(self._pred_dir_path + '/*.csv'))
        if len(pred_file_names) > 0:
            self._index = int(os.path.splitext(os.path.split(pred_file_names[-1])[1])[0]) + 1
        else:
            self._index = 0

    def reset(self):
        pass

    def sweep(self):
        pred_file_names = glob.glob(self._pred_dir_path + '*')
        for pred_file_name in pred_file_names:
            os.remove(pred_file_name)

    def process(self) -> None:
        """
        Predict against the validation data set and save results to disk.

        :return: None
        """

        pred_file_path = os.path.join(self._pred_dir_path, '{0:04d}'.format(self._index) + '.csv')
        self._index += 1

        pred = self._model.predict(self._split_data_mgr.validation_image, batch_size=1)

        val_df = pd.DataFrame(self._split_data_mgr.validation_label)
        pred_df = pd.DataFrame(pred)
        results_df: pd.DataFrame = pd.concat((val_df, pred_df), axis=1)
        results_df.columns = [
            'vTheta',
            'vRadius',
            'vAlpha',
            'pTheta',
            'pRadius',
            'pAlpha']

        logger.debug('Saving prediction results: %s', pred_file_path)
        results_df.to_csv(pred_file_path, ',', index=False)
