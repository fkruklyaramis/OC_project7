import csv
import time


class Action:
    def __init__(self, name, cost, profit_percentage):
        self.name = name
        self.cost = cost
        self.profit_percentage = profit_percentage
        self.profit = (cost * profit_percentage) / 100
        self.ratio = profit_percentage / 100

    def __str__(self):
        """Représente l'action sous forme de chaîne de caractères"""
        return f"{self.name} - Coût: {self.cost}€, Bénéfice: {self.profit_percentage}%, Profit: {self.profit:.2f}€"

    def __lt__(self, other):
        """
        Compare les actions par ratio profit/coût décroissant.
        """
        # Utilisé pour le tri dans sorted()
        return self.ratio < other.ratio

    def __repr__(self):
        """
        Représente l'action sous forme de chaîne de caractères pour le débogage.
        """
        return f"{self.name} - Coût: {self.cost}€, Bénéfice: {self.profit_percentage}%, Profit: {self.profit:.2f}€"


def load_actions_from_csv(file_path):
    """
    Charge les actions depuis un fichier CSV.

    Cette fonction lit un fichier CSV contenant des informations sur les actions
    et crée une liste d'objets Action. Elle filtre les actions ayant un coût
    et un pourcentage de profit positifs.

    Args:
        file_path (str): Chemin vers le fichier CSV contenant les données des actions.
                         Le fichier doit avoir le format : nom,coût,pourcentage_profit

        list: Liste d'objets Action créés à partir des données du fichier CSV.
              Chaque objet Action contient un nom, un coût et un pourcentage de profit.

    Note:
        Le fichier CSV doit avoir un en-tête qui sera ignoré lors de la lecture.
        Seules les actions avec un coût > 0 et un pourcentage de profit > 0 sont incluses.
    """
    actions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Ignorer l'en-tête
        for row in csv_reader:
            name = str(row[0])
            cost = float(row[1])
            profit_percentage = float(row[2])
            if cost > 0 and profit_percentage > 0:
                actions.append(Action(name, cost, profit_percentage))
    return actions


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
    sorted_actions = sorted(actions.copy(), reverse=True)

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
    actions = load_actions_from_csv('csv/dataset2.csv')
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
