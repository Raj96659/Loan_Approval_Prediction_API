

  <h1>Loan Approval Prediction API</h1>
  <div class="meta">A Flask REST API to <strong>train</strong>, <strong>test</strong> and <strong>predict</strong> loan approval using a Random Forest model. This repo contains the backend, model serialization, and examples to test via Postman or curl.</div>

  <h2>Features</h2>
  <ul>
    <li>Train model by uploading a CSV via <code>/train</code> (saves <code>model.pkl</code> and <code>encoders.pkl</code>).</li>
    <li>Evaluate model with a test CSV via <code>/test</code>.</li>
    <li>Predict loan approval with JSON input via <code>/predict</code>.</li>
    <li>Basic feature engineering included (e.g., <code>TotalIncome</code>, <code>Income_to_Loan</code>).</li>
  </ul>

  <h2>Repository structure</h2>
  <pre>
loan_approval_project/
├─ app.py              # Flask app with /train, /test, /predict
├─ requirements.txt    # Python dependencies
├─ README.html         # This file (or README.md)
├─ dataset/            # (optional) store CSVs for testing
├─ model.pkl           # generated after training
└─ encoders.pkl        # generated after training
  </pre>

  <h2>Requirements</h2>
  <pre>
Python 3.10+
Flask
pandas
scikit-learn
numpy
  </pre>
  <p>Install dependencies:</p>
  <pre>pip install -r requirements.txt</pre>

  <h2>Quick start (VS Code / Terminal)</h2>
  <ol>
    <li>Open project folder in VS Code.</li>
    <li>Create & activate a venv:
      <pre>python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
      </pre>
    </li>
    <li>Install requirements:
      <pre>pip install -r requirements.txt</pre>
    </li>
    <li>Run the Flask app:
      <pre>python app.py
# visit http://127.0.0.1:5000 (endpoints are POST)
      </pre>
    </li>
  </ol>

  <h2>API Endpoints</h2>

  <h3><code>/train</code> — Train model</h3>
  <p><strong>Method:</strong> POST<br>
     <strong>Body type:</strong> <code>form-data</code> &rarr; key = <code>file</code> (type = File)</p>
  <p>Example (Postman): choose file <code>loan_train.csv</code> as the <code>file</code> field.</p>
  <p>Response:</p>
  <pre>{
  "message": "Model trained successfully!",
  "accuracy": 0.85
}</pre>

  <h3><code>/test</code> — Evaluate model</h3>
  <p><strong>Method:</strong> POST<br>
     <strong>Body type:</strong> <code>form-data</code> &rarr; key = <code>file</code> (type = File)</p>
  <p>Response:</p>
  <pre>{
  "accuracy": 0.83
}</pre>

  <h3><code>/predict</code> — Predict loan approval</h3>
  <p><strong>Method:</strong> POST<br>
     <strong>Body type:</strong> <code>raw (application/json)</code></p>
  <p>Example JSON:</p>
  <pre>{
  "Gender": "Male",
  "Married": "Yes",
  "Dependents": "0",
  "Education": "Graduate",
  "Self_Employed": "No",
  "ApplicantIncome": 5000,
  "CoapplicantIncome": 2000,
  "LoanAmount": 150,
  "Loan_Amount_Term": 360,
  "Credit_History": 1,
  "Property_Area": "Urban"
}</pre>

  <p>Example response:</p>
  <pre>{
  "prediction": "Approved"
}</pre>

  <h2>curl examples</h2>
  <p>Train:</p>
  <pre>curl -X POST "http://127.0.0.1:5000/train" -F "file=@/path/to/loan_train.csv"</pre>

  <p>Predict:</p>
  <pre>curl -X POST "http://127.0.0.1:5000/predict" -H "Content-Type: application/json" -d '{"Gender":"Male","Married":"Yes","ApplicantIncome":5000,...}'</pre>

  <h2>Postman quick tips</h2>
  <ul>
    <li>For file endpoints use Body → <strong>form-data</strong>. Choose type <strong>File</strong> for the key <code>file</code>.</li>
    <li>For <code>/predict</code>, use Body → <strong>raw</strong> and select <strong>JSON</strong>.</li>
    <li>Create a Collection named <strong>Loan Approval API</strong> with three saved requests: Train, Test, Predict.</li>
  </ul>

  <h2>Feature engineering applied</h2>
  <ul>
    <li><code>TotalIncome</code> = ApplicantIncome + CoapplicantIncome</li>
    <li><code>Income_to_Loan</code> = TotalIncome / (LoanAmount + 1)</li>
    <li>Missing values: numeric &rarr; median, categorical &rarr; mode</li>
    <li>Categorical encoding via saved label encoders (<code>encoders.pkl</code>)</li>
  </ul>

  <h2>Troubleshooting</h2>
  <ul>
    <li><strong>Not Found</strong> error: ensure Flask is running (run <code>python app.py</code>) and you use exact endpoints: <code>/train</code>, <code>/test</code>, <code>/predict</code>.</li>
    <li><strong>Feature names mismatch</strong>: retrain the model (call <code>/train</code>) so <code>model.pkl</code> and <code>encoders.pkl</code> match expected features. Use the same feature names/order as the model.</li>
    <li>If Postman returns long-running request, click <strong>Cancel</strong> in Postman and check server logs in terminal.</li>
  </ul>


 </body>
</html>
