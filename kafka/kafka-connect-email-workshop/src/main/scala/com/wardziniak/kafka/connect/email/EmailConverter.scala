import com.fasterxml.jackson.databind.json.JsonMapper
import com.fasterxml.jackson.module.scala.{ClassTagExtensions, DefaultScalaModule}
import org.apache.kafka.connect.data.{Schema, SchemaAndValue, SchemaBuilder}
import org.apache.kafka.connect.storage.Converter
import com.wardziniak.kafka.connect.email.model.EmailMessage

class EmailConverter extends Converter {
  private val mapper = JsonMapper.builder().addModule(DefaultScalaModule).build() :: ClassTagExtensions

  override def configure(configs: java.util.Map[String, _], isKey: Boolean): Unit = ()

  override def toConnectData(topic: String, value: Array[Byte]): SchemaAndValue = {
    val msg = mapper.readValue[EmailMessage](value)
    new SchemaAndValue(SchemaBuilder.struct().optional().build(), msg)
  }

  override def fromConnectData(topic: String, schema: Schema, value: Any): Array[Byte] =
    mapper.writeValueAsBytes(value)
}
