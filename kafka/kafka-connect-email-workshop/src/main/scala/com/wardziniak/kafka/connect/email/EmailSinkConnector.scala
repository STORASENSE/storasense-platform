package com.wardziniak.kafka.connect.email

import org.apache.kafka.common.config.ConfigDef
import org.apache.kafka.connect.connector.Task
import org.apache.kafka.connect.sink.SinkConnector
import org.slf4j.Logger
import org.slf4j.LoggerFactory

import java.util

import scala.jdk.CollectionConverters.SeqHasAsJava

/**
  * Created by wardziniak on 29.11.2016.
  */
class EmailSinkConnector extends SinkConnector {
  private val log: Logger = LoggerFactory.getLogger(classOf[EmailSinkConnector])
  private var configuration: EmailSinkConfig = _

  override def taskClass(): Class[_ <: Task] = classOf[EmailSinkTask]

  override def taskConfigs(maxTasks: Int): util.List[util.Map[String, String]] =
    (1 to maxTasks).map(_ => configuration.originalsStrings()).asJava

  override def stop(): Unit = { log.info("stopping email sink connector") }

  override def config(): ConfigDef = EmailSinkConfig.config()

  override def start(props: util.Map[String, String]): Unit = {
    configuration = new EmailSinkConfig(props)
    log.info("starting email sink connector")
  }

  override def version(): String = "0.1.1"
}
