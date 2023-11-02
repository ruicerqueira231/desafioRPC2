import xmlrpc.client

def create_task(image_path):
    with open(image_path, "rb") as f:
        image_data = xmlrpc.client.Binary(f.read())

    task_id = proxy.create_task(image_data)
    return task_id

def change_task_status(task_id, new_status):
    result = proxy.change_task_status(task_id, new_status)
    if result:
        print(f"Task {task_id} status changed to {new_status}.")
    else:
        print(f"Failed to change status for Task {task_id}.")

def get_task_status(task_id):
    status = proxy.get_task_status(task_id)
    return status

def process_image(task_id):
    result = proxy.process_image(task_id)
    if result:
        print(f"Image for Task {task_id} processed and status changed to 'Completed'.")
    else:
        print(f"Failed to process image for Task {task_id}.")

def menu():
    while True:
        print("\nMenu:")
        print("1. Create Task")
        print("2. Change Task Status to 'In Progress'")
        print("3. Change Task Status to 'Completed'")
        print("4. Check Task Status")
        print("5. Quit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            image_path = input("Enter the path of the image: ")
            task_id = create_task(image_path)
            print(f"Task created. ID: {task_id}")
        elif choice == "2":
            task_id = input("Enter the task ID: ")
            change_task_status(task_id, "In Progress")
        elif choice == "3":
            task_id = input("Enter the task ID: ")
            status = get_task_status(task_id)
            if status == "In Progress":
                change_task_status(task_id, "Completed")
            else:
                print("You can only mark a task as 'Completed' if it's in progress.")
        elif choice == "4":
            task_id = input("Enter the task ID: ")
            status = get_task_status(task_id)
            print(f"Task Status: {status}")
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    with xmlrpc.client.ServerProxy("http://localhost:8000/RPC2") as proxy:
        menu()



