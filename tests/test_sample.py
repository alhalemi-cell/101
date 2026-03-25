import pytest
import battlesim.models as m
import battlesim.constants as c

def test_damage():
    M1: m.Monster = c.Monsters.ARCANINE
    M2: m.Monster = c.Monsters.BLASTOISE

    # Might give error not sure why
    M1.attack(M1.moves.GetMove(1), M2, c.TypeRelations.GetEffectiveMultiplier)

    assert M2.current_health == 35
