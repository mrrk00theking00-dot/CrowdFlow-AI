from flask import Flask, render_template, request, jsonify
import csv, io
app = Flask(__name__)
buses = 8
approvals = {
  1: {"title":"Petition: Request for extra buses for Marudhamalai Festival","status":"Pending"},
  2: {"title":"Mail Verification: Sudden Crowd Alert — Event at CODISSIA","status":"Pending"}
}
@app.get("/")
def home(): return render_template("index.html")
@app.get("/health")
def health(): return jsonify(status="ok", app="FREEWAY 2.0", mode="demo")
@app.post("/api/allocate")
def allocate():
    global buses
    buses += 1
    return jsonify(ok=True, buses=buses, message="One extra bus allocated in demo mode.")
@app.post("/api/reroute")
def reroute():
    enabled = bool((request.get_json(silent=True) or {}).get("enabled"))
    return jsonify(ok=True, enabled=enabled, message=("Reroute recommendations enabled." if enabled else "Reroute recommendations disabled."))
@app.post("/api/approval/<int:item_id>")
def approval(item_id):
    action=(request.get_json(silent=True) or {}).get("action")
    if item_id not in approvals or action not in ("approve","reject"): return jsonify(ok=False,message="Invalid request."),400
    approvals[item_id]["status"]="Approved" if action=="approve" else "Rejected"
    return jsonify(ok=True,status=approvals[item_id]["status"],message=f"Request {approvals[item_id]['status'].lower()} in demo mode.")
@app.post("/api/upload")
def upload():
    f=request.files.get("dataset")
    if not f or not f.filename: return jsonify(ok=False,message="Choose a CSV file first."),400
    if not f.filename.lower().endswith(".csv"): return jsonify(ok=False,message="Please choose a CSV file."),400
    try:
        reader=csv.DictReader(io.StringIO(f.stream.read().decode("utf-8-sig")))
        rows=list(reader)
        if not reader.fieldnames or not rows: raise ValueError("CSV needs a header row and at least one data row.")
        return jsonify(ok=True,message=f"Validated {len(rows)} rows and {len(reader.fieldnames)} columns in {f.filename}. Demo data was not changed.")
    except Exception as e: return jsonify(ok=False,message=f"CSV validation failed: {e}"),400
@app.post("/api/logout")
def logout(): return jsonify(ok=True,message="This prototype is in demo mode; real authentication is not configured.")
if __name__=="__main__": app.run(debug=True, host="127.0.0.1", port=5000)
