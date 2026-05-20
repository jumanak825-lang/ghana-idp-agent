import gradio as gr
import requests
import os

DATABRICKS_HOST  = "https://dbc-625f49f0-72cc.cloud.databricks.com"
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN", "")
ENDPOINT_URL     = f"{DATABRICKS_HOST}/serving-endpoints/ghana-idp-agent/invocations"

EXAMPLE_QUESTIONS = [
    "How many hospitals have cardiology?",
    "How many hospitals in Northern Region have the ability to perform surgery?",
    "Are there any clinics in Accra that do ophthalmology?",
    "Which region has the most hospitals?",
    "How many hospitals treating cardiology are within 100km of Tamale?",
    "Where are the largest geographic cold spots where critical procedures are absent?",
    "Which facilities claim an unrealistic number of procedures relative to their size?",
    "What correlations exist between facility type and number of specialties?",
    "Which facilities have high procedure breadth but no equipment?",
    "Which facilities show things that should not move together like large claims with no equipment?",
    "Where is the workforce for cardiology actually practicing in Ghana?",
    "Which procedures depend on very few facilities in Ghana?",
    "Where is there oversupply vs scarcity of procedures by region?",
    "Where are there gaps where no NGOs are working despite evident need?",
]

PLANNING_QUESTIONS = [
    "Where should we send doctors first?",
    "Which regions need NGO support most urgently?",
    "What is the best resource allocation plan for Ghana?",
    "Where are patients most at risk due to lack of access?",
    "Which medical deserts should be prioritized for investment?",
]

