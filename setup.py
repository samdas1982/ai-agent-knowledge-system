"""Setup configuration for the AI Agent Knowledge System package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-agent-knowledge-system",
    version="1.0.0",
    author="AI Development Team",
    description="Enterprise Document Query System with Autonomous AI Agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samdas1982/ai-agent-knowledge-system",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "langchain>=0.1.0",
        "openai>=1.3.0",
        "faiss-cpu>=1.7.0",
        "sentence-transformers>=2.2.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "loguru>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "isort>=5.13.0",
        ],
        "pinecone": ["pinecone-client>=3.0.0"],
    },
    entry_points={
        "console_scripts": [
            "ai-knowledge=app.main:app",
        ],
    },
)
