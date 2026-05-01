from dataclasses import dataclass
from enum import Enum, auto


@dataclass(frozen=True)
class PostId:
    id: str


@dataclass(frozen=True)
class PacketId:
    id: str


@dataclass(frozen=True)
class PorterId:
    id: str


@dataclass(frozen=True)
class Timestamp:
    timestamp: float


class PacketStatus(Enum):
    WAITING = auto()
    RESERVED = auto()
    IN_PORTING = auto()
    DELIVERED = auto()


@dataclass(frozen=True)
class Coord:
    x: float
    y: float