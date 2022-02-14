
from myapp import app



if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, port=5005)