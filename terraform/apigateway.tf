################################################################################
# API Gateway                                                                  #
################################################################################
resource "aws_api_gateway_rest_api" "go_container_image" {
  name = local.apigateway_name
  body = data.template_file.apigateway_body.rendered
}

data "template_file" "apigateway_body" {
  template = file("./apigateway_body.yaml")

  vars = {
    title                            = local.apigateway_name
    aws_account                      = data.aws_caller_identity.self.account_id
    aws_region_name                  = data.aws_region.current.name
    lambda_getemployee_function_name = aws_lambda_function.getemployee.function_name
  }
}

resource "aws_api_gateway_stage" "prod" {
  stage_name    = "prod"
  rest_api_id   = aws_api_gateway_rest_api.go_container_image.id
  deployment_id = aws_api_gateway_deployment.for_prod.id

  cache_cluster_enabled = false
  xray_tracing_enabled  = false
}

resource "aws_api_gateway_deployment" "for_prod" {
  rest_api_id = aws_api_gateway_rest_api.go_container_image.id

  triggers = {
    redeployment = sha1(jsonencode([
      data.template_file.apigateway_body.rendered,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}