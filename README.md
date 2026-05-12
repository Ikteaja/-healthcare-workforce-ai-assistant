# Healthcare Workforce AI Assistant

## Project Goal

Healthcare Workforce AI Assistant is an enterprise-grade local AI platform designed to help healthcare organizations manage workforce knowledge, HR documentation, policies, staffing procedures, and operational intelligence using Retrieval-Augmented Generation (RAG).

The platform is fully containerized and runs locally using Rancher Desktop, Ollama, Docker, and ChromaDB.

---

# Project Objectives

- Build a production-style enterprise AI platform
- Implement local LLM hosting
- Implement enterprise RAG architecture
- Apply DevOps and MLOps best practices
- Build modular CI/CD pipelines
- Integrate containerization and GHCR
- Prepare for Kubernetes and GitOps deployment

---

# High-Level Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend API
 │
 ▼
LangChain RAG Pipeline
 │
 ├── ChromaDB Vector Store
 │
 └── Ollama Local LLM
```

---

# Local Platform Architecture

```text
Rancher Desktop
 │
 ├── healthcare-frontend
 ├── healthcare-backend
 ├── healthcare-ollama
 └── healthcare-chromadb
```

---

# Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| RAG Framework | LangChain |
| Local LLM | Ollama |
| Vector Database | ChromaDB |
| Container Runtime | Docker |
| Local Kubernetes | Rancher Desktop |
| CI/CD | GitHub Actions |
| Container Registry | GHCR |
| Testing | Pytest |
| MLOps | MLflow |
| Future GitOps | ArgoCD |
| Future Orchestration | Kubernetes |

---

# CI/CD Pipeline Architecture

## Backend Pipeline

### Jobs

- Security Scan
- Dependency Validation
- Unit Testing
- Integration Testing
- Build Validation
- Artifact Packaging

---

## Frontend Pipeline

### Jobs

- Dependency Scan
- Frontend Validation
- Unit Testing
- Packaging

---

## Enterprise RAG Pipeline

### Jobs

- Supply Chain Security Scan
- Embedding Pipeline Validation
- Retriever Validation
- Vector Database Validation
- RAG Unit Tests
- RAG Integration Tests
- Artifact Packaging

---

## Container Pipeline

### Jobs

- Build Backend Container
- Build Frontend Container
- Push Images to GHCR
- Container Validation

---

# Branching Strategy

```text
main
 │
 ├── feature/cicd-foundation
 ├── feature/docker-local-platform
 └── future feature branches
```

---

# Implemented Phases

| Phase | Status |
|---|---|
| Repository Initialization | Implemented |
| FastAPI Backend Starter | Implemented |
| Streamlit Frontend Starter | Implemented |
| Enterprise Folder Structure | Implemented |
| Backend CI/CD Pipeline | Implemented |
| Frontend CI/CD Pipeline | Implemented |
| Enterprise RAG Pipeline | Implemented |
| Security Scanning | Implemented |
| Unit Testing | Implemented |
| Integration Testing | Implemented |
| Artifact Packaging | Implemented |
| Docker Containerization | Implemented |
| Docker Compose Platform | Implemented |
| Ollama Integration | Implemented |
| ChromaDB Integration | Implemented |
| GHCR Container Registry | Implemented |
| Environment Configuration | Implemented |

---

# Planned Future Phases

| Future Phase | Status |
|---|---|
| PDF Document Upload | Planned |
| Enterprise RAG Ingestion | Planned |
| Embedding Generation | Planned |
| Semantic Search | Planned |
| Chat API | Planned |
| Streaming Responses | Planned |
| MLflow Tracking | Planned |
| Observability and Monitoring | Planned |
| Prometheus Integration | Planned |
| Grafana Dashboards | Planned |
| Kubernetes Deployment | Planned |
| Helm Charts | Planned |
| GitOps Deployment | Planned |
| ArgoCD Integration | Planned |
| RBAC Security | Planned |
| Enterprise Secrets Management | Planned |

---

# Local Development

## Start Platform

```bash
docker compose up -d
```

---

# Local Services

| Service | URL |
|---|---|
| Frontend | http://localhost:8501 |
| Backend API | http://localhost:8000 |
| Ollama | http://localhost:11434 |
| ChromaDB | http://localhost:8001 |

---

# Container Registry

```text
ghcr.io/ikteaja/healthcare-backend
ghcr.io/ikteaja/healthcare-frontend
```

---

# Enterprise Design Principles

- Modular architecture
- Independent CI/CD pipelines
- Local-first AI infrastructure
- Enterprise-grade testing strategy
- Container-native deployment
- GitOps-ready architecture
- Secure software supply chain validation
- Scalable RAG design