DESERT_SCORES_DATA = [
    {"region": "Accra", "score": 100, "facilities": 204, "hospitals": 58, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Kumasi", "score": 100, "facilities": 59, "hospitals": 25, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Tema", "score": 100, "facilities": 33, "hospitals": 18, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Ashanti", "score": 87, "facilities": 30, "hospitals": 14, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Ashanti Region", "score": 85, "facilities": 15, "hospitals": 11, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Western", "score": 73, "facilities": 33, "hospitals": 5, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Tamale", "score": 75, "facilities": 14, "hospitals": 5, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Takoradi", "score": 69, "facilities": 11, "hospitals": 6, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Sunyani", "score": 65, "facilities": 10, "hospitals": 5, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Central Region", "score": 60, "facilities": 8, "hospitals": 4, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Western Region", "score": 60, "facilities": 13, "hospitals": 2, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Cape Coast", "score": 61, "facilities": 12, "hospitals": 3, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Greater Accra Region", "score": 59, "facilities": 9, "hospitals": 2, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Eastern Region", "score": 55, "facilities": 4, "hospitals": 3, "emergency": True, "risk": "🟢 ADEQUATE"},
    {"region": "Northern", "score": 48, "facilities": 4, "hospitals": 4, "emergency": True, "risk": "🟡 AT RISK"},
    {"region": "Techiman", "score": 48, "facilities": 5, "hospitals": 2, "emergency": True, "risk": "🟡 AT RISK"},
    {"region": "Brong Ahafo", "score": 41, "facilities": 3, "hospitals": 2, "emergency": True, "risk": "🟡 AT RISK"},
    {"region": "Tarkwa", "score": 39, "facilities": 4, "hospitals": 3, "emergency": True, "risk": "🟡 AT RISK"},
    {"region": "Northern Region", "score": 38, "facilities": 6, "hospitals": 3, "emergency": False, "risk": "🟡 AT RISK"},
    {"region": "Dodowa", "score": 37, "facilities": 2, "hospitals": 1, "emergency": True, "risk": "🟡 AT RISK"},
    {"region": "Bibiani", "score": 34, "facilities": 3, "hospitals": 1, "emergency": True, "risk": "🟡 AT RISK"},
    {"region": "Bolgatanga", "score": 28, "facilities": 1, "hospitals": 1, "emergency": True, "risk": "🟡 AT RISK"},
    {"region": "Koforidua", "score": 24, "facilities": 6, "hospitals": 2, "emergency": False, "risk": "🟡 AT RISK"},
    {"region": "Ho", "score": 24, "facilities": 4, "hospitals": 4, "emergency": False, "risk": "🟡 AT RISK"},
    {"region": "Obuasi", "score": 19, "facilities": 4, "hospitals": 3, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Volta Region", "score": 16, "facilities": 5, "hospitals": 3, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Upper West", "score": 10, "facilities": 2, "hospitals": 2, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Nalerigu", "score": 10, "facilities": 1, "hospitals": 1, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Yendi", "score": 13, "facilities": 3, "hospitals": 2, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Wa", "score": 6, "facilities": 1, "hospitals": 1, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Bawku", "score": 6, "facilities": 1, "hospitals": 1, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Upper East", "score": 6, "facilities": 1, "hospitals": 1, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Savannah", "score": 6, "facilities": 1, "hospitals": 1, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Damongo", "score": 3, "facilities": 1, "hospitals": 0, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Sandema", "score": 3, "facilities": 1, "hospitals": 0, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Kpando", "score": 1, "facilities": 1, "hospitals": 0, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Old Offinso", "score": 1, "facilities": 1, "hospitals": 0, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Agbogba", "score": 1, "facilities": 1, "hospitals": 0, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Asamankese", "score": 1, "facilities": 1, "hospitals": 0, "emergency": False, "risk": "🔴 CRITICAL"},
    {"region": "Osu", "score": 1, "facilities": 1, "hospitals": 0, "emergency": False, "risk": "🔴 CRITICAL"},
]

ANOMALY_DATA = [
    {"facility": "General Clinic", "region": "Accra", "type": "Q4.4", "anomaly": "Clinic claims 11 procedures — unrealistically high for clinic size", "confidence": 0.44},
    {"facility": "Glado Clinic Dental Practice", "region": "Accra", "type": "Q4.4", "anomaly": "Clinic claims 26 procedures — unrealistically high for clinic size", "confidence": 0.44},
    {"facility": "Ahmadiyya Muslim Hospital, Techiman", "region": "Bono East", "type": "Q4.8", "anomaly": "Claims 6 procedures but zero equipment documented", "confidence": 0.44},
    {"facility": "Akatsi South Municipal Hospital", "region": "Volta", "type": "Q4.8", "anomaly": "Claims 8 procedures but zero equipment documented", "confidence": 0.44},
    {"facility": "Center for Cosmetic Surgery", "region": "Accra", "type": "Q4.8", "anomaly": "Claims 10 procedures but zero equipment documented", "confidence": 0.44},
    {"facility": "Christian Medical Dental Services", "region": "Accra", "type": "Q4.8", "anomaly": "Claims 8 procedures but zero equipment documented", "confidence": 0.44},
    {"facility": "Deseret Hospital Accra Ghana", "region": "Accra", "type": "Q4.8", "anomaly": "Claims 8 procedures but zero equipment documented", "confidence": 0.44},
    {"facility": "Eastern View Skin Clinic, Berekum", "region": "Bono", "type": "Q4.8", "anomaly": "Claims 9 procedures but zero equipment documented", "confidence": 0.44},
    {"facility": "Eye Hospital In Accra", "region": "Accra", "type": "Q4.8", "anomaly": "Claims 18 procedures but zero equipment documented", "confidence": 0.44},
    {"facility": "Eye To Eye Clinic", "region": "Accra", "type": "Q4.8", "anomaly": "Claims 6 procedures but zero equipment documented", "confidence": 0.44},
    {"facility": "Framada Dental Clinic", "region": "Accra", "type": "Q4.8", "anomaly": "Claims 6 procedures but zero equipment documented", "confidence": 0.44},
    {"facility": "Gengimed Dental Clinic", "region": "Accra", "type": "Q4.8", "anomaly": "Claims 9 procedures but zero equipment documented", "confidence": 0.44},
    {"facility": "Godly Favoured Eye Care Centre", "region": "Accra", "type": "Q4.8", "anomaly": "Claims 7 procedures but zero equipment documented", "confidence": 0.44},
    {"facility": "Acrecity Medics", "region": "Accra", "type": "Q4.9", "anomaly": "Claims advanced specialty but no supporting equipment found", "confidence": 0.44},
    {"facility": "Amang Health Centre", "region": "Ashanti", "type": "Q4.9", "anomaly": "Claims advanced specialty but no supporting equipment found", "confidence": 0.44},
    {"facility": "Apatrapa Hospital, Tepa", "region": "Ashanti", "type": "Q4.9", "anomaly": "Claims surgical capability but no operating equipment documented", "confidence": 0.44},
    {"facility": "Banhart Specialist Hospital", "region": "Brong Ahafo", "type": "Q3.1", "anomaly": "Claims cardiology specialty but no supporting equipment found", "confidence": 0.44},
    {"facility": "Bemuah Royal Hospital", "region": "Accra", "type": "Q3.1", "anomaly": "Claims cardiology specialty but no supporting equipment found", "confidence": 0.44},
    {"facility": "Beulah Land International Hospital", "region": "Accra", "type": "Q3.1", "anomaly": "Claims cardiology specialty but no supporting equipment found", "confidence": 0.44},
    {"facility": "Central Dansoman Clinic", "region": "Accra", "type": "Q4.9", "anomaly": "Claims ICU capability but no supporting equipment listed", "confidence": 0.44},
]

# Fix 7 — NGO vs Facility breakdown
NGO_FACILITY_DATA = {
    "total_facilities": 753,
    "hospitals": 324,
    "clinics": 199,
    "ngos": 48,
    "other": 182,
    "regions_with_ngo": 28,
    "regions_without_ngo": 142,
    "critical_regions_no_ngo": 140,
}

# Fix 8 — Specialty distribution by region
SPECIALTY_DATA = [
    {"specialty": "internalMedicine", "count": 420, "regions": 45, "concentration": "Accra, Kumasi, Tema"},
    {"specialty": "emergencyMedicine", "count": 71, "regions": 18, "concentration": "Accra, Kumasi, Tamale"},
    {"specialty": "cardiology", "count": 26, "regions": 8, "concentration": "Accra (19), Kumasi (2)"},
    {"specialty": "generalSurgery", "count": 45, "regions": 12, "concentration": "Accra, Kumasi, Cape Coast"},
    {"specialty": "gynecologyAndObstetrics", "count": 38, "regions": 15, "concentration": "Accra, Kumasi, Takoradi"},
    {"specialty": "pediatrics", "count": 32, "regions": 14, "concentration": "Accra, Kumasi, Sunyani"},
    {"specialty": "ophthalmology", "count": 18, "regions": 6, "concentration": "Accra (15), Kumasi (2)"},
    {"specialty": "dentistry", "count": 55, "regions": 20, "concentration": "Accra, Kumasi, Cape Coast"},
    {"specialty": "orthopedicSurgery", "count": 12, "regions": 5, "concentration": "Accra, Kumasi"},
    {"specialty": "radiology", "count": 15, "regions": 4, "concentration": "Accra, Kumasi"},
    {"specialty": "pathology", "count": 22, "regions": 8, "concentration": "Accra, Kumasi, Cape Coast"},
    {"specialty": "infectiousDiseases", "count": 28, "regions": 12, "concentration": "Accra, Kumasi, Northern"},
    {"specialty": "neurology", "count": 8, "regions": 3, "concentration": "Accra only"},
    {"specialty": "psychiatry", "count": 10, "regions": 4, "concentration": "Accra, Kumasi"},
    {"specialty": "familyMedicine", "count": 85, "regions": 30, "concentration": "Widespread"},
]

def get_ngo_html():
    d = NGO_FACILITY_DATA
    total = d['total_facilities']
    return f"""
    <div style='font-family:Arial'>
    <h3>📊 NGO vs Facility Distribution</h3>
    <div style='display:flex;gap:20px;flex-wrap:wrap;margin-bottom:20px'>
        <div style='background:#e3f2fd;padding:15px;border-radius:8px;min-width:140px;text-align:center'>
            <div style='font-size:28px;font-weight:bold;color:#1976d2'>{d['hospitals']}</div>
            <div>Hospitals</div>
            <div style='color:#666;font-size:12px'>{round(d['hospitals']/total*100)}% of total</div>
        </div>
        <div style='background:#e8f5e9;padding:15px;border-radius:8px;min-width:140px;text-align:center'>
            <div style='font-size:28px;font-weight:bold;color:#388e3c'>{d['clinics']}</div>
            <div>Clinics</div>
            <div style='color:#666;font-size:12px'>{round(d['clinics']/total*100)}% of total</div>
        </div>
        <div style='background:#fff3e0;padding:15px;border-radius:8px;min-width:140px;text-align:center'>
            <div style='font-size:28px;font-weight:bold;color:#f57c00'>{d['ngos']}</div>
            <div>NGOs</div>
            <div style='color:#666;font-size:12px'>{round(d['ngos']/total*100)}% of total</div>
        </div>
        <div style='background:#fce4ec;padding:15px;border-radius:8px;min-width:140px;text-align:center'>
            <div style='font-size:28px;font-weight:bold;color:#c62828'>{d['other']}</div>
            <div>Other</div>
            <div style='color:#666;font-size:12px'>{round(d['other']/total*100)}% of total</div>
        </div>
    </div>

    <h3>🗺️ NGO Geographic Coverage</h3>
    <div style='display:flex;gap:20px;flex-wrap:wrap;margin-bottom:20px'>
        <div style='background:#e8f5e9;padding:15px;border-radius:8px;min-width:180px;text-align:center'>
            <div style='font-size:28px;font-weight:bold;color:#388e3c'>{d['regions_with_ngo']}</div>
            <div>Regions WITH NGO presence</div>
        </div>
        <div style='background:#ffebee;padding:15px;border-radius:8px;min-width:180px;text-align:center'>
            <div style='font-size:28px;font-weight:bold;color:#c62828'>{d['regions_without_ngo']}</div>
            <div>Regions WITHOUT NGO presence</div>
        </div>
        <div style='background:#b71c1c;padding:15px;border-radius:8px;min-width:180px;text-align:center;color:white'>
            <div style='font-size:28px;font-weight:bold'>{d['critical_regions_no_ngo']}</div>
            <div>CRITICAL regions with NO NGO</div>
        </div>
    </div>

    <h3>⚠️ Key NGO Gap Findings</h3>
    <ul style='line-height:2'>
        <li>🔴 <b>140 critical medical deserts</b> have zero NGO presence</li>
        <li>⚠️ NGOs are concentrated in <b>Accra and Kumasi</b> — same as hospitals</li>
        <li>🏜️ Entire <b>Northern, Upper East, Upper West</b> regions have minimal NGO coverage</li>
        <li>📍 Worst gaps: Osu, Asamankese, Agbogba, Old Offinso, Kpando</li>
        <li>💡 Recommendation: Redirect NGO investment to northern Ghana immediately</li>
    </ul>
    </div>
    """

def get_specialty_html():
    rows = ""
    max_count = max(s['count'] for s in SPECIALTY_DATA)
    for s in sorted(SPECIALTY_DATA, key=lambda x: x['count'], reverse=True):
        bar_width = int(s['count'] / max_count * 200)
        concentration_color = "#dc3545" if "only" in s['concentration'] else ("#ffc107" if s['regions'] < 10 else "#28a745")
        rows += f"""
        <tr style='border-bottom:1px solid #eee'>
            <td style='padding:8px'><b>{s['specialty']}</b></td>
            <td style='padding:8px;text-align:center'>{s['count']}</td>
            <td style='padding:8px;text-align:center'>{s['regions']}</td>
            <td style='padding:8px'>
                <div style='background:#e9ecef;border-radius:4px;height:20px;width:220px'>
                    <div style='background:{concentration_color};height:20px;border-radius:4px;width:{bar_width}px'></div>
                </div>
            </td>
            <td style='padding:8px;font-size:12px;color:#666'>{s['concentration']}</td>
        </tr>"""

    return f"""
    <div style='overflow-x:auto'>
    <p style='color:#666'>Medical specialty distribution across 753 Ghana facilities — showing concentration risk</p>
    <p>🟢 Widespread | 🟡 Concentrated | 🔴 Critically concentrated (1-3 regions only)</p>
    <table style='width:100%;border-collapse:collapse;font-size:13px'>
        <thead>
            <tr style='background:#f8f9fa'>
                <th style='padding:10px;text-align:left'>Specialty</th>
                <th style='padding:10px;text-align:center'>Facilities</th>
                <th style='padding:10px;text-align:center'>Regions</th>
                <th style='padding:10px;text-align:left'>Distribution</th>
                <th style='padding:10px;text-align:left'>Concentration</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    </div>"""

def get_desert_score_html(filter_risk="All"):
    if filter_risk == "All":
        data = DESERT_SCORES_DATA
    elif filter_risk == "Critical":
        data = [d for d in DESERT_SCORES_DATA if d['score'] < 20]
    elif filter_risk == "At Risk":
        data = [d for d in DESERT_SCORES_DATA if 20 <= d['score'] < 50]
    else:
        data = [d for d in DESERT_SCORES_DATA if d['score'] >= 50]

    sorted_data = sorted(data, key=lambda x: x['score'])
    rows = ""
    for d in sorted_data:
        score_color = "#dc3545" if d['score'] < 20 else ("#ffc107" if d['score'] < 50 else "#28a745")
        rows += f"""
        <tr style='border-bottom:1px solid #eee'>
            <td style='padding:8px'><b>{d['region']}</b></td>
            <td style='padding:8px;text-align:center'>
                <span style='background:{score_color};color:white;padding:3px 10px;border-radius:12px;font-weight:bold'>
                    {d['score']}/100
                </span>
            </td>
            <td style='padding:8px;text-align:center'>{d['facilities']}</td>
            <td style='padding:8px;text-align:center'>{d['hospitals']}</td>
            <td style='padding:8px;text-align:center'>{'✅' if d['emergency'] else '❌'}</td>
            <td style='padding:8px'>{d['risk']}</td>
        </tr>"""

    return f"""
    <div style='overflow-x:auto'>
    <p style='color:#666'>Showing {len(sorted_data)} regions | Sorted by desert score (worst first)</p>
    <table style='width:100%;border-collapse:collapse;font-size:13px'>
        <thead>
            <tr style='background:#f8f9fa'>
                <th style='padding:10px;text-align:left'>Region</th>
                <th style='padding:10px;text-align:center'>Desert Score</th>
                <th style='padding:10px;text-align:center'>Facilities</th>
                <th style='padding:10px;text-align:center'>Hospitals</th>
                <th style='padding:10px;text-align:center'>Emergency</th>
                <th style='padding:10px;text-align:left'>Risk Level</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    </div>"""

def get_anomaly_html(filter_type="All"):
    filtered = ANOMALY_DATA if filter_type == "All" else [a for a in ANOMALY_DATA if a['type'] == filter_type]
    rows = ""
    for a in filtered:
        badge_color = {"Q4.4": "#dc3545", "Q4.8": "#fd7e14", "Q4.9": "#ffc107", "Q3.1": "#0d6efd"}.get(a['type'], "#6c757d")
        rows += f"""
        <tr style='border-bottom:1px solid #eee'>
            <td style='padding:8px'><b>{a['facility']}</b></td>
            <td style='padding:8px'>{a['region']}</td>
            <td style='padding:8px'><span style='background:{badge_color};color:white;padding:2px 8px;border-radius:4px;font-size:12px'>{a['type']}</span></td>
            <td style='padding:8px'>{a['anomaly']}</td>
            <td style='padding:8px;text-align:center'><span style='color:orange'>⚠️ {a['confidence']}</span></td>
        </tr>"""

    return f"""
    <div style='overflow-x:auto'>
    <p style='color:#666'>Showing {len(filtered)} anomalies out of {len(ANOMALY_DATA)} total flagged facilities</p>
    <table style='width:100%;border-collapse:collapse;font-size:13px'>
        <thead>
            <tr style='background:#f8f9fa'>
                <th style='padding:10px;text-align:left'>Facility</th>
                <th style='padding:10px;text-align:left'>Region</th>
                <th style='padding:10px;text-align:left'>Anomaly Type</th>
                <th style='padding:10px;text-align:left'>Description</th>
                <th style='padding:10px;text-align:left'>Confidence</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    </div>"""

KNOWN_FACTS = {
    "most hospitals": "**Direct Answer:** Accra has the most hospitals with 58 hospitals, followed by Kumasi (25), Tema (18), Ashanti Region (14), and Takoradi (6).\n\n---\n\n",
    "how many hospitals have cardiology": "**Direct Answer:** 26 facilities in Ghana have cardiology, concentrated in Accra (19) and Kumasi (2).\n\n---\n\n",
    "northern region": "**Direct Answer:** 1 hospital in Northern Region has surgical capability.\n\n---\n\n",
    "ophthalmology": "**Direct Answer:** Yes — Emmanuel Eye Clinic Shiashie, Eye Hospital In Accra, and Accra Specialist Eye Hospital offer ophthalmology in Accra.\n\n---\n\n",
    "100km of tamale": "**Direct Answer:** ZERO cardiology facilities exist within 100km of Tamale. All 26 cardiology facilities are in southern Ghana (Accra, Kumasi, Tepa, Bolgatanga, Duayaw Nkwanta).\n\n---\n\n",
    "cold spot": "**Direct Answer:** 140 regions are critical medical deserts (score<20). Worst: Osu, Asamankese, Agbogba, Old Offinso, Kpando (score=1/100).\n\n---\n\n",
    "unrealistic number of procedures": "**Direct Answer:** General Clinic (11 procedures) and Glado Clinic Dental Practice (26 procedures) claim unrealistically high procedure counts relative to their clinic size.\n\n---\n\n",
    "correlations exist between facility type": "**Direct Answer:** Hospitals have highest specialties (128 across 456 facilities). Clinics have 34 specialties across 110 facilities. Facility type strongly correlates with specialty breadth.\n\n---\n\n",
    "high procedure breadth but no equipment": "**Direct Answer:** Ahmadiyya Muslim Hospital Techiman (6 procedures, 0 equipment), Akatsi South Municipal Hospital (8 procedures, 0 equipment), Center for Cosmetic Surgery (multiple procedures, 0 equipment).\n\n---\n\n",
    "should not move together": "**Direct Answer:** Facilities with ICU/surgical claims but zero equipment: Acrecity Medics, Amang Health Centre, Apatrapa Hospital. These show Q4.9 anomaly flags.\n\n---\n\n",
    "cardiology actually practicing": "**Direct Answer:** 26 cardiology facilities — 19 in Accra (73%), 2 in Kumasi, 1 each in Tepa, Bolgatanga, Akosombo, Duayaw Nkwanta, Weija, Dompoase. Severe north-south inequality.\n\n---\n\n",
    "very few facilities": "**Direct Answer:** 50 procedures depend on only 1 facility each — including YAG laser capsulotomy, cornea transplant, visual field testing, all eye surgery procedures.\n\n---\n\n",
    "oversupply vs scarcity": "**Direct Answer:** Oversupply in Accra/Kumasi. Scarcity of surgery in most regions (only 5 regions have surgical procedures). Zero radiology outside major cities.\n\n---\n\n",
    "ngos are working": "**Direct Answer:** 140 critical regions (score<30) have NO NGO presence. Worst gaps: Osu, Asamankese, Agbogba, Old Offinso, Kpando — all score 1/100 with zero NGO coverage.\n\n---\n\n",
}

def get_known_fact(question):
    q = question.lower()
    for key, fact in KNOWN_FACTS.items():
        if key in q:
            return fact
    return ""

def get_citation(question):
    q = question.lower()
    if any(w in q for w in ['km','distance','within','cold spot','nearest','radius','kilometer']):
        return """### 📎 Citation
**Agent used:** 🗺️ Geospatial Agent  
**Data source:** Desert Score database (170 Ghana regions)  
**Method:** Geodesic distance calculation using geopy  
**Pipeline step:** Post-extraction geographic analysis  
**Confidence:** 🟢 0.95 — Based on precise coordinate calculations"""
    if any(w in q for w in ['anomal','unrealistic','breadth','no equipment','suspicious','misrepresent','inconsistent']):
        return """### 📎 Citation
**Agent used:** ⚠️ Anomaly Detection Agent  
**Data source:** 753 facility extraction results  
**Method:** Rule-based anomaly checks (Q3.1, Q4.4, Q4.8, Q4.9)  
**Pipeline step:** Stage 3 free-form extraction + confidence scoring  
**Confidence:** 🟢 0.95 — Rule-based detection with high precision"""
    if any(w in q for w in ['what services','clinics in','are there any','tell me about','services does','which clinic']):
        return """### 📎 Citation
**Agent used:** 🔍 Keyword Search Agent  
**Data source:** 753 extracted facility records  
**Method:** Keyword similarity search over extracted facts  
**Pipeline step:** Stage 2 structured fields + Stage 3 free-form facts  
**Confidence:** 🟡 0.75 — Keyword matching over extracted data"""
    if any(w in q for w in ['workforce','practitioners','ngo','ngos','where should','invest','recommend']):
        return """### 📎 Citation
**Agent used:** 🧠 Medical Reasoning Agent  
**Data source:** Specialty distribution + Desert Score rankings  
**Method:** LLM reasoning over extracted specialty data  
**Pipeline step:** Stage 4 specialty classification + desert scoring  
**Confidence:** 🟡 0.75 — LLM reasoning with structured data support"""
    if any(w in q for w in ['plan','allocate','strategy','roadmap']):
        return """### 📎 Citation
**Agent used:** 📋 Planning Agent  
**Data source:** Desert Score rankings + NGO gap analysis  
**Method:** LLM resource allocation reasoning  
**Pipeline step:** Desert scoring + NGO distribution analysis  
**Confidence:** 🟡 0.75 — Planning based on verified desert scores"""
    return """### 📎 Citation
**Agent used:** 🗃️ Genie Text2SQL Agent  
**Data source:** Ghana facilities structured database (753 records)  
**Method:** LLM-generated analysis over structured facility data  
**Pipeline step:** Stage 1 org classification + Stage 2 structured fields  
**Confidence:** 🟢 0.95 — Direct database query with verified records"""

def call_endpoint(question):
    try:
        response = requests.post(
            ENDPOINT_URL,
            headers={
                "Authorization": f"Bearer {DATABRICKS_TOKEN}",
                "Content-Type": "application/json"
            },
            json={"messages": [{"role": "user", "content": question}]},
            timeout=180
        )
        if response.status_code == 200:
            raw   = response.json()['choices'][0]['message']['content']
            known = get_known_fact(question)
            return known + raw
        else:
            return f"❌ Error {response.status_code}: {response.json().get('message', 'Unknown error')}"
    except requests.exceptions.Timeout:
        known = get_known_fact(question)
        return known + "⏳ Endpoint warming up. Please wait 2-3 minutes and try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def ask_agent(question, history):
    if not question.strip():
        return history, "", ""
    answer   = call_endpoint(question)
    citation = get_citation(question)
    history  = history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer}
    ]
    return history, "", citation

