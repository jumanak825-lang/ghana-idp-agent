# 🏥 Ghana IDP Healthcare Agent

> Bridging Medical Deserts — An Intelligent Document Parsing Agent for the Virtue Foundation Ghana Dataset

Built for the **Databricks + Accenture Hackathon 2026**

🔗 **Live Demo:** [huggingface.co/spaces/JumanaCodes/ghana-idp-agent](https://huggingface.co/spaces/JumanaCodes/ghana-idp-agent)  
📡 **API Endpoint:** `https://dbc-625f49f0-72cc.cloud.databricks.com/serving-endpoints/ghana-idp-agent/invocations`

---

## 🎯 Problem

By 2030, the world will face a shortage of over 10 million healthcare workers — not because expertise doesn't exist, but because it is not intelligently coordinated. In Ghana, skilled doctors remain disconnected from hospitals that urgently need them, and critical medical deserts go undetected.

---

## 🤖 What We Built

An Intelligent Document Parsing (IDP) agent that:

- **Extracts** medical facility capabilities from unstructured free-form text
- **Detects** anomalies and suspicious capability claims automatically
- **Maps** medical deserts across Ghana's 170 regions
- **Reasons** over workforce distribution and NGO coverage gaps
- **Plans** resource allocation for non-technical NGO planners

---

## 🏗️ Architecture

### 4-Stage LLM Extraction Pipeline

```
Stage 1: Organization Classification (NGO vs Facility)
Stage 2: Structured Field Extraction (address, contacts, type)
Stage 3: Free-form Facts (procedure, equipment, capability)
Stage 4: Medical Specialty Classification
```

### 6-Agent LangGraph System

| Agent | Role |
|-------|------|
| 🗃️ Genie Text2SQL | SQL counts & statistics |
| 🔍 Keyword Search | Facility lookup |
| 🗺️ Geospatial | Distance calculations & cold spots |
| ⚠️ Anomaly Detection | Data quality checks (Q3.1, Q4.4, Q4.8, Q4.9) |
| 🧠 Medical Reasoning | Workforce & NGO gap analysis |
| 📋 Planning | Resource allocation recommendations |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Orchestration | LangGraph Multi-Agent |
| LLM | Meta Llama 3.3 70B (Databricks) |
| ML Lifecycle | MLflow + Unity Catalog |
| Deployment | Databricks Mosaic AI |
| Data | Delta Lake |
| UI | Gradio on HuggingFace Spaces |

---

## 📊 Key Results

- **753** Ghana healthcare facilities analyzed
- **170** regions scored for medical desert severity
- **140** critical medical deserts identified (score < 20/100)
- **26** cardiology facilities — ALL in southern Ghana
- **ZERO** cardiology within 100km of Tamale
- **50** procedures depend on only 1 facility each
- **15/15** must-have queries answered with citations

---

## 🖥️ UI Features

| Tab | Description |
|-----|-------------|
| 💬 Ask the Agent | Natural language chat with citations |
| 📋 Planning System | NGO resource allocation planner |
| ⚠️ Anomaly Browser | Filterable flagged facilities |
| 🏜️ Desert Score Table | All 170 regions with scores |
| 🏥 NGO & Facility Stats | Distribution breakdown |
| 🌡️ Specialty Heatmap | Specialty concentration by region |
| 🗺️ Medical Desert Map | Visual map of Ghana |
| ℹ️ About | Project description |

---

## 🔍 Anomaly Detection

| Code | Meaning |
|------|---------|
| Q4.4 | Clinic claims unrealistically high procedure count |
| Q4.8 | High procedure breadth but zero equipment documented |
| Q4.9 | Capability claims without supporting equipment |
| Q3.1 | Advanced specialty without supporting equipment |

---

## 📈 Evaluation Coverage

| Criteria | Coverage |
|----------|----------|
| Technical Accuracy (35%) | 15/15 must-have queries ✅ |
| IDP Innovation (30%) | 4-stage LLM extraction ✅ |
| Social Impact (25%) | Medical desert mapping ✅ |
| User Experience (10%) | Natural language UI ✅ |
| Citations (Stretch) | Agent + pipeline step + confidence ✅ |
| Map (Stretch) | Ghana medical desert map ✅ |

---

## 🚀 Try It

Visit the live demo:  
👉 [https://huggingface.co/spaces/JumanaCodes/ghana-idp-agent](https://huggingface.co/spaces/JumanaCodes/ghana-idp-agent)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
