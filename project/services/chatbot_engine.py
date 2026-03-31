"""Database-backed chatbot response engine."""
from models.disease import ChatbotKnowledge, Disease


class ChatbotEngine:
    """Searches knowledge base and disease table for helpful responses."""

    @staticmethod
    def get_response(query: str) -> str:
        q = query.lower().strip()

        kb_match = (
            ChatbotKnowledge.query.filter(ChatbotKnowledge.question_pattern.ilike(f"%{q}%")).first()
            or ChatbotKnowledge.query.filter(
                ChatbotKnowledge.question_pattern.ilike(f"%{q.split(' ')[0]}%")
            ).first()
        )
        if kb_match:
            return kb_match.answer

        disease = Disease.query.filter(Disease.name.ilike(f"%{q}%")).first()
        if disease:
            return (
                f"{disease.name} is categorized as {disease.category}. "
                f"Precautions: {disease.precautions}. "
                f"Doctor advice: {disease.doctor_advice}"
            )

        return (
            "I could not find an exact answer. Please consult a medical expert for "
            "personalized guidance, especially if symptoms worsen."
        )
