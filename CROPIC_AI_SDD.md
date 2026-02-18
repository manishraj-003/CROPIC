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
