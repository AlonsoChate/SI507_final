from flask import Flask, render_template, request
from rotten_tomatoes import get_basic
from final_proj import score_distribution, time_distribution, get_reviews, get_common_words

app = Flask(__name__)

basic_info = [] # movie name, description, image

''' Home Page
'''
@app.route('/')
def home():
    return render_template("home.html", error=False)


''' Main Page
'''
@app.route('/movie', methods=['POST'])
def movie():
    movie_name = request.form["movie_name"]
    global basic_info
    basic_info = get_basic(movie_name)
    if basic_info is not None:
        return render_template("movie.html", basic=basic_info)
    else:
        return render_template("home.html", error=True)


''' Main Page with visualization
'''
@app.route('/movie/visualization', methods=['POST'])
def visualization():
    option = request.form["options"]
    display = 0
    reviews = []
    words = []
    if option == "high score review":
        reviews = get_reviews(basic_info[0])
        display = 1
    if option == "low score review":
        reviews = get_reviews(basic_info[0], isHighScore=False)
        display = 2
    if option == "Overall score distribution":
        score_distribution(basic_info[0])
        display = 3
    elif option == "Score distribution with time":
        display = 4
        time_distribution(basic_info[0])
    elif option == "Common words":
        display = 5
        critic_high_words = get_common_words(basic_info[0], isHighScore=True, isCritics=True, num=30)
        critic_low_words = get_common_words(basic_info[0], isHighScore=False, isCritics=True, num=30)
        audience_high_words = get_common_words(basic_info[0], isHighScore=True, isCritics=False, num=30)
        audience_low_words = get_common_words(basic_info[0], isHighScore=False, isCritics=False, num=30)
        words = [critic_high_words, critic_low_words, audience_high_words, audience_low_words]
    return render_template("movie.html", basic=basic_info, display=display, reviews=reviews, words=words)


#################################
#    visualization images       #
#################################

''' overal score distribution
'''
@app.route('/<movie_name>_score_distribution')
def score(movie_name):
    return render_template(f"{movie_name}_score_distribution.html")


''' score distribution with time
'''
@app.route('/<movie_name>_time_distribution')
def time(movie_name):
    return render_template(f"{movie_name}_time_distribution.html")


if __name__ == '__main__':
    print("Starting app", app.name)
    app.run(debug=True)