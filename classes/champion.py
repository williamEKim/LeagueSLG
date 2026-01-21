from typing import List
from classes.skill import Skill
from classes.buff import Buff

class Champion:
    """
    챔피언 클래스: 능력치 관리, 스킬 시전, 버프 효과 적용 등 담당
    """
    def __init__(
            self, 
            name: str = '',
            base_stat: List[int] = [],
            stat_growth: List[float] = [],
            level: int = 1,
            minions: tuple[str, int] = ('', 0),
            skills: List[Skill] = [] 
    ):
        self.name: str = name
        # 능력치 순서: [HP, ATK, DEF, SPATK, SPDEF, SPD]
        self.base_stat = base_stat or [0, 0, 0, 0, 0, 0]
        self.stat_growth = stat_growth or [0, 0, 0, 0, 0, 0]
        self.level = level
        self.minion_type, self.minion_count = minions
        self.skills = skills or []
        self.buffs: list[Buff] = []

        # 초기 능력치 계산
        self.recalculate_stats()

        # 현재 체력 설정 (기본 스탯의 HP 기준)
        self.max_hp = base_stat[0]
        self.current_hp = self.max_hp

    def reset_status(self):
        """
        챔피언의 상태를 초기화 (HP 풀회복 및 모든 버프 제거)
        """
        self.current_hp = self.max_hp
        self.buffs = []
        self.recalculate_stats()

    def calculate_stats(self, base_stat, stat_growth, level):
        """
        레벨에 따른 기본 능력치 계산 (공식: 베이스 + 성장치 * (레벨-1))
        """
        lv = level - 1
        return [
            int(base_stat[i] + stat_growth[i] * lv)
            for i in range(len(base_stat))
        ]

    def apply_buffs(self, stats, buffs):
        """
        현재 챔피언에게 걸린 버프들을 순회하며 최종 능력치에 반영
        """
        result = stats.copy()
        for buff in buffs:
            if buff.is_expired():
                continue
            result = buff.apply_stats(result)
        return result
    
    def recalculate_stats(self):
        """
        레벨업이나 버프 변경 시 호출되어 현재 능력치(self.stat)를 갱신
        """
        before_buff = self.calculate_stats(
            self.base_stat,
            self.stat_growth,
            self.level
        )
        final = self.apply_buffs(before_buff, self.buffs)
        
        # 가독성을 위해 사전(dict) 형태로 저장
        self.stat = {
            "HP": final[0],
            "ATK": final[1],
            "DEF": final[2],
            "SPATK": final[3],
            "SPDEF": final[4],
            "SPD": final[5],
        }

    def roll_skills(self) -> Skill:
        """
        챔피언의 스킬들을 확률에 따라 체크하고, 발동된 스킬을 반환
        """
        for skill in self.skills:
            if not skill.can_use(self):
                continue
            if skill.roll(self):
                return skill
        return None

    def take_damage(self, amount: float):
        """
        데미지를 입고 현재 체력을 감소시킴
        """
        self.current_hp = max(0, self.current_hp - amount)
        return self.current_hp

    def getName(self) -> str:
        return self.name

    def getMinion(self) -> tuple:
        return (self.minion_type, self.minion_count) 
    
    def getStat(self, name: str) -> float:
        """
        특정 능력치 이름을 입력받아 현재 값을 반환 (예: 'ATK', 'SPD')
        """
        return self.stat[name.upper()]
    
    def getCurrHealth(self) -> float:
        return self.current_hp

    def addBuff(self, buff_id: str, duration: int, value: float | None = None):
        """
        새로운 버프를 추가 (duration은 턴 단위 정수)
        """
        self.buffs.append(Buff(buff_id, duration, value))
        self.recalculate_stats() # 능력치를 즉시 반영

    def removeBuff(self, buff_id: str):
        """
        특정 ID의 버프를 즉시 제거
        """
        self.buffs = [
            b for b in self.buffs
            if b.buff_id != buff_id
        ]
        self.recalculate_stats()
    
    def is_silenced(self) -> bool:
        """침묵 상태 여부 확인 (스킬 사용 불가)"""
        return any(buff.buff_id == "silence" for buff in self.buffs)
    
    def is_stunned(self) -> bool:
        """기절 상태 여부 확인 (행동 불가)"""
        return any(buff.buff_id == "stun" for buff in self.buffs)

    def is_slowed(self) -> bool:
        """둔화 상태 여부 확인 (이동 속도 감소)"""
        return any(buff.buff_id == "slow" for buff in self.buffs)
    
    def is_alive(self) -> bool:
        """생존 여부 확인"""
        return self.current_hp > 0

    def update(self):
        """만료된 버프를 제거하고 능력치를 재계산"""
        self.buffs = [buff for buff in self.buffs if not buff.is_expired()]
        self.recalculate_stats()

    def on_turn_start(self):
        """턴이 시작될 때 호출 (버프 갱신 등)"""
        self.update()

    def on_turn_end(self):
        """턴이 종료될 때 호출. 버프의 지속 턴수를 감소시킴"""
        for buff in self.buffs:
            buff.tick()
        self.update()