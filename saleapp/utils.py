import sqlite3

def get_Item(query):
    conn = sqlite3.connect("data/cart.db")
    data = conn.execute(query).fetchall()
    conn.close()
    return data

def add_Item_in_Cart(id, productId, quantity):
    conn = sqlite3.connect("data/cart.db")
    product = get_Item('select * from product where id like "1"')
    sql = """
        INSERT INTO cartItem(id, productId, price, quantity, subtotal) 
        VALUES (?, ?, ?, ?, ?)
    """
    conn.execute(sql, (id, product[0][0], product[0][2], quantity, product[0][2]*quantity))
    conn.commit()

def update_Item_in_Cart(id, quantity):
    conn = sqlite3.connect("data/cart.db")
    sql = """
       UPDATE CartItem
           SET 
                quantity = ?
           WHERE 
               id = ?
    """
    print(int(id) + quantity)
    conn.execute(sql, (quantity, int(id), ))
    conn.commit()

def delete_Item_in_Cart(id):
    conn = sqlite3.connect("data/cart.db")
    sql = """
       DELETE FROM CartItem
      WHERE id = ?
    """
    conn.execute(sql, (int(id), ))
    conn.commit()

if __name__ == "__main__":
    # print(get_Item('select * from cartItem'))
    # add_Item_in_Cart(3, 1, 2)
    update_Item_in_Cart("2", 10)
    # delete_Item_in_Cart("1")
