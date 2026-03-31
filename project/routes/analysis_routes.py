"""Routes for upload/symptom analysis workflow."""
import os
from functools import wraps

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db
from forms import SymptomForm, UploadForm
from models.disease import AnalysisLog, Disease
from services.ai_analysis import SkinDiseaseAnalyzer
from services.classifier import classify_from_symptoms

analysis_bp = Blueprint("analysis", __name__, url_prefix="/analysis")
analyzer = SkinDiseaseAnalyzer()


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(*roles):
                flash("You do not have access to this page.", "danger")
                return redirect(url_for("analysis.dashboard"))
            return func(*args, **kwargs)

        return wrapped

    return decorator


@analysis_bp.route("/dashboard")
@login_required
def dashboard():
    recent_logs = (
        AnalysisLog.query.filter_by(user_id=current_user.id)
        .order_by(AnalysisLog.created_at.desc())
        .limit(5)
        .all()
    )

    if current_user.role == "admin":
        return redirect(url_for("admin.admin_dashboard"))
    if current_user.role == "medical_expert":
        return redirect(url_for("admin.expert_dashboard"))

    return render_template("dashboard.html", recent_logs=recent_logs)


@analysis_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
        ext = filename.rsplit(".", 1)[-1].lower()

        if ext not in current_app.config["ALLOWED_EXTENSIONS"]:
            flash("Unsupported file type.", "danger")
            return redirect(request.url)

        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        prediction, confidence, probabilities = analyzer.predict(save_path)
        disease = Disease.query.filter(Disease.name.ilike(prediction)).first()

        if disease is None:
            disease = Disease.query.first()

        log = AnalysisLog(
            user_id=current_user.id,
            image_path=f"uploads/{filename}",
            predicted_disease=prediction,
            confidence=confidence,
        )
        db.session.add(log)
        db.session.commit()

        return render_template(
            "analysis_result.html",
            disease=disease,
            confidence=confidence,
            probabilities=probabilities,
            image_url=url_for("static", filename=f"uploads/{filename}"),
            source_type="image",
        )

    return render_template("upload.html", form=form)


@analysis_bp.route("/symptoms", methods=["GET", "POST"])
@login_required
def symptoms_input():
    form = SymptomForm()
    if form.validate_on_submit():
        symptom_text = form.symptoms.data
        prediction, confidence = classify_from_symptoms(symptom_text)
        disease = Disease.query.filter(Disease.name.ilike(prediction)).first()

        if disease is None:
            disease = Disease.query.first()

        log = AnalysisLog(
            user_id=current_user.id,
            symptoms=symptom_text,
            predicted_disease=prediction,
            confidence=confidence,
        )
        db.session.add(log)
        db.session.commit()

        return render_template(
            "analysis_result.html",
            disease=disease,
            confidence=confidence,
            probabilities={prediction: confidence},
            image_url=None,
            source_type="symptom",
        )

    return render_template("symptom_input.html", form=form)


@analysis_bp.route("/remedy/<int:disease_id>")
@login_required
def remedy_details(disease_id):
    disease = Disease.query.get_or_404(disease_id)
    return render_template("remedy_details.html", disease=disease)
