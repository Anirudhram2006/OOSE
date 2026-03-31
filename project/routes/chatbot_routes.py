"""Chatbot UI and API routes."""
from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required

from forms import ChatForm
from services.chatbot_engine import ChatbotEngine

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")


@chatbot_bp.route("/", methods=["GET", "POST"])
@login_required
def chatbot_page():
    form = ChatForm()
    response = None
    if form.validate_on_submit():
        response = ChatbotEngine.get_response(form.query.data)

    return render_template("chatbot.html", form=form, response=response)


@chatbot_bp.route("/ask", methods=["POST"])
@login_required
def ask_chatbot():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "")
    response = ChatbotEngine.get_response(query)
    return jsonify({"response": response})
