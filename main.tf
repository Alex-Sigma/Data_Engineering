provider "aws" {
  region     = "eu-north-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_key_pair" "de_key" {
  key_name   = "dataops-key" # <-- имя ключа на AWS
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_security_group" "de_sg" {
  name        = "de-sg"
  description = "Allow SSH and Postgres"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "de_ec2" {
  ami                    = "ami-04a5f55f5196f401f"  # Ubuntu 22.04 LTS in eu-north-1
  instance_type          = "t3.medium"
  key_name               = aws_key_pair.de_key.key_name
  vpc_security_group_ids = [aws_security_group.de_sg.id]

  tags = {
    Name = "de-instance"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt update",
      "sudo apt install -y apt-transport-https ca-certificates curl software-properties-common",
      "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg",
      "echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu jammy stable' | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
      "sudo apt update",
      "sudo apt install -y docker-ce docker-ce-cli containerd.io",
      "sudo usermod -aG docker ubuntu",
      "sudo curl -L https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose",
      "sudo chmod +x /usr/local/bin/docker-compose"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }
  
  lifecycle {
    ignore_changes = [user_data]
  }
}

output "public_ip" {
  value = aws_instance.de_ec2.public_ip
}
