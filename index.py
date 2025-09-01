from app import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()


# For Vercel
def handler(request):
    return app(request)


if __name__ == "__main__":
    app.run(debug=True)
