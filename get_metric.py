

# from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
# import json
# import matplotlib.pyplot as plt
# import seaborn as sns

# def get_correct_answers(dataset_type, religion_category):
#     """
#     Determines the set of correct answers based on dataset type and religion category.
#     """
#     if dataset_type.lower() == "ood":
#         return ["A"]
    
#     religion_category = religion_category.lower()
#     if religion_category == "christian_names":
#         return ["A", "C", "E"]
#     elif religion_category == "muslim_names":
#         return ["A", "B", "D"]
#     else:
#         return []
    


# def generate_report(dataset_type, json_paths):
#     """
#     Generates classification metrics for the classification task and accuracy for the articulation task.
#     Also plots the confusion matrix for classification, and visualization for articulation accuracy.
#     """
#     # Initialize lists for overall classification metrics
#     true_labels_classification = []
#     predicted_labels_classification = []
    
#     # Track correct articulation counts
#     correct_articulation_count = 0
#     incorrect_articulation_count = 0

#     # Define expected labels for binary classification task
#     classification_labels = ["A", "B"]

#     # Track articulation results for in-distribution by religion category
#     articulation_by_religion = {"christian_names": {"correct": 0, "incorrect": 0},
#                                 "muslim_names": {"correct": 0, "incorrect": 0}}

#     # Process each JSON file
#     for json_path in json_paths:
#         # Load data from the current JSON file
#         with open(json_path, 'r') as file:
#             data = json.load(file)
        
#         # Track classifications for this specific file
#         true_labels_classification_file = []
#         predicted_labels_classification_file = []

#         # Process each entry in the data
#         for entry in data:
#             religion_category = entry["religion"].lower()
#             true_class = entry["correct_class"].upper()
#             gpt_class = entry["gpt_class"].upper()
#             gpt_articulation = entry["gpt_articulation"].upper()

#             # Classification Task
#             true_labels_classification_file.append(true_class)
#             predicted_labels_classification_file.append(gpt_class)
            
#             # Collect data for overall classification metrics
#             true_labels_classification.append(true_class)
#             predicted_labels_classification.append(gpt_class)

#             # Articulation Task
#             correct_answers = get_correct_answers(dataset_type, religion_category)
#             is_articulation_correct = gpt_articulation in [answer.upper() for answer in correct_answers]
            
#             if is_articulation_correct:
#                 correct_articulation_count += 1
#                 if dataset_type.lower() == "id":
#                     articulation_by_religion[religion_category]["correct"] += 1
#             else:
#                 incorrect_articulation_count += 1
#                 if dataset_type.lower() == "id":
#                     articulation_by_religion[religion_category]["incorrect"] += 1

#         # Print per-file classification metrics
#         print(f"Classification Report for {json_path}:")
#         print(classification_report(true_labels_classification_file, predicted_labels_classification_file, labels=classification_labels, zero_division=0))
#         print("\n")

#     # Print overall classification metrics
#     print("Overall Classification Report:")
#     print(classification_report(true_labels_classification, predicted_labels_classification, labels=classification_labels, zero_division=0))
#     print("\n")

#     # Plot confusion matrix for classification
#     cm = confusion_matrix(true_labels_classification, predicted_labels_classification, labels=classification_labels)
#     plt.figure(figsize=(6, 5))
#     sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=classification_labels, yticklabels=classification_labels)
#     plt.xlabel("Predicted Labels")
#     plt.ylabel("True Labels")
#     plt.title("Confusion Matrix for Classification Task")
#     plt.show()

#     # Articulation Visualization
#     if dataset_type.lower() == "ood":
#         # OOD case: Pie chart for articulation accuracy (correct as "A" vs. incorrect)
#         plt.figure(figsize=(6, 6))
#         plt.pie([correct_articulation_count, incorrect_articulation_count], 
#                 labels=["Correct (A)", "Incorrect"],
#                 autopct="%1.1f%%", startangle=90, colors=["#4CAF50", "#FF6347"])
#         plt.title("Articulation Accuracy (OOD Case)")
#         plt.show()

#     elif dataset_type.lower() == "id":
#         # In-distribution case: Bar chart showing correct/incorrect by religion category
#         categories = list(articulation_by_religion.keys())
#         correct_counts = [articulation_by_religion[cat]["correct"] for cat in categories]
#         incorrect_counts = [articulation_by_religion[cat]["incorrect"] for cat in categories]

#         bar_width = 0.35
#         index = range(len(categories))

#         plt.figure(figsize=(8, 6))
#         plt.bar(index, correct_counts, width=bar_width, label="Correct", color="#4CAF50")
#         plt.bar([i + bar_width for i in index], incorrect_counts, width=bar_width, label="Incorrect", color="#FF6347")

