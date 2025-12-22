"""
Face Recognition System for SaarthiAI
Handles face detection, encoding, and recognition for attendance
"""

import cv2
import numpy as np
import pickle
import os
from datetime import datetime

# Face detection cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Model paths
MODEL_DIR = 'face_recognition/models'
FACE_DATA_FILE = os.path.join(MODEL_DIR, 'face_data.pkl')

def ensure_model_dir():
    """Ensure model directory exists"""
    os.makedirs(MODEL_DIR, exist_ok=True)

def load_face_data():
    """Load saved face encodings"""
    ensure_model_dir()
    if os.path.exists(FACE_DATA_FILE):
        try:
            with open(FACE_DATA_FILE, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading face data: {e}")
            return {}
    return {}

def save_face_data(face_data):
    """Save face encodings to file"""
    ensure_model_dir()
    try:
        with open(FACE_DATA_FILE, 'wb') as f:
            pickle.dump(face_data, f)
        return True
    except Exception as e:
        print(f"Error saving face data: {e}")
        return False

def detect_face(image):
    """
    Detect face in image
    Returns: (x, y, w, h) of face or None
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        return None
    elif len(faces) > 1:
        # If multiple faces, return the largest one
        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
    
    return faces[0]

def extract_face_features(image, face_coords):
    """
    Extract face features (simple histogram-based approach)
    For production, consider using face_recognition library or dlib
    """
    x, y, w, h = face_coords
    face_roi = image[y:y+h, x:x+w]
    
    # Resize to standard size
    face_roi = cv2.resize(face_roi, (100, 100))
    
    # Convert to grayscale
    gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    
    # Apply histogram equalization
    gray_face = cv2.equalizeHist(gray_face)
    
    # Flatten to 1D array (this is our "encoding")
    encoding = gray_face.flatten()
    
    return encoding

def train_recognizer(image, student_id):
    """
    Train/Register a new face
    
    Args:
        image: numpy array (BGR image from OpenCV)
        student_id: unique student identifier
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Detect face
    face_coords = detect_face(image)
    
    if face_coords is None:
        print("No face detected in image")
        return False
    
    # Extract features
    encoding = extract_face_features(image, face_coords)
    
    # Load existing data
    face_data = load_face_data()
    
    # Add or update student face data
    if student_id in face_data:
        # Average with existing encoding if student already registered
        existing_encoding = face_data[student_id]
        face_data[student_id] = (existing_encoding + encoding) / 2
    else:
        face_data[student_id] = encoding
    
    # Save updated data
    success = save_face_data(face_data)
    
    if success:
        print(f"✓ Face registered for student ID: {student_id}")
    else:
        print(f"✗ Failed to register face for student ID: {student_id}")
    
    return success

def calculate_similarity(encoding1, encoding2):
    """
    Calculate similarity between two encodings using normalized correlation
    Returns value between 0 and 1 (1 = identical)
    """
    # Normalize encodings
    norm1 = np.linalg.norm(encoding1)
    norm2 = np.linalg.norm(encoding2)
    
    if norm1 == 0 or norm2 == 0:
        return 0
    
    # Calculate normalized dot product
    similarity = np.dot(encoding1, encoding2) / (norm1 * norm2)
    
    # Convert to 0-1 range
    similarity = (similarity + 1) / 2
    
    return similarity

def recognize_face(image, threshold=0.7):
    """
    Recognize face in image
    
    Args:
        image: numpy array (BGR image from OpenCV)
        threshold: similarity threshold (0-1)
    
    Returns:
        student_id: ID of recognized student or None
    """
    # Detect face
    face_coords = detect_face(image)
    
    if face_coords is None:
        print("No face detected")
        return None
    
    # Extract features
    encoding = extract_face_features(image, face_coords)
    
    # Load face database
    face_data = load_face_data()
    
    if not face_data:
        print("No registered faces in database")
        return None
    
    # Find best match
    best_match_id = None
    best_similarity = 0
    
    for student_id, stored_encoding in face_data.items():
        similarity = calculate_similarity(encoding, stored_encoding)
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_id = student_id
    
    # Check if best match exceeds threshold
    if best_similarity >= threshold:
        print(f"✓ Recognized student ID: {best_match_id} (confidence: {best_similarity:.2%})")
        return best_match_id
    else:
        print(f"✗ No match found (best similarity: {best_similarity:.2%})")
        return None

def get_registered_students():
    """Get list of student IDs with registered faces"""
    face_data = load_face_data()
    return list(face_data.keys())

def delete_student_face(student_id):
    """Delete a student's registered face"""
    face_data = load_face_data()
    
    if student_id in face_data:
        del face_data[student_id]
        save_face_data(face_data)
        print(f"✓ Deleted face data for student ID: {student_id}")
        return True
    else:
        print(f"✗ No face data found for student ID: {student_id}")
        return False

def draw_face_box(image, face_coords, label=None, color=(0, 255, 0)):
    """Draw bounding box around detected face"""
    x, y, w, h = face_coords
    cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
    
    if label:
        cv2.putText(image, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    
    return image

# Test functions
def test_face_detection():
    """Test face detection with webcam"""
    print("Starting webcam for face detection test...")
    print("Press 'q' to quit")
    
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        face_coords = detect_face(frame)
        
        if face_coords is not None:
            frame = draw_face_box(frame, face_coords, "Face Detected")
        
        cv2.imshow('Face Detection Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("=" * 50)
    print("Face Recognition System - Test Mode")
    print("=" * 50)
    
    # Display registered students
    registered = get_registered_students()
    print(f"\nRegistered students: {len(registered)}")
    if registered:
        print("Student IDs:", registered)
    
    # Test face detection
    print("\nStarting face detection test...")
    print("Press 'q' to quit")
    try:
        test_face_detection()
    except Exception as e:
        print(f"Error: {e}")