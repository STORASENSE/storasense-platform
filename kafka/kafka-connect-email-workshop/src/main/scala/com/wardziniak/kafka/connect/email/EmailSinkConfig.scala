package com.wardziniak.kafka.connect.email

import com.wardziniak.kafka.connect.email.EmailSinkConfig.FROM_ADDRESS_KEY
import com.wardziniak.kafka.connect.email.EmailSinkConfig.HOST_NAME_KEY
import com.wardziniak.kafka.connect.email.EmailSinkConfig.PASSWORD_KEY
import com.wardziniak.kafka.connect.email.EmailSinkConfig.SMTP_PORT_KEY
import com.wardziniak.kafka.connect.email.EmailSinkConfig.USERNAME_KEY
import org.apache.kafka.common.config.AbstractConfig
import org.apache.kafka.common.config.ConfigDef

class EmailSinkConfig(originals: java.util.Map[String, String])
    extends AbstractConfig(EmailSinkConfig.config(), originals) {

  def hostname(): String = {
    getString(HOST_NAME_KEY)
  }

  def port(): Int = {
    getInt(SMTP_PORT_KEY)
  }

  def username(): String = {
    getString(USERNAME_KEY)
  }

  def password(): String = {
    getPassword(PASSWORD_KEY).value()
  }

  def fromAddress(): String = {
    getString(FROM_ADDRESS_KEY)
  }

}

object EmailSinkConfig {
  val HOST_NAME_KEY: String = "wardziniak.email.connect.hostname"
  val SMTP_PORT_KEY: String = "wardziniak.email.connect.smtp.port"
  val FROM_ADDRESS_KEY: String = "wardziniak.email.connect.from.address"
  val USERNAME_KEY: String = "wardziniak.email.connect.username"
  val PASSWORD_KEY: String = "wardziniak.email.connect.password"

  def config(): ConfigDef = {
    new ConfigDef()
      .define(
        HOST_NAME_KEY,
        ConfigDef.Type.STRING,
        "",
        new ConfigDef.NonNullValidator(),
        ConfigDef.Importance.HIGH,
        "SMTP Host"
      )
      .define(
        SMTP_PORT_KEY,
        ConfigDef.Type.INT,
        "465",
        ConfigDef.Range.between(1, 65535),
        ConfigDef.Importance.HIGH,
        "SMTP Port"
      )
      .define(
        USERNAME_KEY,
        ConfigDef.Type.STRING,
        "",
        new ConfigDef.NonNullValidator(),
        ConfigDef.Importance.HIGH,
        "SMTP Username"
      )
      .define(
        PASSWORD_KEY,
        ConfigDef.Type.PASSWORD,
        "",
        new ConfigDef.NonNullValidator(),
        ConfigDef.Importance.HIGH,
        "SMTP Password"
      )
      .define(
        FROM_ADDRESS_KEY,
        ConfigDef.Type.STRING,
        "",
        new ConfigDef.NonNullValidator(),
        ConfigDef.Importance.HIGH,
        "From Address"
      )
  }

}
