"""Admin and Medical Expert route handlers."""
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from models.disease import AnalysisLog, Disease, DiseaseUpdateRequest
from models.user import User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(*roles):
                flash("Unauthorized", "danger")
                return redirect(url_for("analysis.dashboard"))
            return func(*args, **kwargs)

        return wrapped

    return decorator


@admin_bp.route("/dashboard")
@login_required
@roles_required("admin")
def admin_dashboard():
    users = User.query.order_by(User.created_at.desc()).all()
    diseases = Disease.query.order_by(Disease.name.asc()).all()
    logs = AnalysisLog.query.order_by(AnalysisLog.created_at.desc()).limit(20).all()
    return render_template("admin_dashboard.html", users=users, diseases=diseases, logs=logs)


@admin_bp.route("/user/<int:user_id>/toggle", methods=["POST"])
@login_required
@roles_required("admin")
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot disable yourself.", "warning")
        return redirect(url_for("admin.admin_dashboard"))

    user.is_active_user = not user.is_active_user
    db.session.commit()
    flash("User status updated.", "success")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/user/<int:user_id>/delete", methods=["POST"])
@login_required
@roles_required("admin")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete yourself.", "warning")
        return redirect(url_for("admin.admin_dashboard"))

    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", "success")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/disease/save", methods=["POST"])
@login_required
@roles_required("admin")
def save_disease():
    disease_id = request.form.get("disease_id")
    disease = Disease.query.get(disease_id) if disease_id else Disease()

    disease.name = request.form.get("name", "").strip()
    disease.category = request.form.get("category", "").strip()
    disease.description = request.form.get("description", "").strip()
    disease.remedies = request.form.get("remedies", "").strip()
    disease.precautions = request.form.get("precautions", "").strip()
    disease.doctor_advice = request.form.get("doctor_advice", "").strip()

    if not disease_id:
        db.session.add(disease)

    db.session.commit()
    flash("Disease record saved.", "success")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/disease/<int:disease_id>/delete", methods=["POST"])
@login_required
@roles_required("admin")
def delete_disease(disease_id):
    disease = Disease.query.get_or_404(disease_id)
    db.session.delete(disease)
    db.session.commit()
    flash("Disease deleted.", "success")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/expert")
@login_required
@roles_required("medical_expert")
def expert_dashboard():
    diseases = Disease.query.order_by(Disease.name.asc()).all()
    requests = (
        DiseaseUpdateRequest.query.order_by(DiseaseUpdateRequest.created_at.desc()).limit(20).all()
    )
    return render_template("expert_dashboard.html", diseases=diseases, requests=requests)


@admin_bp.route("/expert/request", methods=["POST"])
@login_required
@roles_required("medical_expert")
def submit_expert_update():
    req = DiseaseUpdateRequest(
        disease_id=request.form.get("disease_id"),
        expert_id=current_user.id,
        update_notes=request.form.get("update_notes", "").strip(),
        reference=request.form.get("reference", "").strip(),
    )
    db.session.add(req)
    db.session.commit()
    flash("Update submitted for admin review.", "success")
    return redirect(url_for("admin.expert_dashboard"))


@admin_bp.route("/expert/approve/<int:request_id>", methods=["POST"])
@login_required
@roles_required("admin")
def approve_request(request_id):
    req = DiseaseUpdateRequest.query.get_or_404(request_id)
    req.approved = True
    disease = Disease.query.get(req.disease_id)
    if disease:
        disease.description = f"{disease.description}\n\nExpert update: {req.update_notes}"
        disease.validated = True

    db.session.commit()
    flash("Expert update approved.", "success")
    return redirect(url_for("admin.admin_dashboard"))
