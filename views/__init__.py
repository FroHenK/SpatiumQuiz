import SpatiumQuiz

app = SpatiumQuiz.app


def init(app_t):
    global app
    app = app_t
    from views import admin
    from views import quiz_view
    from views import unsecure_api
