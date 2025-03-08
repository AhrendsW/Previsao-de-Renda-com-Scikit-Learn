from setuptools import setup, find_packages

setup(
    name="previsao_renda",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.1.0",
        "numpy>=1.24.3",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.2",
        "seaborn>=0.12.2",
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "streamlit>=1.28.0",
        "ucimlrepo>=0.0.3",
        "joblib>=1.3.2",
        "python-dotenv>=1.0.0"
    ],
    python_requires=">=3.9.5",
)