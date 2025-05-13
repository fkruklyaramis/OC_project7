import csv
import time
from itertools import combinations


class Action:
    def __init__(self, name, cost, profit_percentage):
        self.name = name
        self.cost = cost
        self.profit_percentage = profit_percentage
        self.profit = cost * profit_percentage / 100

    def __str__(self):
        return f"{self.name} - Coût: {self.cost}€, Bénéfice: {self.profit_percentage}%, Profit: {self.profit:.2f}€"


def load_actions_from_csv(file_path):
    actions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Ignorer l'en-tête
        for row in csv_reader:
            name = str(row[0])
            cost = float(row[1])
            profit_percentage = float(row[2])
            actions.append(Action(name, cost, profit_percentage))
    return actions


def bruteforce_best_investment(actions, max_budget=500):
    """
    Trouve la meilleure combinaison d'actions pour maximiser le profit en testant
    toutes les combinaisons possibles
    Arguments:
        actions (list): Liste des objets Action
        max_budget (float): Budget maximum disponible
    Returns:
        tuple: (meilleure_combinaison, coût_total, profit_total)
    """
    best_combination = []
    best_profit = 0
    best_cost = 0
    total_combinations = 0
    # Tester toutes les combinaisons possibles, de taille 1 à len(actions)
    for action_count in range(1, len(actions) + 1):
        # La fonction combinations de itertools génère toutes les combinaisons
        # possibles de r actions parmi la liste d'actions
        for combo in combinations(actions, action_count):
            total_combinations += 1
            # Calculer le coût total de cette combinaison
            total_cost = sum(action.cost for action in combo)
            # Vérifier si cette combinaison respecte le budget
            if total_cost <= max_budget:
                # Calculer le profit total généré par cette combinaison
                total_profit = sum(action.profit for action in combo)
                # Si cette combinaison donne un meilleur profit, la garder
                if total_profit > best_profit:
                    best_profit = total_profit
                    best_combination = combo
                    best_cost = total_cost
    print(f"Nombre total de combinaisons testées: {total_combinations}")
    return best_combination, best_cost, best_profit


def main():
    start_time = time.time()
    actions = load_actions_from_csv('actions.csv')
    print(f"Nombre d'actions chargées: {len(actions)}")

    best_combination, best_cost, best_profit = bruteforce_best_investment(actions)
    print("\nMeilleure combinaison d'actions:")

    for action in best_combination:
        print(f"- {action}")
    print(f"\nCoût total: {best_cost:.2f}€")
    print(f"Profit total: {best_profit:.2f}€")
    print(f"Rendement: {(best_profit/best_cost*100):.2f}%")
    execution_time = time.time() - start_time
    print(f"\nTemps d'exécution: {execution_time:.4f} secondes")


if __name__ == "__main__":
    main()


"""
Initialisation des variables:
best_combination: Liste qui stockera la meilleure combinaison d'actions trouvée
best_profit: Variable pour garder trace du meilleur profit trouvé jusqu'à présent
best_cost: Variable pour stocker le coût de la meilleure combinaison
total_combinations: Compteur pour suivre combien de combinaisons sont testées

Génération de toutes les combinaisons:
La boucle extérieure for r in range(1, len(actions) + 1) itère sur toutes les tailles possibles de combinaisons, de 1 action à toutes les actions.
Pour chaque taille r, la fonction utilise combinations(actions, r) du module itertools pour générer toutes les combinaisons possibles de r actions parmi la liste complète.
exemple avec action A B C D : 
Quand r = 1 : la fonction combinations(actions, 1) génère :
(A)
(B)
(C)
(D)
Quand r = 2 : la fonction combinations(actions, 2) génère :
(A, B)
(A, C)
(B, C)
(A, D)
(B, D)
(C, D)
Quand r = 3 : la fonction combinations(actions, 3) génère :
(A, B, C)
(A, B, D)
(A, C, D)
(B, C, D)
Quand r = 4 : la fonction combinations(actions, 4) génère :
(A, B, C, D)


Évaluation de chaque combinaison: Pour chaque combinaison, la fonction:
Incrémente le compteur total_combinations
Calcule le coût total en additionnant le coût de chaque action dans la combinaison
Vérifie si le coût total respecte le budget maximum (500€ par défaut)
Si la combinaison est dans le budget, calcule le profit total généré

Sélection de la meilleure combinaison:
Si le profit total de la combinaison actuelle est meilleur que le meilleur profit trouvé jusqu'à présent, cette combinaison devient la nouvelle "meilleure combinaison"
La fonction met à jour best_profit, best_combination et best_cost

Résultat:
À la fin, la fonction affiche le nombre total de combinaisons testées
Elle retourne un tuple contenant la meilleure combinaison d'actions, son coût total et son profit total
Complexité
Cette approche bruteforce teste systématiquement toutes les combinaisons possibles, ce qui donne une complexité temporelle de O(2^n) où n est le nombre d'actions.
Pour 20 actions, cela signifie tester jusqu'à 2^20 = 1,048,576 combinaisons au total. Cette approche est exhaustive et garantit de trouver la solution optimale, mais elle devient inefficace pour un grand nombre d'actions."""
