# AI-Powered Endpoint Monitoring & Anomaly Detection Platform

A defensive cybersecurity project combining **real-time endpoint monitoring**, **behavioral feature engineering**, **Machine Learning**, and a **Flask dashboard** to identify unusual process activity on a Linux system.

> This project is educational and defensive. It does not use real malware and does not claim to provide production-grade malware detection. Suspicious behaviors used during model training are generated from controlled synthetic scenarios.

---

## Overview

The platform continuously monitors local system processes and collects behavioral telemetry such as:

- CPU usage
- Memory usage
- Number of threads
- Network connections
- Process age
- CPU variation rate
- Memory variation rate
- Thread variation
- Network connection variation

The collected information is transformed into behavioral features and analyzed by a Machine Learning model.

Each process is classified as:

```text
Normal
or
Suspicious
