# SYSTEM DESIGN DOCUMENT (SDD) CROPIC-AI for PMFBY

## System Architecture

Mobile App → API Gateway → AI Processing Layer → Database  
↓  
Satellite NDVI Engine  
↓  
Web Dashboard

## AI Components

1\. Image Quality Validator  
2. CNN-based Crop & Damage Classifier  
3. U-Net/DeepLabV3+ Segmentation Model  
4. NDVI Cross-Verification Engine  
5. Fraud Detection Module

## Damage Quantification Formula

Damage Ratio (φ) = Damaged Pixels / Total Plant Pixels

## NDVI Formula

NDVI = (NIR - RED) / (NIR + RED)

## Database Design

Tables: Users, Farms, Images, Damage Assessments, Satellite Records, Claims, Fraud Logs.

## Deployment Strategy

Cloud-native microservices architecture using Docker & Kubernetes, auto-scaling, CDN-based image delivery, optional edge inference using TensorRT.

## Explainable AI

Use SHAP and LIME for interpretability. Provide visual heatmaps and feature importance for insurance claim transparency.

**SYSTEM DESIGN DOCUMENT (SDD): CROPIC-AI (v2.0)**

**Updated Theme:** Retail-Grade POS Web UI/UX (Ronas IT Inspired)

**1. Visual Identity & UI/UX Strategy**

The interface is updated from a standard utility dashboard to a \"High-End Retail Analytics\" style to improve user engagement and transparency.

- **Color Palette:** A \"Modern Dark/Light Hybrid\" scheme.

  - **Base:** Neutral grayscale (#F9FAF5 or \#0C090A) for a clean gallery feel.

  - **Accents:** Saturated \"Nature-Tech\" gradients (Forest Green for healthy NDVI, Burnt Orange for damage, and Coral Red for fraud alerts) to highlight critical actions.

- **Typography:** Professional, sans-serif high-contrast fonts to ensure readability of complex crop metrics.

- **Layout:** A \"Three-Column Dashboard\" inspired by POS systems:

  - **Left:** Global Navigation (Claims, Farm Maps, Analytics).

  - **Center:** Main Canvas (Interactive satellite maps & crop health heatmaps).

  - **Right:** Detail Panel (Individual farmer profiles, damage quantification, and claim status).

**2. Updated System Architecture**

The architecture shifts to a \"Retail-Storefront\" model where individual farms are treated as \"assets\" in a real-time inventory system.

- **Mobile App (Field Agent):** Focused on \"Product Capture\" (Image Quality Validator) with a seamless, native-feel UI.

- **Web Dashboard (Insurer):** A high-load \"Command Center\" featuring:

  - **Real-Time Metrics:** Cards for Total Claims, Pending Assessments, and Damage Ratios.

  - **Analytics Graph:** Monthly damage trends and regional risk heatmaps using monthly/weekly filters.

**3. AI Processing & Feature Enhancements**

AI components are now integrated into the UI as \"Smart Recommendations\" similar to retail cross-selling engines.

- **Explainable AI (XAI) Heatmaps:** Instead of raw data, SHAP/LIME outputs are rendered as \"Visual Overlays\" on farm images, allowing insurance adjusters to see exactly *why* the AI flagged damage.

- **Fraud Detection Module:** Modeled after \"Transaction Fraud Logs\" in POS systems, flagging anomalies in image metadata or satellite mismatches.

**4. Database & Functional Modules**

The data structure remains robust but is categorized for \"E-commerce Efficiency\":

- **Asset Management:** Table: Farms (treated as products with SKU-like IDs).

- **Transaction Logs:** Table: Claims (tracked with Status, Date, and Cost identifiers).

- **Satellite Records:** Table: NDVI_History (Integrated with monthly mini-calendars for temporal health tracking).

**5. Technical Specifications**

- **Frontend:** React / Next.js for high-performance server-side rendering (SSR) and SEO-optimized admin panels.

- **Backend:** Cloud-native microservices (Docker & Kubernetes) with PostgreSQL for structured claim data and MongoDB for unstructured image metadata.

- **Edge Inference:** Optional TensorRT for instant image validation on-field, reducing server round-trip time.

**6. Delivery & Scaling**

- **Responsive Design:** Optimized for tablet use by field inspectors and desktop use by headquarters.

- **Rapid Deployment:** Utilizing a \"Design System\" approach for quick UI scaling as more crop types or insurance products are added.
