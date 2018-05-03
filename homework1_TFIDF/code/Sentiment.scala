package yu_guangbo_tweets
import scala.util.parsing.json
import java.io._

import scala.io.Source
import scala.util.parsing.json.JSON




/**
  * Created by guangboyu on 16/9/19.
  */
object Sentiment {
  def eliminate(str: String): String = {
    val word = str.split(" ")
    val newstr = word.filterNot(word => word.contains("@") || word.contains("#") || word.contains(":") || word.contains("http:"))
    val result = newstr.mkString(" ")
    result
  }

  def sentiScore(str: String, score: scala.collection.mutable.HashMap[String, Int]): Int = {
    var num: Int = 0
    val word = str.split(" ")
    for (w <- word) {
      if (score.contains(w)) num = num + score(w)
    }
    num
  }

  def main(args: Array[String]) {
    val score = new scala.collection.mutable.HashMap[String, Int]
    for (line <- Source.fromFile(args(1)).getLines()) {
      //read sentimental
      //scores from AFINN
      val sp = line.split("\t")
      val sn = sp(1).toInt
      score += (sp(0) -> sn)
    }
    val writer = new PrintWriter(new File("yu_guangbo_tweets_sentiment_first20.txt" ))
    var j = 1
    val senti_score = new scala.collection.mutable.HashMap[Int, Int]
    for (i <- Source.fromFile(args(0)).getLines if (j <= 20)) {
      /*val line = URLEncoder.encode(i, "UTF8")*/
      val json = JSON.parseFull(i).get.asInstanceOf[Map[String, Any]]
      val content = json("text").toString()
      val lower_content = content.toLowerCase()
      val text = eliminate(lower_content)
      val text_score = sentiScore(text, score)
      senti_score += (j -> text_score)
      val write_in = (j, text_score)
      writer.write(write_in.toString+"\n")
      j = j + 1
    }
    writer.close

  }

}
