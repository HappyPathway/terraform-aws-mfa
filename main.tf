variable "mfa_token" {
  description = "MFA Token from MFA Access Device"
}


variable "region" {
  description = "AWS Region"
}

data "external" "session_token" {
  program = ["python", "${path.module}/scripts/get_session_token.py"]

  query = {
    mfa_token  = "${var.mfa_token}"
    region     = "${var.region}"
  }
}

output "session_token" {
  value = "${data.external.session_token.result.session_token}"
}

output "access_key" {
  value = "${data.external.session_token.result.access_key}"
}

output "secret_key" {
  value = "${data.external.session_token.result.secret_key}"
}
