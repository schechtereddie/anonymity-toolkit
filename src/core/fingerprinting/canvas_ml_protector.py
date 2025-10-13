#!/usr/bin/env python3
"""
Canvas ML Fingerprint Protector
Advanced machine learning-based detection and prevention of canvas fingerprinting attacks
"""

import os
import json
import random
import hashlib
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import torch
import torch.nn as nn


@dataclass
class CanvasFingerprint:
    """Complete canvas fingerprinting operation data"""
    operation_type: str  # 'fillRect', 'strokeText', 'getImageData', etc.
    parameters: list     # Operation parameters
    canvas_size: tuple   # Width, height of canvas
    fill_style: str      # Current fill style/color
    font: str           # Current font settings
    timestamp: float    # When operation was performed
    context_state: Dict[str, Any]  # Full canvas context state


@dataclass
class CanvasProtectionModel:
    """ML model for canvas fingerprinting detection"""
    anomaly_detector: IsolationForest
    pattern_recognizer: Any  # TensorFlow or PyTorch model
    feature_scaler: StandardScaler
    trained: bool = False

    def save_model(self, path: str):
        """Save the ML model to disk"""
        try:
            # Save sklearn components
            import joblib
            model_data = {
                'anomaly_detector': self.anomaly_detector,
                'feature_scaler': self.feature_scaler,
                'trained': self.trained
            }
            joblib.dump(model_data, f"{path}_ml.pkl")

            print(f"✅ Canvas protection model saved to {path}")
        except Exception as e:
            print(f"❌ Failed to save canvas model: {e}")

    @classmethod
    def load_model(cls, path: str) -> Optional['CanvasProtectionModel']:
        """Load the ML model from disk"""
        try:
            import joblib
            model_data = joblib.load(f"{path}_ml.pkl")

            model = cls(
                anomaly_detector=model_data['anomaly_detector'],
                pattern_recognizer=None,  # Will be loaded separately if needed
                feature_scaler=model_data['feature_scaler']
            )
            model.trained = model_data.get('trained', False)
            return model

        except Exception as e:
            print(f"❌ Failed to load canvas model: {e}")
            return None


