from flask import Flask
app=Flask(__name__)

@app.route("/api/analyze/<wallet>")
def wallet(wallet):

    return 

if __name__=="__main__":
    app.run(debug=True)