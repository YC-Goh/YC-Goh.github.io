
import numpy as np
from collections import Counter, defaultdict

__N_AFFIXES_BY_REROLL_CHANCE = {
    0: 1, 
    20: 1, 
    30: 1, 
    40: 1, 
    50: 1, 
    60: 2, 
    70: 2, 
    80: 2, 
    90: 2, 
    95: 2, 
}

__AFFIX_IDS = list(__N_AFFIXES_BY_REROLL_CHANCE.values())
__AFFIX_IDS = [range(sum(__AFFIX_IDS[:i]), sum(__AFFIX_IDS[:i+1])) for i in range(len(__AFFIX_IDS))]

__AFFIXES_BY_REROLL_CHANCE = {
    f"_{id:03.0f}": chance / 100
    for chance, ids in zip(__N_AFFIXES_BY_REROLL_CHANCE.keys(), __AFFIX_IDS)
    for id in ids
}

__AFFIX_IDS = np.array(list(__AFFIXES_BY_REROLL_CHANCE.keys()))
__REROLL_CHANCE = np.array(list(__AFFIXES_BY_REROLL_CHANCE.values()))
__ROLL_CHANCE = np.array([1 / __AFFIX_IDS.shape[0] for _ in __AFFIX_IDS])

def __markov_matrix(reroll_chance, roll_chance):
    n = len(reroll_chance)
    P = np.zeros((n, n))
    
    # Normalize roll_chance to ensure it's a probability distribution
    roll_prob = roll_chance / roll_chance.sum()
    
    for i in range(n):
        if reroll_chance[i] == 0:
            # Absorbing state - stays in same state with probability 1
            P[i, i] = 1.0
        else:
            # Non-absorbing state
            # Probability of staying (not rerolling)
            P[i, i] = 1 - reroll_chance[i]
            
            # Probability of rerolling and landing on each state
            reroll_prob = reroll_chance[i]
            P[i, :] += reroll_prob * roll_prob
    
    return P

__MARKOV_MATRIX = __markov_matrix(__REROLL_CHANCE, __ROLL_CHANCE)

def __roll_affix(affix_ids: np.ndarray[str], roll_chance: np.ndarray[float], reroll_chance: np.ndarray[float]) -> str:
    affix_index, affix, p_reroll, reroll = None, None, None, True
    while reroll:
        affix_index = np.random.choice(range(len(affix_ids)), p=roll_chance)
        affix = affix_ids[affix_index].item()
        p_reroll = reroll_chance[affix_index].item()
        reroll = np.random.choice([True, False], p=[p_reroll, 1 - p_reroll])
    return affix

def main(rolls: int) -> None:
    # roll_ids = [__roll_affix(__AFFIX_IDS, __ROLL_CHANCE, __REROLL_CHANCE) for _ in range(rolls)]
    # num_roll_ids = dict(sorted(Counter(roll_ids).items()))
    # p_roll_ids = {id: n / rolls for id, n in num_roll_ids.items()}
    # p_roll_by_reroll = defaultdict(float)
    # for affix_id, p_roll in p_roll_ids.items():
    #     p_reroll = __AFFIXES_BY_REROLL_CHANCE[affix_id]
    #     p_roll_by_reroll[p_reroll] += p_roll
    r_tilde = __REROLL_CHANCE.mean()
    n = __REROLL_CHANCE.shape[0]
    r_factor = (1 / (1 - r_tilde)) / n
    p_roll = r_factor * (1 - __REROLL_CHANCE)
    p_roll_by_reroll = defaultdict(float)
    for i, p_reroll in enumerate(__REROLL_CHANCE):
        p_roll_by_reroll[p_reroll.item()] += p_roll[i].item()
    return p_roll_by_reroll

if __name__ == "__main__":
    print(main(10_000))
