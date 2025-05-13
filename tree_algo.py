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


class TreeNode:
    """Représente un nœud dans l'arbre de décision"""
    def __init__(self, action=None, parent=None):
        self.action = action  # Action associée à ce nœud (None pour la racine)
        self.parent = parent  # Référence au nœud parent
        self.include_child = None  # Enfant représentant l'inclusion de l'action suivante
        self.exclude_child = None  # Enfant représentant l'exclusion de l'action suivante

    def get_path(self):
        """Retourne la liste des actions dans le chemin de la racine à ce nœud"""
        actions = []
        current = self
        while current.parent is not None:
            if current.action is not None:  # Si c'est un nœud d'inclusion
                actions.append(current.action)
            current = current.parent
        return actions

    def calculate_cost_profit(self):
        """Calcule le coût total et le profit total du chemin jusqu'à ce nœud"""
        actions = self.get_path()
        total_cost = sum(action.cost for action in actions)
        total_profit = sum(action.profit for action in actions)
        return total_cost, total_profit


def tree_bruteforce(actions, max_budget=500):
    """
    Implémentation de l'algorithme brute force en utilisant un arbre binaire.
    Chaque niveau de l'arbre représente une décision d'inclure ou non une action.

    Arguments:
        actions (list): Liste des objets Action
        max_budget (float): Budget maximum disponible
    Returns:
        tuple: (meilleure_combinaison, coût_total, profit_total)
    """
    root = TreeNode()  # Créer le nœud racine (sans action)
    best_profit = 0
    best_combination = []
    nodes_explored = 0

    # Fonction récursive pour construire l'arbre et explorer toutes les combinaisons
    def build_tree(node, level):
        # nonlocal pour accéder aux variables de la portée englobante et non pas créer de nouvelles variables locales
        nonlocal best_profit, best_combination, nodes_explored
        nodes_explored += 1

        # Si on a atteint la fin de la liste d'actions, on évalue le nœud
        if level == len(actions):
            # Vérifier si cette combinaison est meilleure que la meilleure trouvée jusqu'à présent
            cost, profit = node.calculate_cost_profit()
            if cost <= max_budget and profit > best_profit:
                best_profit = profit
                best_combination = node.get_path()
            return

        # Créer l'enfant "inclusion" (ajouter l'action courante)
        current_action = actions[level]
        include_node = TreeNode(current_action, node)
        node.include_child = include_node
        # Calculer le coût en ajoutant cette action
        temp_cost, _ = include_node.calculate_cost_profit()

        # Ne construire le sous-arbre que si le budget n'est pas dépassé
        if temp_cost <= max_budget:
            build_tree(include_node, level + 1)
        # ne pas construire l'arbre si la renta n'est optimale

        # Créer l'enfant "exclusion" (ne pas ajouter l'action courante)
        exclude_node = TreeNode(None, node)
        node.exclude_child = exclude_node
        build_tree(exclude_node, level + 1)

    # Construire l'arbre en commençant par la racine
    build_tree(root, 0)

    # Calculer le coût total de la meilleure combinaison
    best_cost = sum(action.cost for action in best_combination)

    print(f"Nombre de nœuds explorés: {nodes_explored}")
    return best_combination, best_cost, best_profit


def main():
    start_time = time.time()
    actions = load_actions_from_csv('actions.csv')
    print(f"Nombre d'actions chargées: {len(actions)}")

    best_combination, best_cost, best_profit = tree_bruteforce(actions)
    print("\nMeilleure combinaison d'actions:")

    for action in best_combination:
        print(f"- {action}")
    print(f"\nCoût total: {best_cost:.2f}€")
    print(f"Profit total: {best_profit:.2f}€")
    print(f"Rendement: {(best_profit/best_cost*100) if best_cost > 0 else 0:.2f}%")
    execution_time = time.time() - start_time
    print(f"\nTemps d'exécution: {execution_time:.4f} secondes")


if __name__ == "__main__":
    main()


"""Structure de l'arbre :
Chaque nœud représente une décision concernant une action spécifique
Chaque nœud a deux enfants : "include_child" (on prend l'action) et "exclude_child" (on ne prend pas l'action)
L'arbre a autant de niveaux que d'actions disponibles
Exploration exhaustive :

L'algorithme construit et parcourt l'arbre complet de façon récursive
Chaque chemin de la racine à une feuille représente une combinaison d'actions unique
Toutes les combinaisons possibles sont examinées, comme dans l'algorithme de force brute
Optimisation de base :

Si à un moment donné le coût d'un chemin dépasse le budget, on arrête l'exploration de cette branche
Cette optimisation permet d'éviter d'explorer des combinaisons qui ne respectent pas la contrainte de budget
Trace du meilleur résultat :

À chaque nœud feuille, on compare le profit total avec le meilleur trouvé jusqu'à présent
Si on trouve une meilleure combinaison, on la sauvegarde"""
