


from flask import Flask, request , render_template , url_for
from flask_pymongo import PyMongo

import pymongo


client = pymongo.MongoClient("localhost", 27017)
db = client.demo
app = Flask(__name__)
#uri for mongodb change user and password to your own username and password for mongodb and change database name at end
app.config['MONGO_URI'] = 'mongodb://user:password@localhost:27017/demo'
mongo = PyMongo(app)
result = []

# default route for the site if the it is accessed via "GET" it will return the main page
# if it is accessed via "POST" it will return the search page with the result requested
@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        title = (request.form["title"])
        if title is not None:
            return search(title)
    return main()


# function that actually inserts data into the mongodb database
# with mild form validation will not insert null objects into database
@app.route('/create', methods=['POST'])
def create():
    title = request.form.get('title')
    price = request.form.get('price')
    desc = request.form.get('desc')
    tag = request.form.get('tag')
    img = request.form.get('img')
    if 'img' in request.files:
        img = request.files['img']
        mongo.save_file(img.filename, img)
        if title and price and desc and tag and img:
            # inserting into collection
            # will create the collection if the one specified doesnt exist
            # mongo.db.<insert collection name you would like to use here>.insert
            mongo.db.democollection.insert({'title': request.form.get('title'),
                                            'price': request.form.get('price'), 'desc': request.form.get('desc'),
                                            'tag': request.form.get('tag'), 'img_name': img.filename})
            return main()
    return add()


# function to retrieve images from the db is used when displaying data takes in the file name in the url
@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


# search function takes in a title and uses the mongo db "find"
# function to search the database which is then looped through and displayed
@app.route('/search')
def search(title):
    final = ""
    # using regex to load the query var with the title passed in
    query = {"title": {"$regex": title, "$options": "i"}}
    # appending all the data to the end of the final var after every loop
    # change to collection you would like to use
    # returning the final var which is now full of the necessary html code
    for item in db.democollection.find(query):
        imgstring = item['img_name']
        final = final + f'''
        
       <div class="col-sm-3"> 
       <img src="{url_for('file', filename=imgstring)}" height= 300>
       <h5>
                <b>Title: {item["title"]}</b>
        </h5>
        <h5>
                <b>Price: ${item["price"]}</b>
        <h5>
                <b>Description: {item["desc"]}</b>
        </h5>
                <br>
        </div>

        '''
    return '''
    <div><button class="button button1" onclick="document.location='/'" style="margin-top: px; margin-bottom: 20px; 
    color: #ffffff; 
                    background-color: #1E90FF;">Main Menu</button>
    </div>
    
    <head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    </head>
    <html>
    <style> body { background-color: #ffd633; } 
    
.button {
  border: none;
  color: white;
  padding: 5px 30px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 2px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
}

.button1 {
  background-color: white;
  color: black;
  border: 2px solid #4CAF50;
}

.button1:hover {
  background-color: #4CAF50;
  color: white;
}

.button2 {
  background-color: white;
  color: black;
  padding: 3px 25px;
  border: 2px solid #008CBA;
}

.button2:hover {
  background-color: #008CBA;
  color: white;
}

    </style>
 
    
    <div class="row">

    ''' + final + '''
    </div> 
    
    </html>'''



