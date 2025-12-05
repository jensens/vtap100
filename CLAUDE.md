Erste Directive:

- IMMER TDD! Erst tests schreiben oder updaten, dann den Applikationscode.
- gute UX und Doku sind Pflicht
- folge dem DRY Prinzip
- verwende früh WebSearch, z.B wenn Du zu wenig oder alte Info hast oder bei einem Problem nicht weiterkommst

SCM:
- arbeite immer auf einem Git Worktree unter ./worktrees (git-ignored, Ordner anlegen falls es fehlt), so koennen Agents parallel arbeiten.
- committe nach jedem erfolgreichen Task
- worktree aufraeumen, wenn task komplett.
- push erfolgt durch den User, es sei denn er fragt explizit danach

Sprache:
- der Software ist Englisch und Deutsch, alle TUI Texte und Hilfen werden übersetzt.
- die Doku ist english
- Prompts und Pläne können gerne Deutsch sein.

Pläne:
- immer auch unter ./docs ablegen, immer PLAN_[THEMA].md

Dokumentation ist auch unter ./docs abzulegen. Ausgenommen davon sind Hilfetexte fùr das Programm.
