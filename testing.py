from final_proj import get_review_raw_data, get_trees_from_global

movie_name = "THE SHAWSHANK REDEMPTION"

raw_data = get_review_raw_data(movie_name)

scoreTree, timeTree = get_trees_from_global(raw_data, movie_name)