# works exactly the same as search function but instead searching for tag instead of title
# except this is a post method receiving info from a form instead of passing data through a function call
@app.route('/tag', methods=['POST'])
def tag():
    final = ""
    query = {"tag": {"$regex": request.form.get('tag'), "$options": "i"}}
    # change to collection you would like to use
    for item in db.democollection.find(query):
        imgstring = item['img_name']
        final = final + f'''
        
       <div class="col-sm-3"> 
       <img src="{url_for('file', filename=imgstring)}" height= 300>
       <h5>
                <b>Title: {item["title"]}</b>
        </h5>
        <h5>
                <b>Price: ${item["price"]}</b>
        <h5>
                <b>Description: {item["desc"]}</b>
        </h5>
                <br>
        </div>

        '''
    return '''
    <div><button class="button button1" onclick="document.location='/'" style="margin-top: px; margin-bottom: 20px; color: #ffffff; 
                    background-color: #1E90FF;">Main Menu</button>
    </div>
    
    <head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    </head>
    <html>
    <style> body { background-color: #ffd633; } 
    
.button {
  border: none;
  color: white;
  padding: 5px 30px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 2px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
}

.button1 {
  background-color: white;
  color: black;
  border: 2px solid #4CAF50;
}

.button1:hover {
  background-color: #4CAF50;
  color: white;
}

.button2 {
  background-color: white;
  color: black;
  padding: 3px 25px;
  border: 2px solid #008CBA;
}

.button2:hover {
  background-color: #008CBA;
  color: white;
}

    </style>
 
    
    <div class="row">

    ''' + final + '''
    </div> 
    
    </html>'''



# the main menu for the page just returns basic html
@app.route('/main')
def main():
    return '''
    <head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<style>

.button {
  border: none;
  color: white;
  padding: 5px 30px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 2px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
}

.button1 {
  background-color: white;
  color: black;
  border: 2px solid #4CAF50;
}

.button1:hover {
  background-color: #4CAF50;
  color: white;
}

.button2 {
  background-color: white;
  color: black;
  padding: 3px 25px;
  border: 2px solid #008CBA;
}

.button2:hover {
  background-color: #008CBA;
  color: white;
}

body { 

  background: url("http://127.0.0.1:5000/file/MicrosoftTeams-image (13).png") no-repeat fixed center; background-size: 
  cover; 
}
</style>
    </head>
        <html>
            <body style="Arial Black, Gadget, sans-serif">
            <div style="margin-top: 50px;">
            <div class="col-xs-4 col-xs-offset-5">
            <h2 style="white-space: nowrap; text-align: center;">
            Web Catalog in Python with MongoDB</h2>
            <h3>
                 <button class="button button1" onclick="document.location='/add'" background-color: white; 
                 color: black; 
                 border: 2px solid #008CBA;>Add Item</button>
                 <button class="button button1" onclick="document.location='/team'" background-color: white; 
                 color: black; 
                 border: 2px solid #008CBA;>Team Members</button>
            </h3>
</div>
                <form method="post" action=".">
                <div class="form-group">
                    <div class="col-xs-2 col-xs-offset-5">
                    <h3>
                     <div style="margin-top: 10px;">
                    <p>Search</p>
                    </h3>
                    <input class="button button1" name="title" />
                    <input class="button button2" type="submit" value="Go" />
                    </div>
                </form>
                </div>
                <br>
                <br>
                <br>
                <form method="post" action="/tag">
                <div class="col-xs-4 col-xs-offset-5">
                <h3>
                <label for="title">View By Category</label>
                </h3>
                <select class="button button1" name="tag" id="tag">
                    <option value="shirts">Shirts</option>
                    <option value="pants">Pants</option>
                    <option value="shoes">Shoes</option>
                </select>
                <input class="button button2" type="submit" value="Go" />
                </div>
                </form>
                 <form method="post" action="/all">
                 <div class="col-xs-4 col-xs-offset-5" style="margin-top: 10px;">
                 <input class="button button1" type="submit" value="View All" />
                 </form>
                 </div>
                 </div>
            </body>
            </body>
        </html>
    '''


