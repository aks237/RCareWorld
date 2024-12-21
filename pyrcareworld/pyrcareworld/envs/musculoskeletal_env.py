"""Musculoskeletal environment to test musculoskeletal analysis"""
from pyrcareworld.attributes.musculoskeletal_attr import MusculoskeletalAttr
from pyrcareworld.envs.base_env import RCareWorld


_DEFAULT_EXECUTABLE_PATH = "@editor"


class MusculoskeletalEnv(RCareWorld):
    """Musculoskeletal environment to test musculoskeletal analysis"""

    # Environment-specific unity attribute IDs.
    _person_id: int = 1738

    def __init__(self, executable_file=str(_DEFAULT_EXECUTABLE_PATH), seed: int=None,*args, **kwargs):
        super().__init__(executable_file=executable_file, *args, **kwargs)
        print(self.attrs)


    def get_person(self) -> MusculoskeletalAttr:
        """Access the person."""
        return self.GetAttr(self._person_id)

