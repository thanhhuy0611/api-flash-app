from src import app

print(app.config['SQLALCHEMY_DATABASE_URI'],'dadasdsa')

#khoa

if __name__ == "__main__":
  app.run(debug=True, 
          # ssl_context='adhoc'
          )