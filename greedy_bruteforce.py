

# Calculer le ratio de chaque action
# Trier les actions par ratio décroissant avec quicksort
# Parcourir la liste triée et ajouter les actions à la combinaison tant que le coût total ne dépasse pas le budget

import csv
import time


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


def calculate_ratio(action):
    """Calcule le ratio profit/coût pour une action"""
    return action.profit_percentage / 100


def quicksort_actions(actions, low=0, high=None):
    """
    Implémentation de l'algorithme QuickSort pour trier les actions
    par ratio profit/coût décroissant.

    Arguments:
        actions (list): Liste des objets Action à trier
        low (int): Indice de début du sous-tableau à trier
        high (int): Indice de fin du sous-tableau à trier

    Returns:
        list: Liste triée des actions
    """
    if high is None:
        high = len(actions) - 1

    # Cas de base : si le sous-tableau a 0 ou 1 élément, il est déjà trié
    if low >= high:
        return

    # Fonction pour partitionner le tableau
    def partition(arr, low, high):
        # Choisir le pivot (dernier élément)
        pivot_ratio = calculate_ratio(arr[high])

        # Index du plus petit élément
        i = low - 1

        # Parcourir tous les éléments et comparer avec le pivot
        for j in range(low, high):
            # Si l'élément actuel a un ratio plus grand que le pivot (tri décroissant)
            if calculate_ratio(arr[j]) > pivot_ratio:
                # Échanger l'élément plus grand avec l'élément à l'index i+1
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        # Échanger le pivot avec l'élément à la position i+1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    # Trouver l'élément pivot, le placer à sa position correcte,
    # et placer tous les éléments plus grands à gauche et plus petits à droite
    pivot_index = partition(actions, low, high)

    # Trier récursivement les sous-tableaux
    quicksort_actions(actions, low, pivot_index - 1)
    quicksort_actions(actions, pivot_index + 1, high)

    return actions


def sort_actions_by_ratio(actions):
    """
    Trie les actions par ratio profit/coût décroissant.

    Arguments:
        actions (list): Liste des objets Action

    Returns:
        list: Liste triée des actions
    """
    return quicksort_actions(actions.copy())  # Retourne une copie triée pour ne pas modifier l'original


def greedy_investment(actions, max_budget=500):
    """
    Trouve une combinaison d'actions en utilisant une approche gloutonne.
    Trie les actions par ratio profit/coût et les sélectionne tant que le budget le permet.

    Arguments:
        actions (list): Liste des objets Action
        max_budget (float): Budget maximum disponible

    Returns:
        tuple: (combinaison_sélectionnée, coût_total, profit_total)
    """
    # Trier les actions par ratio profit/coût décroissant
    sorted_actions = sort_actions_by_ratio(actions)

    selected_combination = []
    total_cost = 0
    total_profit = 0

    # Parcourir les actions triées et les ajouter si possible
    for action in sorted_actions:
        if total_cost + action.cost <= max_budget:
            selected_combination.append(action)
            total_cost += action.cost
            total_profit += action.profit

    return selected_combination, total_cost, total_profit


def main():
    start_time = time.time()
    actions = load_actions_from_csv('actions.csv')
    print(f"Nombre d'actions chargées: {len(actions)}")

    best_combination, best_cost, best_profit = greedy_investment(actions)
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
