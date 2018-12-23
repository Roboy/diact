# Interface of state activation towards signal instance
# Signal instance interface towards state activation

from typing import Set


class ISignalInstance:

    def name(self) -> str:
        """
        Returns the name if this signal instance's signal.
        """
        pass


class IActivation:

    name: str

    def write_props(self) -> Set[str]:
        pass

    def specificity(self) -> float:
        pass

    def wiped(self, sig: ISignalInstance) -> None:
        pass

    def wipe(self) -> None:
        pass

    def signal_instances(self) -> Set[ISignalInstance]:
        pass
