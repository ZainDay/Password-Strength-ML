from flask import Flask, request
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np

app = Flask(__name__)

# Dataset
X = np.array([
    [4,0,0],[5,0,0],[6,1,0],
    [7,1,1],[8,1,1],[9,2,1],
    [10,2,2],[12,3,2],[14,3,3]
])
y = [0,0,0, 1,1,1, 2,2,2]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Accuracy
accuracy = accuracy_score(y, model.predict(X)) * 100

def features(pwd):
    return [[
        len(pwd),
        sum(c.isdigit() for c in pwd),
        sum(not c.isalnum() for c in pwd)
    ]]

@app.route("/", methods=["GET","POST"])
def home():
    result = ""
    width = "0%"
    if request.method == "POST":
        pwd = request.form["pwd"]
        pred = model.predict(features(pwd))[0]
        result = ["Weak", "Medium", "Strong"][pred]
        width = ["30%", "65%", "100%"][pred]

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Password Strength Checker</title>
<style>
:root {{
    --bg: #f4f6f8;
    --card: #ffffff;
    --text: #1f2933;
    --sub: #6b7280;
}}

@media (prefers-color-scheme: dark) {{
    :root {{
        --bg: #111827;
        --card: #1f2933;
        --text: #f9fafb;
        --sub: #9ca3af;
    }}
}}

body {{
    background: var(--bg);
    font-family: "Segoe UI", sans-serif;
    display: flex;
    justify-content: center;
    padding: 40px;
}}

.container {{
    background: var(--card);
    width: 520px;
    padding: 35px;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}}

h2,h3 {{
    color: var(--text);
}}

p,li,td {{
    color: var(--sub);
    font-size: 14px;
}}

input {{
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #d1d5db;
    margin-top: 10px;
}}

button {{
    width: 100%;
    margin-top: 15px;
    padding: 12px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}}

.bar {{
    height: 8px;
    background: #e5e7eb;
    border-radius: 5px;
    overflow: hidden;
    margin-top: 10px;
}}

.fill {{
    height: 100%;
    width: {width};
    background: linear-gradient(90deg,#ef4444,#f59e0b,#22c55e);
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}}

td {{
    border-bottom: 1px solid #e5e7eb;
    padding: 6px;
}}
</style>
</head>

<body>
<div class="container">

<h2>Password Strength Checker</h2>
<p>Machine Learning based password security evaluation</p>

<form method="post">
    <input type="password" name="pwd" placeholder="Enter password" required>
    <button>Evaluate</button>
</form>

<h3>Strength</h3>
<div class="bar"><div class="fill"></div></div>
<p><b>{result}</b></p>

<h3>Model Accuracy</h3>
<p>{accuracy:.2f}% on training data</p>

<h3>How ML Works</h3>
<ul>
<li>Password length</li>
<li>Number of digits</li>
<li>Number of special characters</li>
</ul>

<h3>Sample Dataset</h3>
<table>
<tr><td>abc</td><td>Weak</td></tr>
<tr><td>abc123</td><td>Medium</td></tr>
<tr><td>Abc@12345</td><td>Strong</td></tr>
</table>

</div>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)

