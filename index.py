from app import create_app

app = create_app()


# For Vercel
def handler(request):
    return app(request)


if __name__ == "__main__":
    app.run(debug=True)
