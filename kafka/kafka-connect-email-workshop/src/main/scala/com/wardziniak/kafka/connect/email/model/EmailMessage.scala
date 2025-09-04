package com.wardziniak.kafka.connect.email.model

import com.fasterxml.jackson.annotation.JsonProperty

/**
  * Created by wardziniak on 01.12.2016.
  */
case class EmailMessage(
  @JsonProperty("title") title: String,
  @JsonProperty("body") body: String,
  @JsonProperty("toRecipients") toRecipients: Option[List[Recipient]]
)

case class Recipient(@JsonProperty("name") name: String, @JsonProperty("emailAddress") emailAddress: String)
