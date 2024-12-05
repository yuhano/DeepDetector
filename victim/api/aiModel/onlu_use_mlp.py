import joblib
import os

# Define the relative paths to the files
base_path = os.path.dirname(__file__)
vectorizer_path = os.path.join(base_path, 'tfidf_vectorizer.pkl')
label_encoder_path = os.path.join(base_path, 'label_encoder.pkl')
mlp_model_path = os.path.join(base_path, 'mlp_model.pkl')

# Load the saved TF-IDF vectorizer and label encoder
try:
    vectorizer = joblib.load(vectorizer_path)
    label_encoder = joblib.load(label_encoder_path)
    mlp_model = joblib.load(mlp_model_path)
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# Define the function to predict with the MLP model
def predict_with_mlp(query):
    # 입력 텍스트를 TF-IDF로 변환
    query_tfidf = vectorizer.transform([query])
    
    # MLP 모델로 예측
    pred = mlp_model.predict(query_tfidf)
    label = label_encoder.inverse_transform(pred)
    
    return label[0]  # 예측 결과 반환

# 사용 예제
if __name__ == "__main__":
    user_input = input("분류할 SQL 쿼리를 입력하세요: ")
    prediction = predict_with_mlp(user_input)
    print("\n예측 결과:")
    print(f"MLP: {prediction}")
