package com.wardziniak.kafka.connect.email

import com.fasterxml.jackson.databind.json.JsonMapper
import com.fasterxml.jackson.module.scala.DefaultScalaModule
import com.wardziniak.kafka.connect.email.EmailSinkTask.log
import com.wardziniak.kafka.connect.email.EmailSinkTask.mapper
import com.wardziniak.kafka.connect.email.model.EmailMessage
import org.apache.commons.mail.SimpleEmail
import org.apache.kafka.connect.sink.ErrantRecordReporter
import org.apache.kafka.connect.sink.SinkRecord
import org.apache.kafka.connect.sink.SinkTask
import org.slf4j.Logger
import org.slf4j.LoggerFactory

import java.util

import scala.jdk.CollectionConverters.IterableHasAsScala

/**
  * Created by wardziniak on 29.11.2016.
  */
class EmailSinkTask extends SinkTask {
  private var config: EmailSinkConfig = _
  private var reporter: Option[ErrantRecordReporter] = None

  override def stop(): Unit = {
    log.info("email sink task has stopped")
  }

  override def put(records: util.Collection[SinkRecord]): Unit = {
    records.asScala
      .foreach(record => {
        try {
          val email = mapper.convertValue(record.value(), classOf[EmailMessage])
          sendEmail(email)
          log.debug("sent email")
        } catch {
          case error: Throwable => reporter match {
              case Some(reporter) => reporter.report(record, error)
              case _              => log.warn("unable to send email", error)
            }
        }
      })
  }

  override def start(props: util.Map[String, String]): Unit = {
    config = new EmailSinkConfig(props)
    log.info("email sink task has started")

    try {
      reporter = Option.when(context.errantRecordReporter() != null)(context.errantRecordReporter())
    } catch {
      case _: NoSuchMethodError    => reporter = None
      case _: NoClassDefFoundError => reporter = None
    }
  }

  override def version(): String = "0.0.1"

  private def sendEmail(emailMessage: EmailMessage): Unit = {
    val email = new SimpleEmail()
    email.setHostName(config.hostname())
    email.setSmtpPort(config.port())
    email.setAuthentication(config.username(), config.password())
    email.setFrom(config.fromAddress())
    email.setStartTLSEnabled(true)
    email.setSSLOnConnect(true)
    email.setSubject(emailMessage.title)
    email.setMsg(emailMessage.body)
    if (emailMessage.toRecipients.isDefined) {
      emailMessage.toRecipients.get.map(_.emailAddress).foreach(address => email.addTo(address))
    }
    email.send()
    log.info("Email sent")
  }
}

object EmailSinkTask {
  private val log: Logger = LoggerFactory.getLogger(classOf[EmailSinkTask])
  private val mapper: JsonMapper = JsonMapper.builder().addModule(DefaultScalaModule).build()
}
