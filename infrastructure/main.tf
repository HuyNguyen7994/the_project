provider "aws" {
  region = "us-east-1"
}

resource "aws_key_pair" "admin-key" {
  key_name   = "admin"
  public_key = file("credentials\\admin.pub")
}

resource "aws_instance" "single-node-website" {
  ami           = "ami-0e731c8a588258d0d"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.admin-key.key_name

  tags = {
    Name = "CUBoulder"
  }
}
