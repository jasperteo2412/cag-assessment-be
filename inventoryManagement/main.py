import os
import time
import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/test', methods=['GET'])
def test():
    message = {
        'hello': 'Hello world'
    }
    response = jsonify(message)
    return response

@app.route('/items', methods=['GET'])
def get_inventory():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM items")
        results = cursor.fetchall()
        response = jsonify(results)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/filter/date', methods=['POST'])
def filter_date_inventory():
    try:        
        _json = request.json
        _dt_from = _json['dt_from']
        _dt_to = _json['dt_to']
        if _dt_from and _dt_to and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "SELECT id, name, category, price FROM items WHERE last_updated_dt BETWEEN %s AND %s"
            bindData = (_dt_from, _dt_to)            
            cursor.execute(sqlQuery, bindData)
            results = cursor.fetchall()

            totalPrice = 0
            for row in results:
                totalPrice += row['price']
            
            response = jsonify({
                "items": [results],
                "total_price": totalPrice
            })

            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/category', methods=['POST'])
def category_inventory():
    try:        
        _json = request.json
        _category = _json['category']
        if _category and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            if _category == "all":
                sqlQuery = "SELECT category, sum(price) as total_price, count(*) as count FROM items GROUP BY category"
                cursor.execute(sqlQuery)
            elif _category:
                sqlQuery = "SELECT category, sum(price) as total_price, count(*) as count FROM items WHERE category = %s GROUP BY category"
                bindData = (_category)           
                cursor.execute(sqlQuery, bindData)
            else:
                return showMessage()
            
            results = cursor.fetchall()
            
            response = jsonify({
                "items": [results]
            })
            
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/filter', methods=['POST'])
def filter_inventory():
    try:        
        _json = request.json
        _name = _json['filters']['name']
        _category = _json['filters']['category']
        _price_range = _json['filters']['price_range']

        _page = _json['pagination']['page']
        _limit = _json['pagination']['limit']

        _field = _json['sort']['field']
        _order = _json['sort']['order']

        if _category and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "SELECT id, name, category, price FROM items WHERE "
            bindData = ()

            if _category != 'all':
                sqlQuery = sqlQuery+"category = %s AND "
                bindData += (_category,)

            if _price_range:
                sqlQuery = sqlQuery+"(price BETWEEN %s AND %s) AND "
                bindData += (_price_range[0], _price_range[1],)

            if _name:
                sqlQuery = sqlQuery+"name LIKE %s "
                bindData += ("%{}%".format(_name),)
            
            if _page and _limit and _field and _order:
                _start = 0
                if _page > 1:
                    _start =  (_page - 1) * _limit
                sqlQuery = sqlQuery+"ORDER BY %s %s LIMIT %s OFFSET %s"
                bindData += (_field, _order, _limit, _start,)

            cursor.execute(sqlQuery, bindData)
            results = cursor.fetchall()
            
            response = jsonify({
                "items": [results],
                "count": len(results),
                "page": _page,
                "limit": _limit
            })
            
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/insert', methods=['POST'])
def insert_inventory():
    try:        
        _json = request.json
        _name = _json['name']
        _email = _json['category']
        _phone = _json['price']
        if _name and _email and _phone and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)	
            _created_dt = time.strftime('%Y-%m-%d %H:%M:%S')
            _last_updated_dt = time.strftime('%Y-%m-%d %H:%M:%S')
            sqlQuery = "INSERT INTO items(name, category, price, created_dt, last_updated_dt) VALUES(%s, %s, %s, %s, %s)"
            bindData = (_name, _email, _phone, _created_dt, _last_updated_dt)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()

            cursor.execute("SELECT MAX(id) as id FROM items")
            results = cursor.fetchone()

            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'An error has ocurred at: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(port=8000, debug=os.getenv('DEBUG'))