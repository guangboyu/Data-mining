package yu_guangbo_tweets

import java.io.{File, PrintWriter}

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SparkSession
import scala.util.parsing.json


/**
  * Created by guangboyu on 16/9/19.
  */
object TFDF {
  def eliminate(str: String) : String = {
    val word = str.split(" ")
    val newstr = word.filterNot(word => word.contains("rt") || word.contains("@") || word.contains("#") || word.contains(":") || word.contains("http") || word.equals("") || word.contains("www"))
    val result_1 = newstr.mkString(" ")
    val result = result_1.replaceAll("\\pP|\\pS", "")
    result
  }

  def main(args: Array[String]): Unit ={
    val sparkConf = new SparkConf().setAppName("TFDF").setMaster("local")
    val sc = new SparkContext(sparkConf)
    val tweet = sc.textFile(args(0))
    val tweet_20 = tweet.take(20)
    val tweet_20_rdd = sc.parallelize(tweet_20)

    import org.apache.spark.sql.SparkSession


    val spark = SparkSession.builder().appName("Spark SQL Example").config("spark.some.config.option", "some-value").getOrCreate()

    import spark.implicits._

    val tweet_sql = spark.read.json(tweet_20_rdd)
    val tweet_text = tweet_sql.select("text")
    val pr = tweet_text.count
    val tweet_rdd = tweet_text.as[String].rdd
    val tweet_count = tweet_rdd
    //words count
    val tweet_count_sum = tweet_count.flatMap(line => line.split(" ")).map(word => (eliminate(word.toLowerCase), 1)).reduceByKey(_+_)
    val array_2 = new scala.collection.mutable.ArrayBuffer[(String, List[Int])]
    for(i <-1 to 20){
      val l = i
      val line = tweet_count.take(i).drop(i-1)
      val line_RDD = sc.parallelize(line)
      val line_count = line_RDD.flatMap(line => line.split(" ")).map(word => (eliminate(word.toLowerCase), 1)).reduceByKey(_+_) //RDD[(String, Int)]
      val line_output = line_count.map{case (word, count) => (word, List(l, count))}
      val line_format = line_output.collect//Map[(String, List(Int)]
      array_2 ++= line_format
    }
    val map_rdd_1 = sc.parallelize(array_2)
    val map_rdd_2 = map_rdd_1.groupByKey() //unique key
    val new_map_1 = tweet_count_sum.join(map_rdd_2)
    val new_map = new_map_1.sortByKey(true)
    val final_map = new_map.map{case (word, (count, d)) => (word, count, d)}
    val final_seq_1 = final_map.collect.toSeq
    val final_seq = final_seq_1.drop(1)
    val writer = new PrintWriter(new File("yu_guangbo_tweets_tfdf_first20.txt" ))
    for(x <- final_seq){
      writer.write(x + "\n")
    }
    writer.close()


  }

}
