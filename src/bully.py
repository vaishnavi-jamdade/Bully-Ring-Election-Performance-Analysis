"""
Bully Leader Election Algorithm
Generates experiment records compatible with performance_analysis.py.
"""

from __future__ import annotations
import random
import time
from typing import Iterable, Optional


def bully_election(
    number_of_nodes: int,
    failed_nodes: Optional[Iterable[int]] = None,
    initiator_node: Optional[int] = None,
    random_seed: Optional[int] = None,
) -> dict:
    """
    Run one Bully election.

    Nodes are numbered 1..number_of_nodes. The highest active node becomes
    coordinator. A node sends an election message to every higher active node.
    Each higher active node responds and starts its own election.

    Returns one experiment record.
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

    messages = 0
    rounds = 0
    current = initiator_node

    start = time.perf_counter()

    # A practical Bully-election simulation:
    # the initiator contacts all higher active nodes; the highest active
    # participant ultimately wins.
    while current != coordinator_node:
        higher = [n for n in active if n > current]
        rounds += 1

        for node in higher:
            messages += 1          # election message
            messages += 1          # OK/response message

        current = min(higher) if higher else coordinator_node

    messages += 1                  # coordinator announcement

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    active_count = len(active)
    failure_rate = len(failed) / number_of_nodes * 100

    return {
        "algorithm": "Bully",
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
    print(bully_election(10, failed_nodes=[3, 7], random_seed=42))
