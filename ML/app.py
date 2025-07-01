
# Example streamlit interface
import streamlit as st
import joblib
import pandas as pd

model = joblib.load("titanic_pipeline.pkl")
Pclass = st.selectbox("Pclass", [1, 2, 3])
Sex = st.selectbox("Sex", ["male", "female"])
Age = st.slider("Age", 0, 100, 25)
Fare = st.slider("Fare", 0.0, 500.0, 32.0)
Embarked = st.selectbox("Embarked", ["S", "C", "Q"])

if st.button("Predict"):
    X_new = pd.DataFrame([[Pclass, Sex, Age, Fare, Embarked]],
            columns=["Pclass", "Sex", "Age", "Fare", "Embarked"])
    pred = model.predict(X_new)
    st.write("Prediction:", "Survived" if pred[0] == 1 else "Did not survive")
