from typing import List
from classes.champion import Champion
from classes.skill import Skill


class Battle:
    def __init__(self, left: Champion, right: Champion):
        self.left = left
        self.right = right
        self.turn = 1

    def start(self):
        self._log(f"Battle Start: {self.left.name} vs {self.right.name}")

        while self._both_alive():
            self._log(f"\n[ Turn {self.turn} ]")

            self._process_turn(self.left, self.right)
            if not self.right.is_alive():
                break

            self._process_turn(self.right, self.left)
            self.turn += 1

        self._finish()

    def _both_alive(self) -> bool:
        return self.left.is_alive() and self.right.is_alive()

    def _process_turn(self, actor: Champion, target: Champion):
        self._log(f"{actor.name}'s turn")

        actor.on_turn_start()
        if not actor.is_alive():
            return

        skill = actor.roll_skills()
        if skill:
            self._use_skill(actor, target, skill)

        self._basic_attack(actor, target)

        actor.on_turn_end()
        target.on_turn_end()

    def _use_skill(self, attacker: Champion, defender: Champion, skill: Skill):
        self._log(f"{attacker.name} uses {skill.name}!")
        skill.cast(self, attacker, defender)
        self._log(f"(HP: {defender.current_hp})")

    def _basic_attack(self, attacker: Champion, defender: Champion):
        damage = max(0, attacker.getStat('ATK') - defender.getStat('DEF'))
        defender.take_damage(damage)

        self._log(
            f"{attacker.name} attacks {defender.name} "
            f"→ {damage} damage "
            f"(HP: {defender.current_hp})"
        )

        

    def _finish(self):
        winner = self.left if self.left.is_alive() else self.right
        self._log(f"\nWinner: {winner.name}")

    def _log(self, msg: str):
        print(msg)
