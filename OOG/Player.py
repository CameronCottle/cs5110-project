from abc import ABC, abstractmethod
from typing import Any

class Player(ABC):
	def __init__(self, name: str = "") -> None:
		self.name = name

	@abstractmethod
	def defect(self) -> Any:
		pass

	@abstractmethod
	def cooperate(self) -> Any:
		pass