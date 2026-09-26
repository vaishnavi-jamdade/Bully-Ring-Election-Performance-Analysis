"""
Performance Analysis of Bully and Ring Leader Election Algorithms.

Usage:
    python performance_analysis.py ../dataset/bully_ring_election_dataset.csv

The script creates CSV summaries and performance graphs.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import ttest_ind


def load_dataset(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("%", "percent", regex=False)
    )

    # Keep the notebook's naming convention consistent.
    if "election_time_(ms)" in df.columns and "election_time_ms" not in df.columns:
        df = df.rename(columns={"election_time_(ms)": "election_time_ms"})

    numeric_columns = [
        "number_of_nodes", "failed_nodes", "active_nodes",
        "failure_rate_percent", "coordinator_failure",
        "initiator_node", "coordinator_node", "messages_sent",
        "election_rounds", "election_time_ms", "execution_run",
        "random_seed", "messages_per_active_node",
        "time_per_active_node",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def run_analysis(df: pd.DataFrame, output_dir: str | Path = "results") -> dict[str, pd.DataFrame]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Dataset Shape:", df.shape)
    print("\nAlgorithms:")
    print(df["algorithm"].value_counts())
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nDuplicate Rows:", df.duplicated().sum())

    comparison = df.groupby("algorithm").agg(
        Average_Election_Time_ms=("election_time_ms", "mean"),
        Average_Messages=("messages_sent", "mean"),
        Average_Election_Rounds=("election_rounds", "mean"),
        Average_Messages_Per_Active_Node=("messages_per_active_node", "mean"),
        Average_Time_Per_Active_Node=("time_per_active_node", "mean"),
    ).round(3)

    failure_analysis = df.groupby(
        ["failure_rate_percent", "algorithm"]
    ).agg(
        Average_Time_ms=("election_time_ms", "mean"),
        Average_Messages=("messages_sent", "mean"),
        Average_Rounds=("election_rounds", "mean"),
    ).reset_index()

    condition_analysis = df.groupby(
        ["failure_condition", "algorithm"]
    ).agg(
        Average_Time_ms=("election_time_ms", "mean"),
        Average_Messages=("messages_sent", "mean"),
        Average_Rounds=("election_rounds", "mean"),
    ).reset_index()

    node_summary = df.groupby(
        ["number_of_nodes", "algorithm"]
    ).agg(
        Mean_Time_ms=("election_time_ms", "mean"),
        Std_Time_ms=("election_time_ms", "std"),
        Mean_Messages=("messages_sent", "mean"),
        Std_Messages=("messages_sent", "std"),
        Mean_Rounds=("election_rounds", "mean"),
        Std_Rounds=("election_rounds", "std"),
    ).reset_index().round(3)

    failure_summary = df.groupby(
        ["failure_rate_percent", "algorithm"]
    ).agg(
        Mean_Time_ms=("election_time_ms", "mean"),
        Std_Time_ms=("election_time_ms", "std"),
        Mean_Messages=("messages_sent", "mean"),
        Std_Messages=("messages_sent", "std"),
        Mean_Rounds=("election_rounds", "mean"),
        Std_Rounds=("election_rounds", "std"),
    ).reset_index().round(3)

    final_analysis = df.groupby("algorithm").agg(
        Total_Executions=("algorithm", "count"),
        Avg_Election_Time_ms=("election_time_ms", "mean"),
        Min_Election_Time_ms=("election_time_ms", "min"),
        Max_Election_Time_ms=("election_time_ms", "max"),
        Avg_Messages=("messages_sent", "mean"),
        Min_Messages=("messages_sent", "min"),
        Max_Messages=("messages_sent", "max"),
        Avg_Election_Rounds=("election_rounds", "mean"),
        Avg_Messages_Per_Active_Node=("messages_per_active_node", "mean"),
        Avg_Time_Per_Active_Node=("time_per_active_node", "mean"),
    ).round(3)

    # Save tables.
    tables = {
        "overall_comparison": comparison,
        "performance_by_node_count": node_summary,
        "performance_by_failure_rate": failure_summary,
        "performance_by_failure_condition": condition_analysis,
        "final_algorithm_performance": final_analysis,
    }

    for name, table in tables.items():
        table.to_csv(output_dir / f"{name}.csv")

    # Graph 1: average election time.
    df.groupby("algorithm")["election_time_ms"].mean().plot(kind="bar", figsize=(8, 5))
    plt.title("Average Election Time: Bully vs Ring")
    plt.xlabel("Algorithm")
    plt.ylabel("Average Election Time (ms)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_dir / "average_election_time.png", dpi=300)
    plt.close()

    # Graph 2: average messages.
    df.groupby("algorithm")["messages_sent"].mean().plot(kind="bar", figsize=(8, 5))
    plt.title("Average Messages Sent: Bully vs Ring")
    plt.xlabel("Algorithm")
    plt.ylabel("Average Messages")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_dir / "average_messages.png", dpi=300)
    plt.close()

    # Graph 3: election rounds.
    df.groupby("algorithm")["election_rounds"].mean().plot(kind="bar", figsize=(8, 5))
    plt.title("Average Election Rounds: Bully vs Ring")
    plt.xlabel("Algorithm")
    plt.ylabel("Average Election Rounds")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_dir / "average_election_rounds.png", dpi=300)
    plt.close()

    # Node-size graphs.
    for value, title, ylabel, filename in [
        ("election_time_ms", "Election Time vs Number of Nodes",
         "Average Election Time (ms)", "time_vs_nodes.png"),
        ("messages_sent", "Messages Sent vs Number of Nodes",
         "Average Messages Sent", "messages_vs_nodes.png"),
        ("election_rounds", "Election Rounds vs Number of Nodes",
         "Average Election Rounds", "rounds_vs_nodes.png"),
    ]:
        data = df.groupby(["number_of_nodes", "algorithm"])[value].mean().reset_index()
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=data, x="number_of_nodes", y=value,
                     hue="algorithm", marker="o")
        plt.title(title)
        plt.xlabel("Number of Nodes")
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_dir / filename, dpi=300)
        plt.close()

    # Failure-rate graphs.
    for value, title, ylabel, filename in [
        ("Average_Time_ms", "Election Time vs Failure Rate",
         "Average Election Time (ms)", "time_vs_failure_rate.png"),
        ("Average_Messages", "Messages Sent vs Failure Rate",
         "Average Messages", "messages_vs_failure_rate.png"),
        ("Average_Rounds", "Election Rounds vs Failure Rate",
         "Average Election Rounds", "rounds_vs_failure_rate.png"),
    ]:
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=failure_analysis, x="failure_rate_percent", y=value,
                     hue="algorithm", marker="o")
        plt.title(title)
        plt.xlabel("Failure Rate (%)")
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_dir / filename, dpi=300)
        plt.close()

    # Heatmaps.
    for value, title, filename in [
        ("election_time_ms", "Average Election Time Heatmap", "heatmap_time.png"),
        ("messages_sent", "Average Messages Heatmap", "heatmap_messages.png"),
    ]:
        pivot = df.pivot_table(
            values=value,
            index="number_of_nodes",
            columns="algorithm",
            aggfunc="mean",
        )
        plt.figure(figsize=(8, 6))
        sns.heatmap(pivot, annot=True, fmt=".2f")
        plt.title(title)
        plt.tight_layout()
        plt.savefig(output_dir / filename, dpi=300)
        plt.close()

    # Boxplots.
    for value, title, ylabel, filename in [
        ("election_time_ms", "Distribution of Election Time",
         "Election Time (ms)", "boxplot_time.png"),
        ("messages_sent", "Distribution of Messages Sent",
         "Messages Sent", "boxplot_messages.png"),
    ]:
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=df, x="algorithm", y=value)
        plt.title(title)
        plt.xlabel("Algorithm")
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(output_dir / filename, dpi=300)
        plt.close()

    # Correlation.
    correlation_columns = [
        "number_of_nodes", "failed_nodes", "active_nodes",
        "failure_rate_percent", "messages_sent", "election_rounds",
        "election_time_ms", "messages_per_active_node",
        "time_per_active_node",
    ]
    correlation_columns = [c for c in correlation_columns if c in df.columns]
    correlation_matrix = df[correlation_columns].corr()

    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f")
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(output_dir / "correlation_matrix.png", dpi=300)
    plt.close()

    # Statistical comparison.
    bully_time = df[df["algorithm"].astype(str).str.lower() == "bully"]["election_time_ms"].dropna()
    ring_time = df[df["algorithm"].astype(str).str.lower() == "ring"]["election_time_ms"].dropna()

    if len(bully_time) > 1 and len(ring_time) > 1:
        t_stat, p_value = ttest_ind(bully_time, ring_time, equal_var=False)
        print("\nIndependent t-test")
        print("T-statistic:", round(t_stat, 4))
        print("P-value:", round(p_value, 6))

    print("\nFinal Performance Table:")
    print(final_analysis)

    return tables


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python performance_analysis.py <dataset.csv> [output_dir]")
        raise SystemExit(1)

    dataset = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "results"

    df = load_dataset(dataset)
    run_analysis(df, output_dir)


if __name__ == "__main__":
    main()