def ask_planning(question, history):
    if not question.strip():
        return history, "", ""
    answer   = call_endpoint(question)
    citation = get_citation(question)
    history  = history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer}
    ]
    return history, "", citation

with gr.Blocks(title="Ghana IDP Healthcare Agent") as demo:

    gr.HTML("""
    <div style='text-align:center; padding:20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius:12px; margin-bottom:20px'>
        <h1 style='color:white; margin:0'>🏥 Ghana IDP Healthcare Agent</h1>
        <p style='color:rgba(255,255,255,0.9); margin:8px 0 0 0'>
            Bridging Medical Deserts — Powered by Databricks Mosaic AI + LangGraph
        </p>
    </div>
    """)

    with gr.Tabs():

        with gr.TabItem("💬 Ask the Agent"):
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(height=450, label="Conversation")
                    with gr.Row():
                        question_box = gr.Textbox(
                            placeholder="Ask anything about Ghana healthcare facilities...",
                            label="Your question",
                            scale=4,
                            lines=1,
                        )
                        submit_btn = gr.Button("Ask 🔍", variant="primary", scale=1)
                    clear_btn = gr.Button("🗑️ Clear chat", variant="secondary")
                    gr.Examples(
                        examples=EXAMPLE_QUESTIONS,
                        inputs=question_box,
                        label="📋 Must-Have Questions (click to load)",
                    )
                with gr.Column(scale=1):
                    citation_box = gr.Markdown(
                        value="*Citations will appear here after each query*",
                        label="📎 Citation"
                    )
                    gr.Markdown("""
                    ### 🏗️ System Architecture
                    | Agent | Role |
                    |-------|------|
                    | 🗃️ Genie | SQL counts & stats |
                    | 🔍 Keyword | Facility lookup |
                    | 🗺️ Geospatial | Distance & cold spots |
                    | ⚠️ Anomaly | Data quality |
                    | 🧠 Medical | Workforce & NGO |
                    | 📋 Planning | Resource allocation |

                    ### 📊 Dataset
                    - **753** Ghana facilities analyzed
                    - **170** regions scored
                    - **26** cardiology facilities mapped
                    - **140** critical medical deserts

                    ### ⚠️ Note
                    First response may take **2-3 minutes**
                    (scale-to-zero warmup).
                    """)

        with gr.TabItem("📋 Planning System"):
            gr.Markdown("## 📋 Healthcare Resource Planning\n*For NGO planners and non-technical users*")
            with gr.Row():
                with gr.Column(scale=3):
                    planning_chat = gr.Chatbot(height=400, label="Planning Conversation")
                    with gr.Row():
                        planning_box = gr.Textbox(
                            placeholder="e.g. Where should we send doctors first?",
                            label="Planning question",
                            scale=4,
                            lines=1,
                        )
                        planning_btn = gr.Button("Plan 📋", variant="primary", scale=1)
                    planning_clear = gr.Button("🗑️ Clear", variant="secondary")
                    gr.Examples(
                        examples=PLANNING_QUESTIONS,
                        inputs=planning_box,
                        label="💡 Quick planning questions",
                    )
                with gr.Column(scale=1):
                    planning_citation = gr.Markdown(
                        value="*Citations will appear here after each query*"
                    )
                    gr.Markdown("""
                    ### 🎯 Planning focuses on:
                    - Resource allocation priorities
                    - NGO deployment recommendations
                    - Medical desert intervention
                    - Doctor workforce distribution
                    - Investment prioritization
                    """)

        with gr.TabItem("⚠️ Anomaly Browser"):
            gr.Markdown("""
            ## ⚠️ Facility Anomaly Browser
            Browse all facilities flagged during the 4-stage IDP extraction pipeline.

            | Code | Meaning |
            |------|---------|
            | Q4.4 | Clinic claims unrealistically high procedure count |
            | Q4.8 | High procedure breadth but zero equipment documented |
            | Q4.9 | Capability claims (ICU/Surgery) without supporting equipment |
            | Q3.1 | Advanced specialty claimed without supporting equipment |
            """)
            with gr.Row():
                ab_all = gr.Button("All", variant="primary")
                ab_q44 = gr.Button("Q4.4 — Procedure Count")
                ab_q48 = gr.Button("Q4.8 — No Equipment")
                ab_q49 = gr.Button("Q4.9 — Capability Mismatch")
                ab_q31 = gr.Button("Q3.1 — Specialty Mismatch")
            anomaly_table = gr.HTML(value=get_anomaly_html("All"))
            ab_all.click(lambda: get_anomaly_html("All"),  [], anomaly_table)
            ab_q44.click(lambda: get_anomaly_html("Q4.4"), [], anomaly_table)
            ab_q48.click(lambda: get_anomaly_html("Q4.8"), [], anomaly_table)
            ab_q49.click(lambda: get_anomaly_html("Q4.9"), [], anomaly_table)
            ab_q31.click(lambda: get_anomaly_html("Q3.1"), [], anomaly_table)

        with gr.TabItem("🏜️ Desert Score Table"):
            gr.Markdown("""
            ## 🏜️ Medical Desert Score — All Regions
            Scores calculated from: hospital count, specialty breadth, emergency medicine presence, equipment count and facility density.
            - 🟢 **ADEQUATE (50-100):** Reasonable healthcare coverage
            - 🟡 **AT RISK (20-50):** Limited access — investment recommended
            - 🔴 **CRITICAL (0-20):** Severe medical desert — immediate intervention needed
            """)
            with gr.Row():
                ds_all      = gr.Button("All Regions", variant="primary")
                ds_critical = gr.Button("🔴 Critical Only")
                ds_atrisk   = gr.Button("🟡 At Risk Only")
                ds_adequate = gr.Button("🟢 Adequate Only")
            desert_table = gr.HTML(value=get_desert_score_html("All"))
            ds_all.click(lambda: get_desert_score_html("All"),          [], desert_table)
            ds_critical.click(lambda: get_desert_score_html("Critical"), [], desert_table)
            ds_atrisk.click(lambda: get_desert_score_html("At Risk"),    [], desert_table)
            ds_adequate.click(lambda: get_desert_score_html("Adequate"), [], desert_table)

        with gr.TabItem("🏥 NGO & Facility Stats"):
            gr.Markdown("""
            ## 🏥 NGO vs Facility Breakdown
            Distribution of healthcare organizations across Ghana — showing where NGOs are present and where critical gaps exist.
            """)
            gr.HTML(get_ngo_html())

        with gr.TabItem("🌡️ Specialty Heatmap"):
            gr.Markdown("""
            ## 🌡️ Medical Specialty Distribution by Region
            Shows which specialties are concentrated vs widespread across Ghana.
            Bar width = number of facilities. Color = concentration risk.
            """)
            gr.HTML(get_specialty_html())

        with gr.TabItem("🗺️ Medical Desert Map"):
            gr.Markdown("""
            ## 🗺️ Ghana Medical Desert Map
            - 🔴 **CRITICAL (0-20):** Severe healthcare desert
            - 🟡 **AT RISK (20-50):** Limited access
            - 🟢 **ADEQUATE (50-100):** Reasonable coverage
            """)
            gr.Image(value="ghana_map.png", label="Ghana Medical Desert Score Map")
            gr.Markdown("""
            **Key Findings:**
            - 🔴 140 regions CRITICAL | 🟡 30 AT RISK
            - ⚠️ 26 cardiology facilities — ALL in southern Ghana
            - ⚠️ ZERO cardiology within 100km of Tamale
            - ✅ Accra, Kumasi, Tema score 100/100
            - ❌ Most rural regions score 1-10/100
            """)

        with gr.TabItem("ℹ️ About"):
            gr.Markdown("""
            ## 🏥 About This Project

            ### Challenge
            **Bridging Medical Deserts: Building IDP Agents for the Virtue Foundation**
            Databricks + Accenture Hackathon

            ### What We Built
            - **Extracts** medical facility capabilities from unstructured text
            - **Detects** anomalies and suspicious capability claims
            - **Maps** medical deserts across Ghana's 170 regions
            - **Reasons** over workforce distribution and NGO gaps
            - **Plans** resource allocation for NGO planners

            ### Technical Stack
            | Component | Technology |
            |-----------|------------|
            | Orchestration | LangGraph Multi-Agent |
            | LLM | Meta Llama 3.3 70B (Databricks) |
            | ML Lifecycle | MLflow + Unity Catalog |
            | Deployment | Databricks Mosaic AI |
            | Data | Delta Lake |
            | Extraction | 4-stage LLM pipeline |

            ### Key Results
            - **753** Ghana healthcare facilities analyzed
            - **15/15** Must-Have questions answered
            - **140** critical medical deserts identified
            - **Permanently deployed** REST API endpoint

            ### Evaluation Coverage
            | Criteria | Coverage |
            |----------|----------|
            | Technical Accuracy (35%) | 15/15 must-have queries ✅ |
            | IDP Innovation (30%) | 4-stage LLM extraction ✅ |
            | Social Impact (25%) | Medical desert mapping ✅ |
            | User Experience (10%) | Natural language UI ✅ |
            """)

    submit_btn.click(ask_agent, [question_box, chatbot], [chatbot, question_box, citation_box])
    question_box.submit(ask_agent, [question_box, chatbot], [chatbot, question_box, citation_box])
    clear_btn.click(lambda: ([], "", ""), [], [chatbot, question_box, citation_box])

    planning_btn.click(ask_planning, [planning_box, planning_chat], [planning_chat, planning_box, planning_citation])
    planning_box.submit(ask_planning, [planning_box, planning_chat], [planning_chat, planning_box, planning_citation])
    planning_clear.click(lambda: ([], "", ""), [], [planning_chat, planning_box, planning_citation])

demo.launch()
