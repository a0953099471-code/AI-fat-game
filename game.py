import time
from datetime import datetime
import pandas as pd

class Entity:
    def __init__(self, name, max_hp, attack, defense):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense

    def take_damage(self, amount):
        damage = max(0, amount - self.defense)
        self.hp = max(0, self.hp - damage)
        return damage

    def is_alive(self):
        return self.hp > 0

class Player(Entity):
    def __init__(self):
        super().__init__('Player', max_hp=100, attack=12, defense=6)
        self.bmi = 24.0
        self.calories = 0
        self.score = 0
        self.last_action = '等待動作'
        self.exercise_time = 0
        self.start_time = time.time()

    def attack_action(self, boss):
        self.last_action = '深蹲→攻擊'
        damage = boss.take_damage(self.attack)
        return damage

    def charge_action(self):
        self.last_action = '開合跳→集氣'
        self.attack += 2
        return 0

    def dodge_action(self):
        self.last_action = '抬腿→閃避'
        self.defense += 2
        return 0

    def block_action(self):
        self.last_action = '平板撐→防禦'
        self.defense += 3
        return 0

    def update_stats(self, calories, seconds):
        self.calories += calories
        self.exercise_time += seconds

    def to_dict(self):
        return {
            'hp': self.hp,
            'max_hp': self.max_hp,
            'bmi': round(self.bmi, 1),
            'calories': int(self.calories),
            'score': self.score,
            'last_action': self.last_action,
            'exercise_time': int(self.exercise_time),
        }

class Boss(Entity):
    def __init__(self, level=1):
        # 限制等級為 1~3 並針對每個等級指定較明確的血量/攻擊/防禦值
        level = max(1, min(level, 3))
        hp_map = {1: 30, 2: 60, 3: 100}
        attack_map = {1: 6, 2: 10, 3: 15}
        defense_map = {1: 1, 2: 3, 3: 5}
        hp = hp_map[level]
        attack = attack_map[level]
        defense = defense_map[level]
        super().__init__(f'Boss {level}', max_hp=hp, attack=attack, defense=defense)
        self.level = level

    def to_dict(self):
        return {'name': self.name, 'hp': self.hp, 'max_hp': self.max_hp, 'level': self.level}

class StatsRecorder:
    def __init__(self):
        self.records = pd.DataFrame(columns=['date', 'calories', 'exercise_minutes', 'bmi', 'score'])

    def add_record(self, calories, exercise_minutes, bmi, score):
        self.records = pd.concat([self.records, pd.DataFrame([{
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'calories': calories,
            'exercise_minutes': exercise_minutes,
            'bmi': bmi,
            'score': score
        }])], ignore_index=True)

    def latest(self):
        if self.records.empty:
            return {}
        return self.records.iloc[-1].to_dict()

class GameEngine:
    def __init__(self, stats_recorder):
        self.player = Player()
        self.boss = Boss(level=1)
        self.stats = stats_recorder
        self.start_time = time.time()
        self.actions = {
            'squat': self.player_attack,
            'jumping_jacks': self.player_charge,
            'leg_raise': self.player_dodge,
            'plank': self.player_block,
        }

    def player_attack(self):
        damage = self.player.attack_action(self.boss)
        self._boss_react()
        return f'你對 {self.boss.name} 傷害 {damage} HP'

    def player_charge(self):
        self.player.charge_action()
        self._boss_react()
        return '你集氣，攻擊力上升'

    def player_dodge(self):
        self.player.dodge_action()
        self._boss_react()
        return '你閃避提高，防禦力上升'

    def player_block(self):
        self.player.block_action()
        self._boss_react()
        return '你進入防禦模式，防禦力上升'

    def _boss_react(self):
        if self.boss.is_alive():
            damage = self.player.take_damage(self.boss.attack)
            self.player.score += 1
            self.player.update_stats(calories=0.8, seconds=1)
            if not self.player.is_alive():
                self.stats.add_record(self.player.calories, self.player.exercise_time / 60, self.player.bmi, self.player.score)
        else:
            self._spawn_next_boss()

    def _spawn_next_boss(self):
        self.player.score += 10
        self.player.update_stats(calories=12, seconds=15)
        # 等級循環：1 -> 2 -> 3 -> 1 ...
        next_level = (self.boss.level % 3) + 1
        self.boss = Boss(level=next_level)

    def handle_action(self, label):
        action = self.actions.get(label)
        if action:
            return action()
        return '找不到動作'

    def to_dict(self):
        return {
            'player': self.player.to_dict(),
            'boss': self.boss.to_dict(),
            'latest_record': self.stats.latest(),
        }
