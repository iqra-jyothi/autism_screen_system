from utils.predict import predict_autism


result, probability = predict_autism(
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    25
)


print("Prediction:", result)
print("Probability:", f"{probability * 100:.2f}%")