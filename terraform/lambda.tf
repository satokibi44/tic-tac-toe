
resource "aws_iam_role" "tic_tac_toe_lambda" {
  name               = "tic_tac_toe_lambda"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "tic_tac_toe" {
  function_name = "tic_tac_toe"
  role          = aws_iam_role.tic_tac_toe_lambda.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.tic_tac_toe.repository_url}:latest"
  architectures = ["arm64"]
  timeout       = 60
  lifecycle {
    ignore_changes = [image_uri]
  }
}

resource "aws_cloudwatch_log_group" "tic_tac_toe_lambda" {
  name              = "/aws/lambda/${aws_lambda_function.tic_tac_toe.function_name}"
  retention_in_days = 30
}

resource "aws_iam_role_policy_attachment" "tic_tac_toe_lambda_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.tic_tac_toe_lambda.name
}
