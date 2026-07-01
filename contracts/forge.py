# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""
FORGE - An AI-Greenlit Build Pipeline
=====================================
Pitch an idea with a reference spec. A validator set reads the spec and judges,
under the Equivalence Principle, whether it is a feasible and worthwhile thing to
build - returning a score and a verdict. Greenlit ideas advance; ideas that are
infeasible or hollow are shelved. A kanban board that triages itself.

Status: PITCHED(0) -> GREENLIT(1) | SHELVED(2)
"""

from genlayer import *
from dataclasses import dataclass
import json
import typing


PITCHED = 0
GREENLIT = 1
SHELVED = 2


@allow_storage
@dataclass
class Idea:
    author: Address
    title: str
    pitch: str
    spec_url: str
    status: u8
    score: u8
    rationale: str


class Forge(gl.Contract):
    ideas: DynArray[Idea]

    def __init__(self) -> None:
        pass

    @gl.public.write
    def pitch(self, title: str, pitch: str, spec_url: str) -> int:
        if len(title.strip()) == 0:
            raise gl.vm.UserError("a title is required")
        if len(pitch.strip()) == 0:
            raise gl.vm.UserError("a pitch is required")
        if len(spec_url.strip()) == 0:
            raise gl.vm.UserError("a spec URL is required")
        it = self.ideas.append_new_get()
        it.author = gl.message.sender_address
        it.title = title
        it.pitch = pitch
        it.spec_url = spec_url
        it.status = u8(PITCHED)
        it.score = u8(0)
        it.rationale = ""
        return len(self.ideas) - 1

    @gl.public.write
    def review(self, idea_id: int) -> None:
        """Read the spec; validators score feasibility/merit and move the card."""
        it = self._get(idea_id)
        if it.status != PITCHED:
            raise gl.vm.UserError("this idea has already been reviewed")

        title = it.title
        pitch = it.pitch
        url = it.spec_url

        def leader_fn() -> str:
            page = ""
            try:
                page = gl.nondet.web.get(url).body.decode("utf-8")[:6000]
            except Exception:
                page = "(spec page unreachable)"
            prompt = (
                f"You are a pragmatic technical reviewer triaging a build idea.\n"
                f"Title: {title}\n"
                f"Pitch: {pitch}\n\n"
                f"Reference spec:\n{page}\n\n"
                "Is this a feasible and worthwhile thing to build? Consider whether "
                "it is physically/technically possible and whether the spec supports "
                "it. Give an integer score from 0 to 100. Greenlight it only if it is "
                'genuinely feasible and worthwhile. Reply with ONLY JSON: '
                '{"greenlight": true|false, "score": <0-100>, "reason": "<one sentence>"}.'
            )
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leader_res) -> bool:
            if not isinstance(leader_res, gl.vm.Return):
                return False
            return self._decision_of(leader_res.calldata)[0] == self._decision_of(leader_fn())[0]

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        green, score, reason = self._decision_of(result)
        it.score = u8(max(0, min(100, score)))
        it.rationale = reason[:300]
        it.status = u8(GREENLIT) if green else u8(SHELVED)

    # ------------------------------------------------------------------ views
    @gl.public.view
    def get_idea_count(self) -> int:
        return len(self.ideas)

    @gl.public.view
    def get_stats(self) -> dict:
        pitched = 0
        green = 0
        shelved = 0
        for it in self.ideas:
            if it.status == GREENLIT:
                green += 1
            elif it.status == SHELVED:
                shelved += 1
            else:
                pitched += 1
        return {"total": len(self.ideas), "pitched": pitched, "greenlit": green, "shelved": shelved}

    @gl.public.view
    def get_idea(self, idea_id: int) -> dict:
        it = self._get(idea_id)
        return {
            "author": it.author.as_hex,
            "title": it.title,
            "pitch": it.pitch,
            "spec_url": it.spec_url,
            "status": int(it.status),
            "score": int(it.score),
            "rationale": it.rationale,
        }

    # -------------------------------------------------------------- internals
    def _get(self, idea_id: int) -> Idea:
        if idea_id < 0 or idea_id >= len(self.ideas):
            raise gl.vm.UserError("no such idea")
        return self.ideas[idea_id]

    def _decision_of(self, result: typing.Any) -> tuple:
        data = result
        if isinstance(data, str):
            data = self._extract_json(data)
        if not isinstance(data, dict):
            return (False, 0, "")
        reason = str(data.get("reason", ""))
        score = 0
        try:
            score = int(data.get("score", 0))
        except (ValueError, TypeError):
            score = 0
        raw = data.get("greenlight", None)
        green = False
        if isinstance(raw, bool):
            green = raw
        elif isinstance(raw, str):
            green = raw.strip().lower() == "true"
        return (green, score, reason)

    def _extract_json(self, text: str) -> typing.Any:
        try:
            return json.loads(text)
        except (ValueError, TypeError):
            pass
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except (ValueError, TypeError):
                return None
        return None
