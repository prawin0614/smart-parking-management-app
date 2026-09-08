from database import get_connection


def add_slot(slot_number, vehicle_type):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO parking_slots
        (slot_number, vehicle_type, status)
        VALUES (%s, %s, 'AVAILABLE')
    """

    cursor.execute(query, (slot_number, vehicle_type))

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message": "Parking slot added successfully",
        "slot_number": slot_number
    }


def get_all_slots():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, slot_number, vehicle_type, status
        FROM parking_slots
        ORDER BY slot_number
    """)

    slots = cursor.fetchall()

    cursor.close()
    connection.close()

    return slots


def update_slot_status(slot_id, status):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE parking_slots
        SET status = %s
        WHERE id = %s
    """, (status, slot_id))

    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    if affected_rows == 0:
        return {"message": "Slot not found"}

    return {"message": "Slot status updated successfully"}


def delete_slot(slot_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM parking_slots
        WHERE id = %s
    """, (slot_id,))

    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    if affected_rows == 0:
        return {"message": "Slot not found"}

    return {"message": "Parking slot deleted successfully"}