from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from porter.vo import Coord, PacketId, PacketStatus, PorterId, PostId, Timestamp

if TYPE_CHECKING:
    from porter.graph import PostGraph

@dataclass(frozen=True)
class Post:
    id: PostId
    coord: Coord


@dataclass(frozen=True)
class PortEvent:
    packet_id: PacketId
    porter_id: PorterId | None
    post_id: PostId
    timestamp: Timestamp
    status: PacketStatus

    @staticmethod
    def create_init_event(packet_id: PacketId, post_id: PostId) -> PortEvent:
        return PortEvent(packet_id, None, post_id, Timestamp(0), PacketStatus.WAITING)


class Packet:
    def __init__(
        self,
        id_: PacketId,
        dep_id: PostId,
        arv_id: PostId,
        events: list[PortEvent] | None = None,
    ) -> None:
        self.id = id_
        self.dep_id = dep_id
        self.arv_id = arv_id
        self.events: list[PortEvent] = events or [PortEvent.create_init_event(id_, dep_id)]
        if not self.events:
            raise ValueError("events must not be empty")

        self.current_status = self.events[-1].status

    def add_event(self, event: PortEvent) -> None:
        self.events.append(event)
        self.current_status = event.status


class PacketListClient:
    def __init__(self, packets: set[Packet] | None = None) -> None:
        self.packets: dict[PacketId, Packet] = {packet.id: packet for packet in (packets or set())}

    def load(
        self,
        packet_id: PacketId,
        porter_id: PorterId,
        post_id: PostId,
        timestamp: Timestamp
    ) -> None:
        if packet_id not in self.packets:
            raise ValueError(f"packet_id {packet_id} not found")

        pac = self.packets[packet_id]
        st = PacketStatus.DELIVERED if post_id == pac.arv_id else PacketStatus.WAITING
        pac.add_event(
            PortEvent(packet_id, porter_id, post_id, timestamp, st)
        )

    def unload(
        self,
        packet_id: PacketId,
        porter_id: PorterId,
        post_id: PostId,
        timestamp: Timestamp
    ) -> None:
        if packet_id not in self.packets:
            raise ValueError(f"packet_id {packet_id} not found")

        pac = self.packets[packet_id]
        pac.add_event(
            PortEvent(packet_id, porter_id, post_id, timestamp, PacketStatus.IN_PORTING)
        )

    def search_packet(
        self,
        status: set[PacketStatus] | None = None,
        cur_post_id: PostId | None = None,
        arv_id: PostId | None = None,
    ) -> list[PacketId]:
        result = []
        for pac_id, pac in self.packets.items():
            if status is not None and pac.current_status not in status:
                continue
            if cur_post_id is not None and pac.events[-1].post_id != cur_post_id:
                continue
            if arv_id is not None and pac.arv_id != arv_id:
                continue
            result.append(pac_id)
        return result


class PortStrategy(ABC):
    @abstractmethod
    def reserve(self, plc: PacketListClient, graph: PostGraph) -> PacketId | None:
        pass


class Porter:
    def __init__(self) -> None:
        pass
