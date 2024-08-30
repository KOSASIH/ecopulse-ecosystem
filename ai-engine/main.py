import os
import argparse
from ai_engine.models.data import DataProcessor
from ai_engine.models.model import Model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, required=True)
    parser.add_argument('--learning_rate', type=float, default=0.001)
    parser.add_argument('--hidden_dim', type=int, default=128)
    parser.add_argument('--output_dim', type=int, default=10)
    args = parser.parse_args()

    file_path = args.file_path
    learning_rate = args.learning_rate
    hidden_dim = args.hidden_dim
    output_dim = args.output_dim

    data_processor = DataProcessor(file_path)
    data = data_processor.preprocess_data()
    X_train, X_test, y_train, y_test = data_processor.split_data()

    model = Model(X_train.shape[1], hidden_dim, output_dim, learning_rate)
    for epoch in range(10):
        model.train(X_train, y_train)
        y_pred = model.evaluate(X_test, y_test)
        accuracy, report, matrix = data_processor.evaluate_model(y_pred, y_test)
        print(f'Epoch {epoch+1}, Accuracy: {accuracy:.3f}')
        print(f'Classification Report:\n{report}')
        print(f'Confusion Matrix:\n{matrix}')

if __name__ == '__main__':
    main()
