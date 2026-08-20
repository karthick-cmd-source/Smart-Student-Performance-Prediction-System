1. Keep your existing 20+ row student_performance_dataset_ml_300.csv.
2. pip install -r requirements.txt
3. python train_model.py
4. Import n8n_gemini_gmail_workflow.json into n8n Cloud.
5. In Google Gemini 2.5 Flash node, select your existing Gemini credential.
6. In Gmail node, select your existing Gmail OAuth2 credential.
7. Activate the workflow and copy the Production webhook URL.
8. Paste it into N8N_WEBHOOK_URL in prototype_ml.py.
9. python prototype_ml.py
10. Enter Student ID, Name, Email and academic values. Predict sends data to n8n, Gemini generates the recommendation, Gmail sends it, n8n returns it, and Python saves it to the same CSV.
Never share API keys, passwords or OAuth tokens.
