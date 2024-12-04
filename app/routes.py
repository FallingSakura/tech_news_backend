from flask import jsonify, request
from app import app, db
import re  # Regular expressions for email validation
from app.rss_to_json import fetch_rss_to_json, fetch_products_to_json, fetch_tools_to_json
from flask_cors import CORS # type: ignore

# give acess to frontend
CORS(app, origins=["http://localhost:3000","http://192.168.2.172","http://main-alb-1-1989302336.us-east-2.elb.amazonaws.com:3000","https://technews.fallingsakura.top"])
# Email validation function
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Homepage route
@app.route('/')
def home():
    return "Welcome to Tech News Aggregator!"

#######Newest Route (/newest))########
@app.route('/newest', methods=['GET'])
def get_newest():
    try:
        # Access the 'articles' collection
        articles_collection = db['articles']
        articles = list(articles_collection.find())

        # Convert MongoDB ObjectId to string for JSON serialization
        for article in articles:
            article['_id'] = str(article['_id'])

        return jsonify(articles), 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

#######Products Route (/products)########
@app.route('/products', methods=['GET'])
def get_products():
    try:
        # Access the 'articles' collection
        products_collection = db['products']
        products = list(products_collection.find())

        # Convert MongoDB ObjectId to string for JSON serialization
        for product in products:
            product['_id'] = str(product['_id'])

        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

########Categories route (/categories)########
@app.route("/categories", methods=['GET', 'POST'])
def get_categories():
    categories_collection = db['categories']  # Collection for categories
    
    if request.method == 'GET':
        try:
            # Fetch all categories (only 'category_name' field)
            categories = list(categories_collection.find({}, {"category_name": 1, "_id": 0}))  
            return jsonify({"categories": categories}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    if request.method == 'POST':
        try:
            # Get the category name from the request body
            data = request.json
            category_name = data.get("category_name")
            
            # Validate if category_name is provided
            if not category_name:
                return jsonify({"error": "Category name is required"}), 400
            
            # Insert the new category into the database
            categories_collection.insert_one({"category_name": category_name})
            
            return jsonify({"message": f"Category '{category_name}' added successfully!"}), 201
        except Exception as e:
            print(str(e))
            return jsonify({"error": str(e)}), 500
    
########Subscribe route (/subscribe)########
# •	This route accepts a POST request containing an email in JSON format.
# •	The email is saved in the subscribers collection in MongoDB.
@app.route("/subscribe", methods=['POST'])
def subscribe():
    try:
        # Get the email from the request form data
        email = request.json.get("email")

        # Validate if email exists in the request
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        # Validate email format
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        # Access the 'subscribers' collection
        subscribers_collection = db['subscribers']
        # Insert the email into the subscribers collection
        subscribers_collection.insert_one({"email": email})

        return jsonify({"message": "Subscription successful!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Error handling
    
########Tools route (/tools)########
@app.route('/tool', methods=['GET'])
def get_tools():
    try:
        # Access the 'articles' collection
        tools_collection = db['tools']
        tools = list(tools_collection.find())

        # Convert MongoDB ObjectId to string for JSON serialization
        for tool in tools:
            tool['_id'] = str(tool['_id'])

        return jsonify(tools), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
