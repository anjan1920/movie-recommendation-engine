from config import (
    MAX_LIKED_MOVIES,
    MOVIE_TITLE_COLUMN,
    USER_ID_TYPE
)



def normalize_title(title: str) -> str:
    return title.strip().lower()


def validate_request(data, df_movies):
    if not data:
        return False, "Request body must be JSON"

    # "userID" section validation
    if "user_id" not in data:
        return False, "user_id is required"
    # Else 
    user_id = data["user_id"]
    if not isinstance(user_id, USER_ID_TYPE):
        return False, f"user_id must be {USER_ID_TYPE.__name__}"

    

    

    return True, None
