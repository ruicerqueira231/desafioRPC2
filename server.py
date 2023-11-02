from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from xmlrpc.client import Binary
from PIL import Image, ImageFilter
import os
import uuid


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


os.makedirs("processed_images", exist_ok=True)

task_status = {}


def process_image(task_id):
    if task_id in task_status and task_status[task_id] == "In Progress":
        image_path = os.path.join(os.getcwd(), f"{task_id}.jpg")

        # Load the image
        image = Image.open(image_path)

        # Apply image processing
        image = image.filter(ImageFilter.BLUR)  # Apply blur filter
        image = image.convert("L")  # Convert to grayscale

        # Define the path for processed_images directory
        processed_images_dir = os.path.join(os.getcwd(), "processed_images")

        # Save the processed image to the processed_images directory
        processed_image_path = os.path.join(processed_images_dir, f"{task_id}.jpg")
        image.save(processed_image_path)

        # Update task status
        task_status[task_id] = "Completed"

        # Remove the temporary image
        os.remove(image_path)

        return True
    else:
        return False


def create_task(image_data):
    task_id = str(uuid.uuid4())

    # Save the image temporarily
    image_path = os.path.join(os.getcwd(), f"{task_id}.jpg")
    with open(image_path, "wb") as f:
        f.write(image_data.data)

    # Update task status
    task_status[task_id] = "Created"

    return task_id


def get_task_status(task_id):
    status = task_status.get(task_id, "Invalid Task ID")
    return status


def get_processed_image(task_id):
    image_path = os.path.join(os.getcwd(), "processed_images", f"{task_id}.jpg")
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            image_data = Binary(f.read())
        return image_data
    else:
        return None


def change_task_status(task_id, new_status):
    if new_status == "Completed":
        process_result = process_image(task_id)
        if not process_result:
            return False

    current_status = get_task_status(task_id)

    if current_status == "Created" and new_status == "In Progress":
        task_status[task_id] = "In Progress"
        return True
    elif current_status == "In Progress" and new_status == "Completed":
        task_status[task_id] = "Completed"
        return True
    else:
        return False


with SimpleXMLRPCServer(('0.0.0.0', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    server.register_function(create_task, 'create_task')
    server.register_function(get_task_status, 'get_task_status')
    server.register_function(get_processed_image, 'get_processed_image')
    server.register_function(process_image, 'process_image')
    server.register_function(change_task_status, 'change_task_status')

    print("Server is running on port 8000...")
    server.serve_forever()






