from abc import ABC, abstractmethod
from typing import List
from runtime.models.runtime_event import RuntimeEvent

class RuntimeAdapter(ABC):
    """
    Abstract base class for Runtime Adapters.
    Adapters are responsible for converting provider-specific data
    (e.g., OTel spans, Java Agent logs) into normalized RuntimeEvents.
    """

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def translate(self, raw_data: any) -> List[RuntimeEvent]:
        pass

class RuntimeCollector(ABC):
    """
    Abstract base class for Runtime Collectors.
    Collectors are responsible for ingesting data from a source
    and using adapters to normalize it.
    """

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def collect(self) -> List[RuntimeEvent]:
        pass
