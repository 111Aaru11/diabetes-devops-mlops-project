terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.23.1"
    }
  }
}

provider "docker" {
    host = "npipe:////./pipe/docker_engine"
}

resource "docker_image" "diabetes_app" {
  name = "aarushi1111/diabetes-app:latest"
}

resource "docker_container" "diabetes_container" {
  image = docker_image.diabetes_app.image_id
  name  = "terraform-diabetes-container"

  ports {
    internal = 5000
    external = 5001
  }
}