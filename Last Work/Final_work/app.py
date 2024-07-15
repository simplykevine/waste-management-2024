from website import create_app
"""
    This script runs a Flask web application.

    It imports the `create_app` function from the `website` module and creates an instance of the Flask app.
    The app is then run in debugging mode.

    Usage:
        - Run this script to start the Flask web app.

    """
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
