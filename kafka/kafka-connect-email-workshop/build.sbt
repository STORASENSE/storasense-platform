ThisBuild / scalaVersion := "2.13.14"
ThisBuild / scalacOptions ++= Seq("-release:11", "-deprecation", "-Werror")
ThisBuild / organization := "com.wardziniak"

name := "kafka-connect-email"

libraryDependencies ++= Seq(
  "org.apache.kafka" % "connect-api" % "3.8.0" % "provided",
  "org.apache.commons" % "commons-email" % "1.6.0",
  "com.fasterxml.jackson.core" % "jackson-databind" % "2.17.2",
  "com.fasterxml.jackson.core" % "jackson-annotations" % "2.17.2",
  "com.fasterxml.jackson.module" %% "jackson-module-scala" % "2.17.2"
)

// sbt-assembly settings (Slash-Syntax)
import sbtassembly.AssemblyPlugin.autoImport._
import sbtassembly.MergeStrategy
import sbtassembly.PathList

assembly / assemblyMergeStrategy := {
  case PathList("META-INF", _ @ _*) => MergeStrategy.discard
  case _                            => MergeStrategy.first
}
