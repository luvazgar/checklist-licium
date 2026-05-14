from app.core.services import exposed_action
from app.core.base import BaseService
from sqlalchemy import func


class UserServiceOverride(BaseService):
    """Override of core.services.user.UserService to add checklist statistics."""

    @exposed_action("read", groups=["practice_checklist_group_manager", "core_group_superadmin"])
    def get_checklist_stats(self, user_id: int) -> dict:
        """
        Get checklist statistics for a specific user.

        Args:
            user_id: The ID of the user to get stats for

        Returns:
            dict with:
                - total_checklists: Total checklists owned by the user
                - open_checklists: Open checklists owned by the user
                - closed_checklists: Closed checklists owned by the user
                - total_items: Total items assigned to the user
                - completed_items: Completed items assigned to the user
                - pending_items: Pending items assigned to the user
        """
        from ..models import PracticeChecklist, PracticeChecklistItem

        # Query checklists owned by user
        total_checklists = self.repo.session.query(func.count(PracticeChecklist.id)).filter(
            PracticeChecklist.owner_id == user_id
        ).scalar() or 0

        open_checklists = self.repo.session.query(func.count(PracticeChecklist.id)).filter(
            PracticeChecklist.owner_id == user_id,
            PracticeChecklist.status == "open"
        ).scalar() or 0

        closed_checklists = self.repo.session.query(func.count(PracticeChecklist.id)).filter(
            PracticeChecklist.owner_id == user_id,
            PracticeChecklist.status == "closed"
        ).scalar() or 0

        # Query items assigned to user
        total_items = self.repo.session.query(func.count(PracticeChecklistItem.id)).filter(
            PracticeChecklistItem.assigned_user_id == user_id
        ).scalar() or 0

        completed_items = self.repo.session.query(func.count(PracticeChecklistItem.id)).filter(
            PracticeChecklistItem.assigned_user_id == user_id,
            PracticeChecklistItem.is_done == True
        ).scalar() or 0

        pending_items = total_items - completed_items

        return {
            "total_checklists": total_checklists,
            "open_checklists": open_checklists,
            "closed_checklists": closed_checklists,
            "total_items": total_items,
            "completed_items": completed_items,
            "pending_items": pending_items,
        }
