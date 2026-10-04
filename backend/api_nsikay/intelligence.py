from api_nsikay.models import ModerationRecord



BLOCK_WORDS = [

    "fraude",

    "arnaque",

    "spam"

]



def moderate_content(text):


    risk = 0


    lower = text.lower()


    for word in BLOCK_WORDS:

        if word in lower:

            risk += 40



    status = "SAFE"


    if risk >= 80:

        status = "BLOCKED"

    elif risk >= 40:

        status = "REVIEW"



    return {

        "risk":risk,

        "status":status

    }




def recommendation_score(

    views,

    likes,

    shares

):


    return (

        views * 0.4

        +

        likes * 0.3

        +

        shares * 0.3

    )


