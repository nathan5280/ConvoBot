import logging

from convobot.manipulate.CountManipulator import CountManipulator
from convobot.manipulate.NumpyManipulator import NumpyManipulator

logger = logging.getLogger(__name__)
manipulators = {'count-manipulator': CountManipulator,
                'numpy-manipulator': NumpyManipulator}

# TODO: Replace with dynamic module loading.
# TODO: Create a model where the configuration can support a full pipeline
# of manipulators.  Resize --> RBBA | Grayscale --> Numpy Stack

class ManipulatorLoader(object):
    '''
    Create the manipulator named in the configuration file.  This decouples
    the code from the configuration.  It could be handled in a 'case' statement,
    but is handled through the lookup in the manipulators list. This could also
    follow an Examplar patter and each of the classes when loaded would register
    in the list.
    '''
    def __init__(self, cfg_mgr):
        '''
        Args:
            cfg_mgr: Global configuration manager

        Return: None
        '''
        logger.debug('Initializing')

        # Keep track of the configurations for the manipulators.
        # Currently none of this is used by the loader.
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_manipulate_cfg()

    def get_manipulator(self):
        '''
        Construct the manipulator based on the configuration.

        Return: The constructed manipulator.
        '''
        name = self._cfg['Name']
        logger.debug('Loading manipulator: %s', name)
        return manipulators[name](self._cfg_mgr)
