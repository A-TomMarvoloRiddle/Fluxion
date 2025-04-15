# FLUXION - AI-based Traffic Management System

![FLUXION](https://via.placeholder.com/800x400?text=FLUXION+Traffic+Management+System)

## 🌟 Overview

FLUXION is an advanced AI-powered traffic management system designed to optimize traffic flow, reduce congestion, and enhance road safety. By leveraging computer vision, machine learning, and reinforcement learning technologies, FLUXION dynamically adjusts traffic signals based on real-time traffic conditions.
This system aims to revolutionize traditional fixed-time traffic signal systems with intelligent, adaptive solutions that respond to actual traffic demands.

## 🔧 Core Features

### Advanced Computer Vision
- Real-time vehicle detection, classification, and tracking at intersections
- Utilizes YOLOv10 for accurate object detection (cars, buses, trucks, motorcycles)
- Multi-class vehicle recognition with confidence thresholds

### Reinforcement Learning (RL)
- Dynamic adjustment of traffic light timings based on real-time vehicle counts
- Reward-penalty system that learns from traffic flow patterns
- Optimizes green time allocation to minimize overall waiting time

### Recurrent Neural Network (RNN) Backup
- Fallback prediction model that handles system failures or unexpected scenarios
- Time-series based traffic prediction using historical data
- LSTM architecture for accurate traffic flow forecasting

### Region of Interest (ROI) Detection
- Focused monitoring of critical intersection areas
- Customizable detection zones for improved accuracy and efficiency
- Reduces computational overhead by focusing on relevant areas

### Cyclic Signal System
- Maintains predictable traffic signal patterns for driver familiarity

### Number Plate Recognition
- Automatically captures license plates of vehicles violating traffic rules
- Stores violation data for potential enforcement actions
- High-accuracy plate detection even in varying lighting conditions

### SUMO Simulation Integration
- Pre-deployment testing using Simulation of Urban Mobility platform
- Scenario-based testing for system robustness

### Weather API Integration
- Switches to RNN model when low visibility threshold is crossed 
- Enhanced visibility compensation during adverse weather

### Flask-based Web Interface
- Real-time monitoring dashboard for traffic conditions
- User-friendly control panel for system parameters
- Visualization of traffic flows and signal timings

### Maps API Integration
- Supplements camera data in infrastructure-limited areas
- Prediction of incoming traffic based on nearby conditions

## 🔍 Technical Implementation

### Technologies Used

- **Python**: Core programming language
- **OpenCV**: Computer vision and image processing
- **Ultralytics YOLO**: Object detection
- **TensorFlow & Keras**: Deep learning models (LSTM)
- **NumPy & Matplotlib**: Data processing and visualization
- **Scikit-learn**: Machine learning utilities

## 🔮 Future Work

- Integration with smart city infrastructure
- Vehicle-to-infrastructure (V2I) communication
- Machine learning enhancements for predictive traffic management
- Mobile application for driver notifications
- Expansion to pedestrian and cyclist safety features

## 👥 Authors

- Apaar Mathur 
- Daksh Sharma
- Keshav Shrimali
- Aryan Jain