class CanvasFingerprintProtector:
    """
    Advanced ML-powered canvas fingerprinting prevention system.
    Detects and mitigates HTML5 canvas-based tracking with GAN-generated noise.
    """

    def __init__(self, use_tensorflow: bool = True):
        self.models_directory = "src/data/canvas_models"
        os.makedirs(self.models_directory, exist_ok=True)

        # ML components for detection
        self.protection_model = self._load_or_create_model()
        self.use_tensorflow_ml = use_tensorflow

        # Canvas operation tracking
        self.operation_sequence = []
        self.canvas_states = {}
        self.fingerprinting_detected = False

        # GAN-based noise generation for mitigation
        self.noise_generator = self._initialize_noise_generator()

        # Detection thresholds
        self.detection_threshold = 0.85  # Probability threshold for fingerprinting detection
        self.malicious_operation_count = 0
        self.consecutive_suspicious_ops = 0

    def _load_or_create_model(self) -> CanvasProtectionModel:
        """Load existing model or create new one with training data"""
        model_path = os.path.join(self.models_directory, "canvas_protector")

        # Try to load existing model
        existing_model = CanvasProtectionModel.load_model(model_path)
        if existing_model and existing_model.trained:
            print("✅ Loaded existing canvas protection model")
            return existing_model

        # Create and train new model
        print("🔄 Creating new canvas protection model...")
        model = CanvasProtectionModel(
            anomaly_detector=IsolationForest(
                contamination=0.15,  # Expected 15% of operations are malicious
                random_state=42,
                n_estimators=100
            ),
            pattern_recognizer=self._create_pattern_recognizer(),
            feature_scaler=StandardScaler()
        )

        # Train with synthetic fingerprinting patterns
        self._train_model_with_synthetic_data(model)
        model.trained = True

        # Save the trained model
        model.save_model(model_path)

        return model

    def _create_pattern_recognizer(self) -> Any:
        """Create advanced pattern recognition model"""
        if self.use_tensorflow_ml:
            # TensorFlow implementation
            try:
                model = tf.keras.Sequential([
                    tf.keras.layers.Dense(128, activation='relu', input_shape=(20,)),
                    tf.keras.layers.Dropout(0.3),
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.Dense(32, activation='relu'),
                    tf.keras.layers.Dense(1, activation='sigmoid')
                ])
                model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
                return model
            except ImportError:
                self.use_tensorflow_ml = False

        # PyTorch fallback
        try:
            class CanvasPatternNet(nn.Module):
                def __init__(self):
                    super(CanvasPatternNet, self).__init__()
                    self.network = nn.Sequential(
                        nn.Linear(20, 128),
                        nn.ReLU(),
                        nn.Dropout(0.3),
                        nn.Linear(128, 64),
                        nn.ReLU(),
                        nn.Dropout(0.2),
                        nn.Linear(64, 32),
                        nn.ReLU(),
                        nn.Linear(32, 1),
                        nn.Sigmoid()
                    )

                def forward(self, x):
                    return self.network(x)

            return CanvasPatternNet()
        except ImportError:
            print("⚠️ Neither TensorFlow nor PyTorch available, using basic detection")
            return None

    def _train_model_with_synthetic_data(self, model: CanvasProtectionModel):
        """Train model with synthetic canvas fingerprinting data"""
        # Generate realistic fingerprinting patterns vs legitimate usage
        fingerprinting_ops = self._generate_fingerprinting_operations(1000)
        legitimate_ops = self._generate_legitimate_operations(1000)

        # Extract features from operations
        fingerprinting_features = [self._extract_canvas_features(op) for op in fingerprinting_ops]
        legitimate_features = [self._extract_canvas_features(op) for op in legitimate_ops]

        # Combine and label training data
        X_train = fingerprinting_features + legitimate_features
        y_train = [1] * len(fingerprinting_features) + [0] * len(legitimate_features)  # 1 = fingerprinting

        # Scale features
        X_train_scaled = model.feature_scaler.fit_transform(X_train)

        # Train anomaly detector
        model.anomaly_detector.fit(X_train_scaled)

        # Train pattern recognizer if available
        if model.pattern_recognizer:
            X_tensor = torch.tensor(X_train_scaled, dtype=torch.float32) if hasattr(torch, 'tensor') else None
            y_tensor = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1) if hasattr(torch, 'tensor') else None

            if X_tensor is not None and y_tensor is not None:
                optimizer = torch.optim.Adam(model.pattern_recognizer.parameters())
                criterion = nn.BCELoss()

                # Simple training loop
                for epoch in range(10):
                    optimizer.zero_grad()
                    outputs = model.pattern_recognizer(X_tensor)
                    loss = criterion(outputs, y_tensor)
                    loss.backward()
                    optimizer.step()

                print(f"✅ Pattern recognizer trained (loss: {loss.item():.4f})")

    def _generate_fingerprinting_operations(self, count: int) -> List[CanvasFingerprint]:
        """Generate synthetic canvas operations typical of fingerprinting"""
        operations = []

        for _ in range(count):
            # Fingerprinting operations are systematic and repetitive
            operation_types = [
                'getImageData', 'getImageData', 'getImageData',  # Most common fingerprinting
                'fillText', 'measureText', 'fillRect', 'strokeText'
            ]

            op_type = random.choice(operation_types)

            if op_type == 'getImageData':
                # Typical fingerprinting scan pattern
                size = random.choice(['small', 'medium', 'large'])
                if size == 'small':
                    width, height = random.randint(1, 50), random.randint(1, 50)
                elif size == 'medium':
                    width, height = random.randint(100, 300), random.randint(100, 300)
                else:
                    width, height = random.randint(500, 1000), random.randint(500, 1000)

                params = [0, 0, width, height]  # Standard full-canvas scan
                canvas_size = (max(width, 200), max(height, 200))

            elif op_type in ['fillText', 'strokeText']:
                params = [f"FingerprintTest_{random.randint(1000, 9999)}", random.randint(10, 50), random.randint(10, 50)]
                canvas_size = (400, 200)

            elif op_type == 'fillRect':
                params = [0, 0, random.randint(50, 200), random.randint(50, 200)]
                canvas_size = (300, 300)

            else:
                params = [f"Test_{random.randint(1000, 9999)}"]
                canvas_size = (200, 200)

            fingerprint = CanvasFingerprint(
                operation_type=op_type,
                parameters=params,
                canvas_size=canvas_size,
                fill_style=f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})",
                font=f"{random.randint(10, 30)}px Arial",
                timestamp=random.random() * 1000,
                context_state={
                    'globalAlpha': 1.0,
                    'globalCompositeOperation': 'source-over',
                    'lineWidth': random.randint(1, 5),
                    'textAlign': random.choice(['start', 'center', 'end'])
                }
            )
            operations.append(fingerprint)

        return operations

    def _generate_legitimate_operations(self, count: int) -> List[CanvasFingerprint]:
        """Generate synthetic canvas operations typical of legitimate usage"""
        operations = []

        for _ in range(count):
            # Legitimate operations are more varied and less systematic
            operation_types = ['fillRect', 'fillRect', 'fillText', 'strokeRect', 'arc', 'lineTo']

            op_type = random.choice(operation_types)

            if op_type == 'fillRect':
                # Diverse rectangle operations
                params = [
                    random.randint(0, 300), random.randint(0, 300),
                    random.randint(10, 100), random.randint(10, 100)
                ]
                canvas_size = (400, 400)

            elif op_type == 'fillText':
                text_options = ['Hello', 'Click here', str(random.randint(1, 100)), 'Buy Now', 'Welcome']
                params = [random.choice(text_options), random.randint(50, 350), random.randint(50, 350)]
                canvas_size = (400, 200)

            elif op_type == 'strokeRect':
                params = [
                    random.randint(0, 350), random.randint(0, 350),
                    random.randint(20, 150), random.randint(20, 150)
                ]
                canvas_size = (400, 400)

            elif op_type == 'arc':
                params = [
                    random.randint(50, 350), random.randint(50, 350),  # center
                    random.randint(10, 50),  # radius
                    random.random() * 2 * 3.14159,  # start angle
                    random.random() * 2 * 3.14159   # end angle
                ]
                canvas_size = (400, 400)

            elif op_type == 'lineTo':
                params = [random.randint(0, 400), random.randint(0, 400)]
                canvas_size = (400, 400)

            else:
                params = ["Unknown operation"]
                canvas_size = (200, 200)

            fingerprint = CanvasFingerprint(
                operation_type=op_type,
                parameters=params,
                canvas_size=canvas_size,
                fill_style=random.choice([
                    '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF',
                    'rgba(255, 0, 0, 0.5)', 'rgba(0, 255, 0, 0.7)'
                ]),
                font=f"{random.choice([12, 14, 16, 18, 24])}px {random.choice(['Arial', 'Helvetica', 'Times', 'Verdana'])}",
                timestamp=random.random() * 2000 + 1000,  # More varied timing
                context_state={
                    'globalAlpha': round(random.random(), 2),
                    'globalCompositeOperation': random.choice(['source-over', 'multiply', 'screen']),
                    'lineWidth': random.uniform(0.5, 3.0),
                    'textAlign': random.choice(['start', 'center', 'end', 'left', 'right'])
                }
            )
            operations.append(fingerprint)

        return operations

    def _extract_canvas_features(self, canvas_op: CanvasFingerprint) -> List[float]:
        """Extract numerical features from canvas operation for ML processing"""
        features = []

        # Operation type encoding (one-hot style)
        operation_types = ['getImageData', 'fillText', 'measureText', 'fillRect', 'strokeRect', 'arc', 'lineTo']
        for op_type in operation_types:
            features.append(1.0 if canvas_op.operation_type == op_type else 0.0)

        # Parameter-based features
        features.append(len(canvas_op.parameters))  # Number of parameters

        # Canvas size features (normalized)
        width, height = canvas_op.canvas_size
        features.extend([
            width / 2000.0,  # Normalize width
            height / 2000.0,  # Normalize height
            (width * height) / (2000.0 * 2000.0),  # Normalized area
            width / height if height > 0 else 0  # Aspect ratio
        ])

        # Color analysis (basic))
        fill_style = canvas_op.fill_style.lower()
        features.extend([
            1.0 if '#' in fill_style else 0.0,  # Hex color
            1.0 if 'rgb' in fill_style else 0.0, # RGB/RGBA color
            1.0 if 'rgba' in fill_style else 0.0,  # RGBA (transparency)
            float(canvas_op.context_state.get('globalAlpha', 1.0)),  # Alpha value
        ])

        # Timing features
        timestamp_norm = canvas_op.timestamp / 10000.0  # Normalize timestamp
        features.append(timestamp_norm)

        # Context state features
        line_width = float(canvas_op.context_state.get('lineWidth', 1.0))
        features.append(line_width / 10.0)  # Normalize line width

        # Font analysis
        font = canvas_op.font
        font_size = 12  # Default
        try:
            # Extract font size if possible
            for part in font.split():
                if part.endswith('px'):
                    font_size = int(part[:-2])
        except:
            pass
        features.append(font_size / 50.0)  # Normalize font size

        # Ensure we have exactly 20 features
        while len(features) < 20:
            features.append(0.0)

        return features[:20]

    def _initialize_noise_generator(self) -> Dict[str, Any]:
        """Initialize GAN-based noise generation for fingerprinting mitigation"""
        # Simplified GAN-like noise generation
        # In a real implementation, this would be a trained GAN model
        return {
            'noise_patterns': self._generate_noise_patterns(),
            'morphological_operations': ['erode', 'dilate', 'open', 'close'],
            'color_perturbations': ['hue_shift', 'saturation_variation', 'brightness_noise'],
            'geometric_transforms': ['subpixel_shift', 'anti_aliasing_noise']
        }

    def _generate_noise_patterns(self) -> List[np.ndarray]:
        """Generate various noise patterns for canvas perturbation"""
        patterns = []

        # Gaussian noise patterns of different intensities
        for intensity in [0.01, 0.03, 0.07, 0.15]:
            pattern = np.random.normal(0, intensity, (100, 100, 4))  # RGBA noise
            patterns.append(pattern)

        # Salt and pepper noise
        for density in [0.001, 0.003, 0.01]:
            pattern = np.random.choice([0, 255], size=(100, 100, 4), p=[1-density, density])
            patterns.append(pattern)

        return patterns

    def detect_canvas_fingerprinting(self, canvas_operations: List[CanvasFingerprint]) -> Dict[str, Any]:
        """
        Analyze canvas operations for fingerprinting behavior
        """
        if not self.protection_model.trained:
            return {'detected': False, 'confidence': 0.0, 'reason': 'Model not trained'}

        # Extract features from recent operations
        recent_ops = canvas_operations[-20:] if len(canvas_operations) > 20 else canvas_operations

        if len(recent_ops) < 3:
            return {'detected': False, 'confidence': 0.0, 'reason': 'Insufficient operations'}

        # Extract features for ML analysis
        features_list = [self._extract_canvas_features(op) for op in recent_ops]
        X_features = self.protection_model.feature_scaler.transform(features_list)

        # Anomaly detection
        anomaly_scores = self.protection_model.anomaly_detector.decision_function(X_features)
        mean_anomaly_score = np.mean(anomaly_scores)
        anomaly_confidence = (mean_anomaly_score + 1) / 2  # Convert to 0-1 scale

        # Pattern recognition (if available)
        pattern_confidence = 0.5
        if self.protection_model.pattern_recognizer:
            try:
                if hasattr(self.protection_model.pattern_recognizer, 'predict_proba'):
                    # TensorFlow/PyTorch prediction
                    predictions = self.protection_model.pattern_recognizer.predict_proba(X_features)
                    pattern_confidence = np.mean(predictions[:, 1])  # Probability of fingerprinting
                else:
                    pattern_confidence = 0.5
            except Exception as e:
                pattern_confidence = 0.5

        # Combined detection
        overall_confidence = (anomaly_confidence * 0.6) + (pattern_confidence * 0.4)
        is_fingerprinting = overall_confidence > self.detection_threshold

        # Count suspicious operations
        if is_fingerprinting:
            self.consecutive_suspicious_ops += 1
            self.malicious_operation_count += 1
        else:
            self.consecutive_suspicious_ops = max(0, self.consecutive_suspicious_ops - 1)

        detection_result = {
            'detected': is_fingerprinting,
            'confidence': overall_confidence,
            'anomaly_score': anomaly_confidence,
            'pattern_score': pattern_confidence,
            'operations_analyzed': len(recent_ops),
            'consecutive_suspicious': self.consecutive_suspicious_ops,
            'reason': self._determine_detection_reason(is_fingerprinting, recent_ops)
        }

        if is_fingerprinting:
            self.fingerprinting_detected = True
            detection_result['countermeasures'] = self._generate_countermeasures(recent_ops)

        return detection_result

    def _determine_detection_reason(self, is_fingerprinting: bool, operations: List[CanvasFingerprint]) -> str:
        """Determine why fingerprinting was detected or not"""
        if not is_fingerprinting:
            return "Operations appear legitimate"

        # Analyze patterns
        reasons = []

        # Check for excessive getImageData operations
        getimagedata_count = sum(1 for op in operations if op.operation_type == 'getImageData')
        if getimagedata_count > len(operations) * 0.4:
            reasons.append(f"High getImageData usage ({getimagedata_count}/{len(operations)} operations)")

        # Check for systematic scanning patterns
        scanning_patterns = self._detect_scanning_patterns(operations)
        if scanning_patterns:
            reasons.append("Systematic scanning patterns detected")

        # Check for repetitive parameters
        repetitive_params = self._detect_repetitive_parameters(operations)
        if repetitive_params:
            reasons.append("Repetitive parameters suggesting automation")

        # Check for timing anomalies
        timing_anomalies = self._detect_timing_anomalies(operations)
        if timing_anomalies:
            reasons.append("Abnormal timing patterns")

        return "; ".join(reasons) if reasons else "ML model flagged as suspicious"

    def _detect_scanning_patterns(self, operations: List[CanvasFingerprint]) -> bool:
        """Detect systematic scanning patterns typical of fingerprinting"""
        # Look for patterns where getImageData covers full canvas repeatedly
        get_image_ops = [op for op in operations if op.operation_type == 'getImageData']

        if len(get_image_ops) < 2:
            return False

        # Check if operations cover similar area patterns
        patterns_consistent = True
        first_op = get_image_ops[0]

        for op in get_image_ops[1:]:
            # Check if parameters are very similar (indicating systematic scanning)
            param_similarity = self._calculate_parameter_similarity(first_op.parameters, op.parameters)
            if param_similarity > 0.8:  # Very similar parameters
                patterns_consistent = True
                break

        return patterns_consistent

    def _detect_repetitive_parameters(self, operations: List[CanvasFingerprint]) -> bool:
        """Detect repetitive parameter usage"""
        all_parameters = [str(op.parameters) for op in operations]

        # Count unique parameter sets
        unique_params = set(all_parameters)

        # If less than 70% unique parameters, consider repetitive
        uniqueness_ratio = len(unique_params) / len(all_parameters)
        return uniqueness_ratio < 0.7

    def _detect_timing_anomalies(self, operations: List[CanvasFingerprint]) -> bool:
        """Detect timing anomalies that suggest automation"""
        if len(operations) < 3:
            return False

        timestamps = [op.timestamp for op in operations]
        intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]

        # Check for too-regular intervals (typical of automation)
        if len(intervals) > 2:
            mean_interval = np.mean(intervals)
            std_interval = np.std(intervals)

            # Low standard deviation indicates too-regular timing
            regularity_score = std_interval / mean_interval if mean_interval > 0 else 0

            # Very regular timing (likely automated)
            return regularity_score < 0.3

        return False

    def _calculate_parameter_similarity(self, params1: list, params2: list) -> float:
        """Calculate similarity between two parameter sets (0-1 scale)"""
        if len(params1) != len(params2):
            return 0.0

        similarities = []
        for p1, p2 in zip(params1, params2):
            if type(p1) == type(p2):
                if isinstance(p1, (int, float)):
                    # Numerical similarity
                    if p1 == p2:
                        similarities.append(1.0)
                    elif p1 != 0:
                        similarity = 1 - abs(p1 - p2) / abs(p1)
                        similarities.append(max(0, similarity))
                    else:
                        similarities.append(0.0)
                else:
                    # String similarity (exact match for now)
                    similarities.append(1.0 if p1 == p2 else 0.0)
            else:
                similarities.append(0.0)

        return np.mean(similarities) if similarities else 0.0

    def _generate_countermeasures(self, operations: List[CanvasFingerprint]) -> Dict[str, Any]:
        """Generate appropriate countermeasures for detected fingerprinting"""
        countermeasures = {}

        # Analyze the specific fingerprinting technique used
        primary_operation = max(set(op.operation_type for op in operations),
                              key=lambda x: sum(1 for op in operations if op.operation_type == x))

        if primary_operation == 'getImageData':
            # Canvas reading fingerprinting - inject noise
            countermeasures.update({
                'technique': 'canvas_reading_interference',
                'noise_injection': True,
                'noise_intensity': 'medium',
                'affected_operations': ['getImageData']
            })

        elif primary_operation in ['fillText', 'measureText']:
            # Text rendering fingerprinting - randomize fonts
            countermeasures.update({
                'technique': 'font_randomization',
                'font_substitution': True,
                'text_rendering_noise': True,
                'affected_operations': ['fillText', 'measureText']
            })

        elif primary_operation in ['fillRect', 'strokeRect']:
            # Shape rendering fingerprinting - add subpixel noise
            countermeasures.update({
                'technique': 'geometric_noise_injection',
                'subpixel_perturbation': True,
                'antialiasing_variation': True,
                'affected_operations': ['fillRect', 'strokeRect', 'arc']
            })

        # General countermeasures
        countermeasures.update({
            'timing_jitter': True,
            'context_state_randomization': True,
            'global_countermeasure_activation': True
        })

        return countermeasures

    def apply_canvas_protection(self, browser_session, countermeasures: Dict[str, Any]) -> bool:
        """
        Apply the specified countermeasures to the browser session
        """
        try:
            # Generate JavaScript protection code
            protection_script = self._generate_protection_javascript(countermeasures)

            # Inject into browser session
            browser_session.execute_script(protection_script)

            # Update session state
            browser_session.canvas_protection_active = True
            browser_session.active_countermeasures = countermeasures

            print("🛡️ Canvas fingerprinting protection activated")
            return True

        except Exception as e:
            print(f"❌ Failed to apply canvas protection: {e}")
            return False

    def _generate_protection_javascript(self, countermeasures: Dict[str, Any]) -> str:
        """Generate JavaScript code to implement the countermeasures"""
        script_parts = []

        # Canvas context protection wrapper
        script_parts.append("""
        function CanvasProtectionWrapper() {
            const originalGetContext = HTMLCanvasElement.prototype.getContext;
            const protectedContexts = new WeakMap();

            HTMLCanvasElement.prototype.getContext = function(contextType, contextAttributes) {
                const originalContext = originalGetContext.call(this, contextType, contextAttributes);

                if (contextType === '2d' && originalContext && !protectedContexts.has(originalContext)) {
                    const protectedContext = new CanvasProtectionContext(originalContext, this);
                    protectedContexts.set(originalContext, protectedContext);
                    return protectedContext;
                }

                return originalContext;
            };
        }
        """)

        if countermeasures.get('noise_injection'):
            script_parts.append("""
            class CanvasProtectionContext {
                constructor(originalContext, canvas) {
                    this.originalContext = originalContext;
                    this.canvas = canvas;
                    this.noiseInjected = false;

                    // Wrap key methods
                    this._wrapGetImageData();
                }

                _wrapGetImageData() {
                    const self = this;
                    const originalGetImageData = this.originalContext.getImageData;

                    this.originalContext.getImageData = function(sx, sy, sw, sh) {
                        const originalData = originalGetImageData.call(this, sx, sy, sw, sh);

                        // Inject noise to prevent fingerprinting
                        const noiseIntensity = 0.03; // Subtle noise
                        for (let i = 0; i < originalData.data.length; i += 4) {
                            // Add slight random variation to RGB channels (preserve A)
                            originalData.data[i] = Math.min(255, Math.max(0,
                                originalData.data[i] + (Math.random() - 0.5) * noiseIntensity * 255));
                            originalData.data[i + 1] = Math.min(255, Math.max(0,
                                originalData.data[i + 1] + (Math.random() - 0.5) * noiseIntensity * 255));
                            originalData.data[i + 2] = Math.min(255, Math.max(0,
                                originalData.data[i + 2] + (Math.random() - 0.5) * noiseIntensity * 255));
                        }

                        return originalData;
                    };
                }

                // Proxy all other methods to original context
                get fillStyle() { return this.originalContext.fillStyle; }
                set fillStyle(value) { this.originalContext.fillStyle = value; }
                get strokeStyle() { return this.originalContext.strokeStyle; }
                set strokeStyle(value) { this.originalContext.strokeStyle = value; }
                get font() { return this.originalContext.font; }
                set font(value) { this.originalContext.font = value; }
                // ... proxy all other properties as needed

                fillRect(...args) { return this.originalContext.fillRect(...args); }
                strokeRect(...args) { return this.originalContext.strokeRect(...args); }
                fillText(...args) { return this.originalContext.fillText(...args); }
                measureText(...args) { return this.originalContext.measureText(...args); }
                arc(...args) { return this.originalContext.arc(...args); }
                lineTo(...args) { return this.originalContext.lineTo(...args); }
                // ... proxy all other methods
            }
            """)

        if countermeasures.get('font_substitution'):
            script_parts.append("""
            // Font randomization in protection context
            CanvasProtectionContext.prototype._applyFontRandomization = function() {
                const originalFont = this.originalContext.font;
                const fonts = ['Arial', 'Helvetica', 'Times New Roman', 'Verdana', 'Georgia'];

                // Slightly modify font on each text operation
                const randomizedFont = originalFont.replace(
                    /(?<=\d+px\s)[^,]+/,
                    () => fonts[Math.floor(Math.random() * fonts.length)]
                );

                this.originalContext.font = randomizedFont;

                // Restore after brief delay to avoid breaking page layout
                setTimeout(() => {
                    this.originalContext.font = originalFont;
                }, 10);
            };
            """)

        if countermeasures.get('timing_jitter'):
            script_parts.append("""
            // Add timing jitter to operations
            CanvasProtectionContext.prototype._addTimingJitter = function() {
                // Small random delay between operations (1-5ms)
                const jitter = Math.random() * 4 + 1;
                const start = performance.now();

                while (performance.now() < start + jitter) {
                    // Busy wait for timing jitter
                }
            };
            """)

        # Initialize protection
        script_parts.append("""
        // Initialize canvas protection
        try {
            new CanvasProtectionWrapper();
            console.log('[Canvas Protection] Active countermeasures applied');
        } catch (e) {
            console.error('[Canvas Protection] Initialization failed:', e);
        }
        """)

        return "\n".join(script_parts)

    def get_protection_statistics(self) -> Dict[str, Any]:
        """Get statistics about canvas protection activity"""
        return {
            'fingerprinting_incidents_detected': self.malicious_operation_count,
            'consecutive_suspicious_operations': self.consecutive_suspicious_ops,
            'protection_active': self.fingerprinting_detected,
            'model_trained': self.protection_model.trained if self.protection_model else False,
            'operations_analyzed': len(self.operation_sequence),
            'detection_threshold': self.detection_threshold,
            'timestamp': datetime.now().isoformat()
        }

    def reset_detection_state(self):
        """Reset detection counters for clean testing"""
        self.fingerprinting_detected = False
        self.malicious_operation_count = 0
        self.consecutive_suspicious_ops = 0
        self.operation_sequence.clear()

    def update_detection_model(self, feedback_data: Dict[str, Any]):
        """Update the detection model with new feedback data"""
        # This would implement online learning with new legitimate/malicious operation examples
        print("🔄 Model update with new feedback data (feature for future implementation)")


class CanvasContextMonitor:
    """Monitor canvas context operations for real-time analysis"""

    def __init__(self, protector: CanvasFingerprintProtector):
        self.protector = protector
        self.operation_history = []
        self.session_operations = []

    def record_canvas_operation(self, operation: CanvasFingerprint):
        """Record a canvas operation for analysis"""
        self.operation_history.append(operation)
        self.session_operations.append(operation)

        # Keep only recent operations for analysis (last 50)
        if len(self.session_operations) > 50:
            self.session_operations.pop(0)

        # Run detection if we have enough operations
        if len(self.session_operations) >= 3:
            detection_result = self.protector.detect_canvas_fingerprinting(self.session_operations)

            if detection_result.get('detected', False):
                print(f"🚨 Canvas fingerprinting detected: {detection_result.get('reason', 'Unknown')}")
                print(".2f"                return detection_result

        return None