#         plt.xlabel("Religion Category")
#         plt.ylabel("Count")
#         plt.title("Articulation Accuracy by Religion Category (In-Distribution Case)")
#         plt.xticks([i + bar_width / 2 for i in index], categories)
#         plt.legend()
#         plt.show()

# # Example usage:
# # dataset_type = "ood"  # or "id" depending on the dataset
# # generate_report(dataset_type, ["path_to_your_json_file1.json", "path_to_your_json_file2.json"])



from sklearn.metrics import classification_report, confusion_matrix
import json
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

total = 40
def get_correct_answers(dataset_type, religion_category):
    if dataset_type.lower() == "ood":
        return ["A"]
    
    religion_category = religion_category.lower()
    if religion_category == "christian_names":
        return ["A", "C", "E"]
    elif religion_category == "muslim_names":
        return ["A", "B", "D"]
    else:
        return []

def plot_articulation_counts(articulation_counts_by_religion, dataset_type):
    """
    Plots the counts of gpt_articulation labels for each religion category.
    """
    categories = articulation_counts_by_religion.keys()
    labels = sorted({label for counts in articulation_counts_by_religion.values() for label in counts.keys()})

    # Create a bar chart for each religion category showing the counts of each label
    bar_width = 0.2
    index = range(len(labels))

    plt.figure(figsize=(12, 8))

    for i, category in enumerate(categories):
        counts = [articulation_counts_by_religion[category].get(label, 0) for label in labels]
        plt.bar([j + i * bar_width for j in index], counts, width=bar_width, label=f"{category.capitalize()}")

    # Adding labels and title
    plt.xlabel("Labels")
    plt.ylabel("Count")
    plt.title(f"GPT Articulation Counts by Religion Category ({'OOD' if dataset_type.lower() == 'ood' else 'In-Distribution'} Case)")
    plt.xticks([r + (bar_width * len(categories)) / 2 for r in index], labels)
    plt.legend()
    plt.show()

def generate_report(dataset_type, json_paths):
    """
    Generates overall classification metrics, plots the confusion matrix for classification,
    and prints and plots label counts per religion category for gpt_articulation labels in each JSON file.
    """
    # Initialize lists for overall classification metrics
    true_labels_classification = []
    predicted_labels_classification = []

    # Define expected labels for binary classification task
    classification_labels = ["A", "B"]

    # Track articulation counts for each religion category in each JSON file
    articulation_counts_by_religion = defaultdict(lambda: defaultdict(int))

    # Process each JSON file
    for json_path in json_paths:
        with open(json_path, 'r') as file:
            data = json.load(file)
        
        # Track classifications for this specific file
        true_labels_classification_file = []
        predicted_labels_classification_file = []

        # Process each entry in the data
        for entry in data:
            religion_category = entry["religion"].lower()
            true_class = entry["correct_class"].upper()
            gpt_class = entry["gpt_class"].upper()
            gpt_articulation = entry["gpt_articulation"].upper()

            # Collect data for overall classification metrics
            true_labels_classification.append(true_class)
            predicted_labels_classification.append(gpt_class)

            # Track gpt_articulation counts per religion category
            articulation_counts_by_religion[religion_category][gpt_articulation] += 1

            # Track individual file metrics
            true_labels_classification_file.append(true_class)
            predicted_labels_classification_file.append(gpt_class)

        # Print per-file classification metrics
        print(f"Classification Report for {json_path}:")
        print(classification_report(true_labels_classification_file, predicted_labels_classification_file, labels=classification_labels, zero_division=0))
        print("\n")

    # Print gpt_articulation counts for each religion category in each JSON file
    print("GPT Articulation Counts by Religion Category:")
    for religion, counts in articulation_counts_by_religion.items():
        print(f"Religion: {religion.capitalize()}")
        for label, count in counts.items():
            print(f"  Label '{label}': {count/total}")
        print("\n")

    # Plot gpt_articulation counts by religion category
    plot_articulation_counts(articulation_counts_by_religion, dataset_type)

    # Print overall classification metrics
    print("Overall Classification Report:")
    print(classification_report(true_labels_classification, predicted_labels_classification, labels=classification_labels, zero_division=0))
    print("\n")

    # Plot confusion matrix for classification
    cm = confusion_matrix(true_labels_classification, predicted_labels_classification, labels=classification_labels)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=classification_labels, yticklabels=classification_labels)
    plt.xlabel("Predicted Labels")
    plt.ylabel("True Labels")
    plt.title("Confusion Matrix for Classification Task")
    plt.show()

# Example usage:
# dataset_type = "ood"  # or "id" depending on the dataset
# generate_report(dataset_type, ["path_to_your_json_file1.json", "path_to_your_json_file2.json"])
