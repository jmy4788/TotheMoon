import pandas as pd
import numpy as np
import tensorflow as tf
from transformers import TFRobertaModel, RobertaTokenizer
import optuna


# Read the CSV file
"""
df = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\BTC데이터\Input_df.csv')
# i want to use only columns 1, 2, 3, 4, 5
df = df.iloc[:, 1:6]
# Convert the dataframe to a NumPy array
data = df.to_numpy()
"""
input = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\BTC데이터\Input_df.csv')
output = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\BTC데이터\output_df.csv')
# Generate input and output data for time-series prediction
"""
X_train = np.array([data[i:i+timesteps] for i in range(len(data)-timesteps)])
X_train = X_train.astype(str)
y_train = data[timesteps:]
y_train = y_train.astype(str)

"""

input = input.values.tolist()
output = output.values.tolist()

X_train = input
y_train = output
"""
timesteps = 50
n_features = 5

X_train = np.random.rand(20, timesteps, n_features)
y_train = np.random.rand(20, n_features)
"""

def create_model(batch_size, learning_rate):
    # Load the transformer model
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    model = TFRobertaModel.from_pretrained('roberta-base')

    # Prepare the inputs
    input_ids = tokenizer.encode(X_train)
    attention_mask = [1] * len(input_ids)

    # Define the loss function and optimizer
    loss_fn = tf.keras.losses.MeanSquaredError()
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    # Create a metric to track the accuracy
    accuracy_metric = tf.keras.metrics.MeanSquaredError()

    for i in range(100):
        with tf.GradientTape() as tape:
            logits = model(input_ids, attention_mask=attention_mask)
            loss_value = loss_fn(y_train, logits)
            grads = tape.gradient(loss_value, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))
        # Update the accuracy metric
        accuracy_metric(y_train, logits)
        midterm_accuracy = accuracy_metric.result()
        print("Midterm accuracy of Train model : ", midterm_accuracy)
        print("Iteration:", i)
        
        with open('C:\Programming\python\TotheMoon\PyOneDark\인공지능모델\midterm_accuracy.txt', 'a') as f:
            f.write(str(midterm_accuracy))
        model.save('C:\Programming\python\TotheMoon\PyOneDark\인공지능모델\model_'+str(i)+'.h5', overwrite=True, include_optimizer=True)


    # Get the final accuracy
    final_accuracy = accuracy_metric.result()
    print("Final accuracy of Train model : ", final_accuracy)
    # save Final accuracy to local txt file
    with open('C:\Programming\python\TotheMoon\PyOneDark\인공지능모델\save_accuracy.txt', 'a') as f:
        f.write(str(final_accuracy))
    # Save the model
    model.save('C:\Programming\python\TotheMoon\PyOneDark\인공지능모델\model.h5', overwrite=True, include_optimizer=True)
    # Return the final accuracy
    return final_accuracy

def optimize_parameters(trial):
    # Define the hyperparameters to optimize
    batch_size = trial.suggest_int("batch_size", 16, 128)
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-4, 1e-2)

    # Create the model and return the final accuracy
    final_accuracy = create_model(batch_size, learning_rate)
    print("Final accuracy of optimize parameter : ", final_accuracy)
    # Return the final accuracy
    return final_accuracy

# Create a new study
study = optuna.create_study()

# Optimize the parameters
study.optimize(optimize_parameters, n_trials=10)

# Print the best parameters
print("Best parameters: ", study.best_params)

# Print the best parameters
print("Best parameters: ", study.best_params)

# Print the best trial's accuracy
print("Best trial's accuracy: ", study.best_trial.value)

# Print the best trial's number
print("Best trial's number: ", study.best_trial.number)

# Print the trials dataframe
print(study.trials_dataframe())


# save the best parameters to local txt file
with open('C:\Programming\python\TotheMoon\PyOneDark\인공지능모델\Best_parameters.txt', 'a') as f:
    f.write(str(study.best_params))

"""
checkpoint = tf.keras.callbacks.ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True)
model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, callbacks=[checkpoint])
"""