# works the same as the search and tag functions except the find field is empty and returns all data in the database
# equivalent to select * in sql
@app.route('/all', methods=['POST'])
def all():
    final = ""
    # change to collection you would like to use
    for item in db.democollection.find():
        imgstring = item['img_name']
        final = final + f'''
        
       <div class="col-sm-3"> 
       <img src="{url_for('file', filename=imgstring)}" height= 300>
       <h5>
                <b>Title: {item["title"]}</b>
        </h5>
        <h5>
                <b>Price: ${item["price"]}</b>
        <h5>
                <b>Description: {item["desc"]}</b>
        </h5>
                <br>
        </div>

        '''
    return '''
    <div><button class="button button1" onclick="document.location='/'" style="margin-top: px; margin-bottom: 20px; color: #ffffff; 
                    background-color: #1E90FF;">Main Menu</button>
    </div>
    
    <head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    </head>
    <html>
    <style> body { background-color: #ffd633; } 
    
.button {
  border: none;
  color: white;
  padding: 5px 30px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 2px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
}

.button1 {
  background-color: white;
  color: black;
  border: 2px solid #4CAF50;
}

.button1:hover {
  background-color: #4CAF50;
  color: white;
}

.button2 {
  background-color: white;
  color: black;
  padding: 3px 25px;
  border: 2px solid #008CBA;
}

.button2:hover {
  background-color: #008CBA;
  color: white;
}

    </style>
 
    
    <div class="row">

    ''' + final + '''
    </div> 
    
    </html>'''


# returns html form which sends data to the /create route above
@app.route('/add')
def add():

    return '''
    <head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<style> body { background-color: #ffd633; } </style>
    </head>
    <html>
     <form method="post" action="/create" enctype="multipart/form-data">
     <div class="form-group">
                    <div class="col-xs-4 col-xs-offset-4">
                        <label for="title">Title</label>
                        <input type="text" class="form-control" name="title"/>
                    </div>
                    <div class="col-xs-4 col-xs-offset-4">
                        <label for="price">Price</label>
                        <input type="text" class="form-control" name="price"/>
                    </div>
                    <div class="col-xs-4 col-xs-offset-4">
                        <label for="desc">Description</label>
                        <input class="form-control" type="text" name="desc"/>
                    </div>
                    <div class="col-xs-4 col-xs-offset-4">
                        <label for="tag">Choose a Tag</label>
                        <select class="form-control" name="tag" id="tag">
                        <option value="shirts">Shirts</option>
                        <option value="pants">Pants</option>
                        <option value="shoes">Shoes</option>
                    </div>
                </select></p>
                <label for="img">Choose a Image </label>
                    Image<input type="file" class="form-control"  name="img"/>
                    <input class="form-control" type="submit" value="Submit" style="margin-top: 50px; color: #ffffff; 
                    background-color: #1E90FF;"/> 
                    <br>
                    <h3><a href="/" style="color: #ffffff; 
                    background-color: #1E90FF; text-align: center;">Main Menu</a></h3>
                    
    </div>                
    
    </form>
    
    </html>

                '''


@app.route('/team')
def team():
    return '''
    
    </div>

    <head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    </head>
    <html>
    <div style="text-align: center; border: 2px solid #008CBA; margin-top: 40px "> 
    <h1>Team Members<h2/>
    <h2>Sajeel Nazir </h2>
    <h2>Ali, Wajahat</h2>
    <h2>Badrian Watt </h2>
    <h2>Sharony Rashid</h2>
    <h2>Jarod Porter</h2>
    <h2>Polina Sherriuble </h2>
    
    
    </div>
    <div style="text-align: center;margin-top: 10px; margin-bottom: 20px; 
    color: #ffffff; background-color: #1E90FF;"><button class="button button1" 
    onclick="document.location='/'" >Main Menu</button>
    </div>
    <style> body { background-color: #ffd633; } 

.button {
  border: none;
  color: white;
  padding: 5px 30px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 2px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
}

.button1 {
  background-color: white;
  color: black;
  border: 2px solid #4CAF50;
}

.button1:hover {
  background-color: #4CAF50;
  color: white;
}

.button2 {
  background-color: white;
  color: black;
  padding: 3px 25px;
  border: 2px solid #008CBA;
}

.button2:hover {
  background-color: #008CBA;
  color: white;
}

    </style>


    <div class="row">

    </div> 

    </html>'''

