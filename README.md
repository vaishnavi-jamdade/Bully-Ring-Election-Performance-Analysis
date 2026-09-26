# Bully-Ring-Election-Performance-Analysis
Performance analysis of Bully and Ring leader election algorithms under different node failure conditions using simulation and comparative performance metrics. 

# Performance Analysis of Bully and Ring Leader Election Algorithms

## 📌 Project Overview

This project focuses on the performance analysis of two distributed leader election algorithms:

* **Bully Algorithm**
* **Ring Algorithm**

The study evaluates their performance under different node failure conditions and different network sizes.

The objective is to compare the behavior of both algorithms using measurable performance parameters such as election time, messages exchanged, election rounds, node failures, and success/failure of the election process.

---

## 🎯 Objectives

1. Implement the Bully leader election algorithm.
2. Implement the Ring leader election algorithm.
3. Simulate different node failure conditions.
4. Analyze the performance of both algorithms.
5. Compare the algorithms for different numbers of nodes.
6. Study the effect of increasing node failures.
7. Analyze election time and message complexity.
8. Identify performance trends using graphs and statistical analysis.

---

## 🔬 Research Question

How does the performance of the Bully and Ring leader election algorithms vary under different node failure conditions and different network sizes?

---

## 📊 Parameters

The dataset contains the following parameters:

* Algorithm
* Number of Nodes
* Failed Nodes
* Active Nodes
* Failure Rate (%)
* Failure Condition
* Coordinator Failure
* Initiator Node
* Coordinator Node
* Messages Sent
* Election Rounds
* Election Time (ms)
* Success/Failure
* Execution Run
* Random Seed
* Messages per Active Node
* Time per Active Node

---

## 🧪 Experimental Setup

The algorithms are evaluated using different network sizes and node failure conditions.

### Network Sizes

* 5 nodes
* 10 nodes
* 20 nodes
* 50 nodes
* 100 nodes

Multiple execution runs and random seeds are used to obtain performance measurements.

---

## 📈 Performance Metrics

The following metrics are used for comparison:

### 1. Election Time

Measures the time required to complete the leader election process.

### 2. Messages Sent

Measures the total number of messages exchanged during the election.

### 3. Election Rounds

Measures the number of communication rounds required for leader election.

### 4. Failure Rate

Measures the proportion of failed nodes in the network.

### 5. Success/Failure

Determines whether the leader election was successfully completed.

### 6. Messages per Active Node

Measures communication overhead relative to the number of active nodes.

### 7. Time per Active Node

Measures election time relative to the number of active nodes.

---

## 🗂️ Project Structure

```text
bully-ring-election-performance-analysis/
│
├── README.md
├── requirements.txt
│
├── dataset/
│   └── bully_ring_election_dataset.csv
│
├── src/
│   ├── bully_algorithm.py
│   ├── ring_algorithm.py
│   └── performance_analysis.py
│
├── notebooks/
│   └── performance_analysis.ipynb
│
├── results/
│   ├── performance_summary.csv
│   └── figures/
│
└── paper/
    └── research_paper.pdf
```

---

## 🛠️ Technologies Used

* Python
* Google Colab
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Jupyter Notebook

---

## 📚 Algorithms

### Bully Algorithm

The Bully algorithm elects the active process with the highest priority/identifier as the coordinator. When a coordinator fails, another active process initiates an election.

### Ring Algorithm

The Ring algorithm organizes processes logically in a ring. An election message is passed through the ring, and the eligible process with the highest identifier is selected as coordinator.

---

## 📊 Analysis

The experimental results are analyzed using tables and visualizations to study:

* Election time
* Message overhead
* Number of election rounds
* Effect of node failures
* Effect of network size
* Algorithm behavior under different failure conditions

---

## 🚧 Project Status

* [x] Dataset preparation
* [x] Algorithm implementation
* [x] Performance analysis
* [x] Visualization
* [ ] Final research paper
* [ ] Final experimental validation

---

## 👩‍💻 Author

**Vaishnavi Jamdade**

M.Tech — Information Technology

---

## 📄 Research Paper

The research paper for this project is included in the `paper/` directory.

---

## ⚠️ Note

The experimental results are based on simulation and the generated dataset. Results may vary depending on the random seed, network configuration, node failure conditions, and execution environment.

