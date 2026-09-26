"""
Ring Leader Election Algorithm
Generates experiment records compatible with performance_analysis.py.
"""

from __future__ import annotations
import random
import time
from typing import Iterable, Optional


def ring_election(
    number_of_nodes: int,
    failed_nodes: Optional[Iterable[int]] = None,
    initiator_node: Optional[int] = None,
    random_seed: Optional[int] = None,
) -> dict:
    """
    Run one Ring election.

    Active nodes form a logical ring in ascending node order. The election
    token travels through the active ring and the highest active node becomes
    coordinator.
    """
    if number_of_nodes < 2:
        raise ValueError("number_of_nodes must be at least 2")

    rng = random.Random(random_seed)
    all_nodes = list(range(1, number_of_nodes + 1))

    if failed_nodes is None:
        failed_nodes = []

    failed = sorted(set(int(n) for n in failed_nodes))
    invalid = [n for n in failed if n not in all_nodes]
    if invalid:
        raise ValueError(f"Invalid failed node(s): {invalid}")

    active = [n for n in all_nodes if n not in failed]
    if not active:
        raise ValueError("At least one node must remain active")

    if initiator_node is None:
        initiator_node = rng.choice(active)
    if initiator_node not in active:
        raise ValueError("initiator_node must be an active node")

    coordinator_node = max(active)
    coordinator_failed = int(coordinator_node in failed)

    start = time.perf_counter()

    # The token passes once around the active logical ring.
    ring = active[active.index(initiator_node):] + active[:active.index(initiator_node)]
    messages = len(ring)
    rounds = 1

    # Coordinator announcement makes a second traversal.
    messages += len(ring)

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    active_count = len(active)
    failure_rate = len(failed) / number_of_nodes * 100

    return {
        "algorithm": "Ring",
        "number_of_nodes": number_of_nodes,
        "failed_nodes": len(failed),
        "active_nodes": active_count,
        "failure_rate_percent": failure_rate,
        "failure_condition": "No Failure" if not failed else "Node Failure",
        "coordinator_failure": coordinator_failed,
        "initiator_node": initiator_node,
        "coordinator_node": coordinator_node,
        "messages_sent": messages,
        "election_rounds": rounds,
        "election_time_ms": elapsed_ms,
        "execution_run": 1,
        "random_seed": random_seed,
        "messages_per_active_node": messages / active_count,
        "time_per_active_node": elapsed_ms / active_count,
        "success/failure": "Success",
    }


if __name__ == "__main__":
    print(ring_election(10, failed_nodes=[3, 7], random_seed=42))
