from flask import Flask, request, redirect, url_for
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np

app = Flask(__name__)

X = np.array([
    [4,0,0],[5,0,0],[6,1,0],
    [7,1,1],[8,1,1],[9,2,1],
    [10,2,2],[12,3,2],[14,3,3]
])
y = [0,0,0, 1,1,1, 2,2,2]

model = LogisticRegression()
model.fit(X, y)
accuracy = accuracy_score(y, model.predict(X)) * 100

def features(pwd):
    return [[
        len(pwd),
        sum(c.isdigit() for c in pwd),
        sum(not c.isalnum() for c in pwd)
    ]]

css = """
<style>
* { box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }

body {
    background: #0f172a;
    color: #e5e7eb;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.card {
    background: #020617;
    width: 420px;
    padding: 35px;
    border-radius: 14px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.6);
}

h2 {
    margin-bottom: 5px;
}

p {
    color: #94a3b8;
    font-size: 14px;
}

input {
    width: 100%;
    padding: 12px;
    margin-top: 12px;
    border-radius: 8px;
    border: 1px solid #1e293b;
    background: #020617;
    color: #e5e7eb;
}

button {
    width: 100%;
    padding: 12px;
    margin-top: 18px;
    background: #2563eb;
    border: none;
    border-radius: 8px;
    color: white;
    cursor: pointer;
    font-size: 15px;
}

button:hover {
    background: #1e40af;
}

.bar {
    height: 8px;
    background: #1e293b;
    border-radius: 6px;
    margin-top: 10px;
    overflow: hidden;
}

.fill {
    height: 100%;
    background: linear-gradient(90deg,#ef4444,#f59e0b,#22c55e);
}

a {
    color: #60a5fa;
    text-decoration: none;
    font-size: 14px;
}

.error {
    color: #f87171;
    margin-top: 10px;
}
</style>
"""

# ---------------- LOGIN PAGE ----------------
@app.route("/", methods=["GET","POST"])
def login():
    error = ""
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            return redirect(url_for("checker"))
        else:
            error = "Invalid username or password"

    return f"""
    {css}
    <div class="card">
        <h2>Secure Login</h2>
        <p>Access the password strength analyzer</p>

        <form method="post">
            <input name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button>Login</button>
        </form>

        <div class="error">{error}</div>
    </div>
    """

# ---------------- PASSWORD CHECKER ----------------
@app.route("/checker", methods=["GET","POST"])
def checker():
    result = ""
    width = "0%"

    if request.method == "POST":
        pred = model.predict(features(request.form["pwd"]))[0]
        result = ["Weak","Medium","Strong"][pred]
        width = ["30%","65%","100%"][pred]

    return f"""
    {css}
    <div class="card">
        <h2>Password Strength Checker</h2>
        <p>ML-based password security evaluation</p>

        <form method="post">
            <input type="password" name="pwd" placeholder="Enter password" required>
            <button>Evaluate</button>
        </form>

        <div class="bar">
            <div class="fill" style="width:{width}"></div>
        </div>

        <p><b>{result}</b></p>
        <p>Model Accuracy: {accuracy:.2f}%</p>

        <a href="/">Logout</a>
    </div>
    """

if __name__ == "__main__":
    app.run(debug=True)


