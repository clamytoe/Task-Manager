from flasgger import Swagger

from task_manager import create_app

app = create_app()
swagger = Swagger(app)


if __name__ == "__main__":
    app.run(debug=True)  # progma: no cover
