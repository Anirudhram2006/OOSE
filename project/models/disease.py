"""Disease, remedies, chatbot, and logging models."""
from app import db


class Disease(db.Model):
    __tablename__ = "diseases"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    remedies = db.Column(db.Text, nullable=False)
    precautions = db.Column(db.Text, nullable=False)
    doctor_advice = db.Column(db.Text, nullable=False)
    validated = db.Column(db.Boolean, default=False, nullable=False)

    remedy_entries = db.relationship(
        "Remedy", back_populates="disease", lazy=True, cascade="all, delete-orphan"
    )


class Remedy(db.Model):
    __tablename__ = "remedies"

    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey("diseases.id"), nullable=False)
    remedy_name = db.Column(db.String(150), nullable=False)
    details = db.Column(db.Text, nullable=False)
    reference_url = db.Column(db.String(255), nullable=True)

    disease = db.relationship("Disease", back_populates="remedy_entries")


class ChatbotKnowledge(db.Model):
    __tablename__ = "chatbot_knowledge"

    id = db.Column(db.Integer, primary_key=True)
    question_pattern = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)


class AnalysisLog(db.Model):
    __tablename__ = "analysis_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    symptoms = db.Column(db.Text, nullable=True)
    predicted_disease = db.Column(db.String(120), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", back_populates="analysis_logs")


class DiseaseUpdateRequest(db.Model):
    __tablename__ = "disease_update_requests"

    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey("diseases.id"), nullable=False)
    expert_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    update_notes = db.Column(db.Text, nullable=False)
    reference = db.Column(db.String(255), nullable=True)
    approved = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
