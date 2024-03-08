import pytest
import sys
from os.path import abspath, dirname
# Ajoutez le chemin du dossier src au chemin de recherche des modules
sys.path.append(abspath(dirname(dirname(__file__))))
from src.calculator import Calculator

# Reste du code inchangé...

@pytest.fixture
def calculator():
    return Calculator()

def test_add(calculator):
    assert calculator.add(3, 5) == 8

def test_subtract(calculator):
    assert calculator.subtract(10, 4) == 6

def test_multiply(calculator):
    assert calculator.multiply(2, 5) == 10

def test_divide(calculator):
    assert calculator.divide(10, 2) == 5
    with pytest.raises(ValueError):
        calculator.divide(10, 0)
