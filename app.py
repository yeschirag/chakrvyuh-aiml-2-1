from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# --- SECURE ANSWER STORAGE ---
# These are now hidden on the server, invisible to the user.
CORRECT_ANSWERS = {
    "1": "KANG",
    "2": "ThisIsPassword"
}

REWARD_LINKS = {
    "1": "https://drive.google.com/file/d/1o6uDWIs9gcR26Ybi_m4EmZSgetMggNA0/view?usp=drive_link",
    "2": "https://chakrvyuh-aiml-d2-c4.vercel.app/" # The final link
}
# -----------------------------

@app.route('/')
def index():
    """Serves the main challenge page."""
    return render_template('index.html')


@app.route('/check_answer', methods=['POST'])
def check_answer():
    """Handles answer submissions from the JavaScript."""
    
    # Get the JSON data sent from the browser
    data = request.json
    
    if not data or 'challenge' not in data or 'guess' not in data:
        return jsonify({"correct": False, "message": "Invalid request."}), 400

    challenge_id = str(data['challenge'])
    user_guess = data['guess']
    
    # --- Challenge 1: Riddle ---
    if challenge_id == "1":
        is_correct = (user_guess.upper() == CORRECT_ANSWERS["1"])
        if is_correct:
            # Send back a "correct" response and the secret link
            return jsonify({
                "correct": True,
                "secret_link": REWARD_LINKS["1"]
            })
        else:
            return jsonify({
                "correct": False,
                "message": "Incorrect. The variant escapes. Try again."
            })

    # --- Challenge 2: Passkey ---
    elif challenge_id == "2":
        is_correct = (user_guess == CORRECT_ANSWERS["2"]) # This one is case-sensitive
        if is_correct:
            # Send back "correct" and the final link
            return jsonify({
                "correct": True,
                "final_link": REWARD_LINKS["2"]
            })
        else:
            return jsonify({
                "correct": False,
                "message": "ACCESS DENIED. PASSKEY INCORRECT."
            })

    # Fallback for unknown challenge IDs
    return jsonify({"correct": False, "message": "Unknown challenge."}), 400


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)