from pymongo import MongoClient

def users_db():
    client = MongoClient("mongodb+srv://kapengbarako:latte@test-cluster.qsvaj.mongodb.net/?retryWrites=true&w=majority&appName=Test-Cluster")
    user_db = client["user_db"]
    users = user_db["users"]

    return users

def dept_db():
    client = MongoClient("mongodb+srv://kapengbarako:latte@test-cluster.qsvaj.mongodb.net/?retryWrites=true&w=majority&appName=Test-Cluster")
    dept_db = client["dept_db"]
    dept = dept_db["dept"]

    return dept

def project_db():
    client = MongoClient("mongodb+srv://kapengbarako:latte@test-cluster.qsvaj.mongodb.net/?retryWrites=true&w=majority&appName=Test-Cluster")
    project_db = client["project_db"]
    projects = project_db["projects"]

    return projects

def task_db():
    client = MongoClient("mongodb+srv://kapengbarako:latte@test-cluster.qsvaj.mongodb.net/?retryWrites=true&w=majority&appName=Test-Cluster")
    project_db = client["project_db"]
    tasks = project_db["tasks"]

    return tasks

def image_db():
    client = MongoClient("mongodb+srv://kapengbarako:latte@test-cluster.qsvaj.mongodb.net/?retryWrites=true&w=majority&appName=Test-Cluster")
    images_db = client["images_db"]
    images = images_db["images"]

    return images