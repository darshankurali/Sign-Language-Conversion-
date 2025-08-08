import pandas as pd
import matplotlib.pyplot as plt

# Simulated accuracy data (Replace with actual history)
previous_accuracies = [75, 80, 85, 90]  # Past accuracies of your model
previous_epochs = [1, 2, 3, 4]  # Past evaluation runs

# Example accuracy from previous works (Replace with actual values)
previous_works_accuracies = [70, 78, 82, 88]  # Another model's performance

# Current model evaluation
data = {
    "Sample #": list(range(1, 11)),
    "Predicted Class (ch1)": [7, 7, 7, 4, 6, 7, 7, 7, 7, 5],
    "Second Prediction (ch2)": [0, 0, 5, 2, 5, 6, 2, 7, 2, 0],
    "Correct?": [True, True, True, True, True, True, True, True, True, False],
    "Final Character": ["X", "Y", "Y", "L", "X", "Y", "Y", "Y", "Y", "1"]
}

df = pd.DataFrame(data)

# Compute current model accuracy
current_accuracy = sum(df["Correct?"]) / len(df["Correct?"]) * 100

# Update accuracy lists
previous_accuracies.append(current_accuracy)
previous_epochs.append(len(previous_accuracies))
previous_works_accuracies.append(previous_works_accuracies[-1])  # Assuming previous work had no new update

# Plot 1: Your model's accuracy over time
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)  # Create first subplot
plt.plot(previous_epochs, previous_accuracies, marker="o", linestyle="-", color="blue", label="Your Model")
plt.xlabel("Model Evaluation #")
plt.ylabel("Accuracy (%)")
plt.title("Your Model's Accuracy Over Time")
plt.ylim(0, 100)
plt.xticks(previous_epochs)
plt.grid(True)
plt.legend()

# Plot 2: Comparison with previous works
plt.subplot(1, 2, 2)  # Create second subplot
plt.plot(previous_epochs, previous_accuracies, marker="o", linestyle="-", color="blue", label="Your Model")
plt.plot(previous_epochs, previous_works_accuracies, marker="s", linestyle="--", color="red", label="Previous Work")
plt.xlabel("Model Evaluation #")
plt.ylabel("Accuracy (%)")
plt.title("Model Comparison Over Time")
plt.ylim(0, 100)
plt.xticks(previous_epochs)
plt.grid(True)
plt.legend()

# Show the plots
plt.tight_layout()
plt.show()
