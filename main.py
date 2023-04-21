from flask import Flask, render_template, request
from rotten_tomatoes import get_basic
from final_proj import score_distribution

app = Flask(__name__)

basic_info = [] # movie name, description, image

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/movie', methods=['POST'])
def movie():
    movie_name = request.form["movie_name"]
    global basic_info
    basic_info = get_basic(movie_name)
    return render_template("movie.html", basic=basic_info)


@app.route('/movie/visualization', methods=['POST'])
def visualization():
    option = request.form["options"]
    display = 0
    if option == "Overall score distribution":
        score_distribution(basic_info[0])
        display = 1
    elif option == "Score distirbution with time":
        # TODO:
        display = 2
    return render_template("movie.html", basic=basic_info, display=display)

# visualization htmls
@app.route('/<movie_name>_score_distribution')
def distribution(movie_name):
    return render_template(f"{movie_name}_score_distribution.html")

if __name__ == '__main__':
    print("Starting app", app.name)
    app.run(debug=True)