# 🚀 Enterprise NetDevOps: Automation and Centralized Telemetry

This project is an Infrastructure as Code (IaC) lab environment designed to automate high-availability deployments on Cisco topologies and centralize network monitoring using a microservices architecture.

![Network Topology](images/topologia.png)

## 🛠️ Tech Stack

* **Orchestration & Configuration:** Ansible (Layer 2 & 3 automation).
* **Network Infrastructure:** Cisco IOS (Simulated on GNS3), OSPF Routing, HSRP with Object Tracking.
* **Telemetry Processing:** Python 3.12 (UDP Sockets, `pymssql`, RegEx).
* **Containers & Microservices:** Docker (Ubuntu/Debian-based images).
* **Persistent Storage:** Microsoft SQL Server 2022 (Docker Volumes, T-SQL).

## ⚙️ System Architecture

The project is divided into two critical operational phases:

1. **Network Automation (Ansible):** Playbooks dynamically configure distribution switches (DIST-01, DIST-02) by assigning IP addressing, SVIs, OSPF areas, and HSRP redundancy. Object tracking is injected to ensure automatic gateway failover in the event of a perimeter firewall outage.
2. **Telemetry Pipeline (Docker + Python + SQL Server):** 
   * Cisco switches are configured to forward logs (Syslog) to an isolated management network (`tap1`).
   * A Docker container running a Python daemon intercepts UDP packets on port 514.
   * The script parses the text strings and injects them in real-time into a second container hosting a **SQL Server 2022** database.
   * Relational data persists on a local volume, guaranteeing log history retention across server reboots.

## 📂 Project Structure

* `/playbooks/`: Ansible execution flows for campus deployment and configuration backups.
* `/roles/`: Modular Ansible roles (`layer2_switching`, `layer3_routing`, `firewall_edge`).
* `/inventory/`: Dynamic variables split by `host_vars` and `group_vars`.
* `/syslog_daemon/`: Python source code and `Dockerfile` to build the Syslog collector image, adapted with `freetds-dev` dependencies.
* `/backups/`: Automated network equipment configuration backups.

## 🚀 Deployment

To provision the routing layer and spin up the telemetry services:

```bash
# 1. Execute Ansible orchestrator
ansible-playbook playbooks/deploy_campus.yaml --tags "hsrp,redundancy"

# 2. Deploy SQL Server engine with persistent storage
docker volume create mssql_data
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=YourPassword!" -p 1433:1433 -v mssql_data:/var/opt/mssql --name sql_syslog -d [mcr.microsoft.com/mssql/server:2022-latest](https://mcr.microsoft.com/mssql/server:2022-latest)

# 3. Build and launch Python Syslog daemon
cd syslog_daemon
docker build -t netdevops-syslog-ubuntu .
docker run -d --name syslog_receptor -p 10.10.20.100:514:514/udp netdevops-syslog-ubuntu