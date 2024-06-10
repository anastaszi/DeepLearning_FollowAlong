---
title: DeepLearning FollowAlong
emoji: 📈
colorFrom: blue
colorTo: yellow
sdk: streamlit
sdk_version: 1.34.0
app_file: app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
To run the app locally, follow the instructions below.
1. Install python 12.0 or higher

2. Set up streamlit secret OpenAI API key
```
mkdir .streamlit
touch .streamlit/secrets.toml
echo 'SCOPE = "local"' >> .streamlit/secrets.toml
echo 'OPENAI_API_KEY = "YOUR_API_KEY"' >> .streamlit/secrets.toml
```
2. Create a virtual environment
```
python3 -m venv streamlit-env
```
3. Activate the virtual environment
```
source streamlit-env/bin/activate
```
4. Install the requirements
```
pip install -r requirements.txt
```
5. Run the app
```
streamlit run app.py
```
6. Open the browser and go to http://127.0.0.1:7860
7. To deactivate the virtual environment
```
deactivate
```


1. 
```
pip install ipykernel
python -m ipykernel install --user --name=my_env --display-name "Python (my_env)"
jupyter notebook app.ipynb
```