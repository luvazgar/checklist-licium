from __future__ import annotations
import datetime as dt
from fastapi import HTTPException
from app.core.base import BaseService
from app.core.serializer import serialize
from app.core.services import exposed_action
from ..models.feedback import Comment, Suggestion, Tag


class SuggestionService(BaseService):
    from ..models.feedback import Suggestion


    @exposed_action("write", groups=["feedback_group_moderator", "core_group_superadmin"])
    def publish(self, id: int, note: str | None = None, pin: bool = False):
        suggestion = self.repo.session.get(Suggestion, id)
        if not suggestion:
            raise HTTPException(404, "Sugerencia no encontrada")

        if suggestion.status == "publicada":
            raise HTTPException(400, "Ya publicada")

        suggestion.status = "publicada"
        suggestion.published_at = dt.datetime.now(dt.timezone.utc)
        suggestion.moderation_note = note

        self.repo.session.commit()
        return serialize(suggestion)



    @exposed_action("write", groups=["feedback_group_moderator", "core_group_superadmin"])
    def reject(self, id: int, note: str):
        suggestion = self.repo.session.get(Suggestion, id)
        if not suggestion:
            raise HTTPException(404, "Sugerencia no encontrada")

        suggestion.status = "rechazada"
        suggestion.moderation_note = note
        self.repo.session.commit()
        return serialize(suggestion)



    @exposed_action("write", groups=["feedback_group_moderator", "core_group_superadmin"])
    def merge(self, id: int, target_id: int, note: str | None = None):
        suggestion = self.repo.session.get(Suggestion, id)
        target = self.repo.session.get(Suggestion, target_id)

        if not suggestion or not target:
            raise HTTPException(404, "Sugerencia no encontrada")

        suggestion.status = "merged"
        suggestion.moderation_note = note
        self.repo.session.commit()
        return serialize(suggestion)



    @exposed_action("write", groups=["feedback_group_moderator", "core_group_superadmin"])
    def reopen(self, id: int):
        suggestion = self.repo.session.get(Suggestion, id)
        if not suggestion:
            raise HTTPException(404, "Sugerencia no encontrada")

        suggestion.status = "pendiente"
        self.repo.session.commit()
        return serialize(suggestion)



    @exposed_action("write", groups=["feedback_group_moderator", "core_group_superadmin"])
    def vote(self, suggestion_id: int, user_id: str):
        suggestion = self.repo.session.get(Suggestion, suggestion_id)
        if not suggestion:
            raise HTTPException(status_code=404)
        suggestion.votes_count += 1
        self.repo.session.commit()
        return serialize(suggestion)



    @exposed_action("read", groups=["feedback_group_moderator", "core_group_superadmin"])
    def get_moderation_queue(self, status: str = "pendiente"):
        return self.repo.session.query(Suggestion).filter(Suggestion.status == status).all()


class CommentService(BaseService):
    from ..models.feedback import Comment



    @exposed_action("write", groups=["feedback_group_moderator", "core_group_superadmin"])
    def publish_comment(self, id: int, note: str | None = None):
        comment = self.repo.session.get(Comment, id)
        if not comment:
            raise HTTPException(404, "Comentario no encontrado")

        comment.status = "publicada"
        comment.published_at = dt.datetime.now(dt.timezone.utc)
        comment.moderation_note = note
        self.repo.session.commit()
        return serialize(comment)



    @exposed_action("write", groups=["feedback_group_moderator", "core_group_superadmin"])
    def reject_comment(self, id: int, note: str):
        comment = self.repo.session.get(Comment, id)
        if not comment:
            raise HTTPException(404, "Commentario no encontrado")

        comment.status = "rechazada"
        comment.moderation_note = note
        self.repo.session.commit()
        return serialize(comment)


class TagService(BaseService):
    from ..models.feedback import Tag