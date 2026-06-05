from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Order

app = FastAPI()

# CREATE TABLES
Base.metadata.create_all(bind=engine)


# ---------------- DATABASE CONNECTION ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- HOME ----------------
@app.get("/")
def home():
    return {
        "message": "Order Management API running"
    }


# ---------------- CREATE DUMMY ORDERS ----------------
@app.get("/create-dummy")
def create_dummy(db: Session = Depends(get_db)):

    # CHECK EXISTING
    existing1 = db.query(Order).filter(Order.id == 1).first()
    existing2 = db.query(Order).filter(Order.id == 2).first()

    if existing1 or existing2:
        return {
            "message": "Dummy orders already exist"
        }

    # ORDER 1
    order1 = Order(
        id=1,
        customer_name="Joshnika",
        order_item="Laptop",
        address="New York",
        postal_code="23456",
        status="Processing"
    )

    # ORDER 2
    order2 = Order(
        id=2,
        customer_name="Gnanika",
        order_item="Mobile",
        address="California",
        postal_code="12345",
        status="Shipped"
    )

    db.add(order1)
    db.add(order2)

    db.commit()

    return {
        "message": "2 dummy orders created successfully"
    }


# ---------------- VERIFY CUSTOMER ----------------
@app.post("/verify")
def verify_identity(data: dict, db: Session = Depends(get_db)):

    print("RAW REQUEST:", data)

    # GET VALUES
    order_id = str(data.get("order_id", "")).strip()
    postal_code = str(data.get("postal_code", "")).strip()

    # CLEAN VALUES
    order_id = ''.join(filter(str.isdigit, order_id))
    postal_code = ''.join(filter(str.isdigit, postal_code))

    print("ORDER ID:", order_id)
    print("POSTAL CODE:", postal_code)

    # VALIDATE
    if not order_id or not postal_code:
        return {
            "verified": False,
            "message": "Order ID and Postal Code are required"
        }

    # FIND ORDER
    order = db.query(Order).filter(
        Order.id == int(order_id)
    ).first()

    # ORDER NOT FOUND
    if not order:
        return {
            "verified": False,
            "message": "Order not found"
        }

    # POSTAL CODE CHECK
    if str(order.postal_code).strip() != postal_code:
        return {
            "verified": False,
            "message": "Postal code mismatch"
        }

    # SUCCESS
    return {
        "verified": True,
        "message": "Verification successful"
    }


# ---------------- GET ORDER STATUS ----------------
@app.get("/orders/status/{order_id}")
def get_status(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        return {
            "message": "Order not found"
        }

    return {
        "order_id": order.id,
        "status": order.status
    }


# ---------------- MODIFY ORDER ----------------
@app.put("/modify-order")
def modify_order(data: dict, db: Session = Depends(get_db)):

    order_id = data.get("order_id")
    new_item = data.get("new_item")

    order = db.query(Order).filter(
        Order.id == int(order_id)
    ).first()

    if not order:
        return {
            "message": "Order not found"
        }

    order.order_item = new_item

    db.commit()

    return {
        "message": "Order updated successfully"
    }


# ---------------- CANCEL ORDER ----------------
@app.put("/cancel/{order_id}")
def cancel_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        return {
            "message": "Order not found"
        }

    order.status = "Cancelled"

    db.commit()

    return {
        "message": "Order cancelled successfully"
    }


# ---------------- RETURN ORDER ----------------
@app.post("/return")
def return_order(data: dict):

    return {
        "message": f"Return initiated for order {data.get('order_id')}",
        "reason": data.get("reason")
    }


# ---------------- REPORT ISSUE ----------------
@app.post("/report-issue")
def report_issue(data: dict):

    return {
        "message": "Issue reported successfully",
        "issue_type": data.get("issue_type")
    }