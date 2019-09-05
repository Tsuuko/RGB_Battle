
def __advantageBattle(player_BP,opponent_BP):
    player_BP*=1.3
    return __judge(player_BP,opponent_BP)

def __disadvantageBattle(player_BP,opponent_BP):
    opponent_BP*=1.3
    return __judge(player_BP,opponent_BP)

def __normalBattle(player_BP,opponent_BP):
    return __judge(player_BP,opponent_BP)

def __judge(player_BP,opponent_BP):
    if player_BP>opponent_BP:
        return "win"
    elif player_BP<opponent_BP:
        return "lose"
    else:
        return "draw"


def fight(player_color,player_BP,opponent_color,opponent_BP):
    if player_color=="R" and opponent_color=="G":
        battle_result=__advantageBattle(player_BP,opponent_BP)
    elif player_color=="G" and opponent_color=="B":
        battle_result=__advantageBattle(player_BP,opponent_BP)
    elif player_color=="B" and opponent_color=="R":
        battle_result=__advantageBattle(player_BP,opponent_BP)
    elif player_color=="R" and opponent_color=="B":
        battle_result=__disadvantageBattle(player_BP,opponent_BP)
    elif player_color=="B" and opponent_color=="G":
        battle_result=__disadvantageBattle(player_BP,opponent_BP)
    elif player_color=="G" and opponent_color=="R":
        battle_result=__disadvantageBattle(player_BP,opponent_BP)
    else:
        battle_result=__normalBattle(player_BP,opponent_BP)
    return battle_result

a=fight("R",2000,"G",2500)
print(a)
