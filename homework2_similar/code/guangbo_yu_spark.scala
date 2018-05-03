import org.apache.spark.{SparkConf, SparkContext}
import java.io._
import scala.io.Source

/**
  * Created by guangboyu on 16/10/11.
  */
object guangbo_yu_spark {
  def main(args: Array[String]): Unit ={
    val conf = new SparkConf().setMaster("local").setAppName("film_frequent")
    val sc = new SparkContext(conf)
    val a_input = sc.textFile(args(0))
    val d_input = sc.textFile(args(1))
    val support = (args(2)).toInt
    //z//
    val a = a_input.filter(_.nonEmpty).
      map(line => line.split("',")).
      filter(_.length > 1).
      map(line => (line(0), line(1))).
      filter(_._1.length > 2).
      filter(_._2.length > 2).
      map{case (x,y) => (x.substring(2, x.length), y.substring(1, y.length - 1))}
    //a//
    val d = d_input.
      filter(_.nonEmpty).
      map(line => line.split("',")).
      filter(_.length > 1).
      map(line => (line(0), line(1))).
      filter(_._1.length > 2).
      filter(_._2.length > 2).
      map{case (x,y) => (x.substring(2, x.length), y.substring(1, y.length - 1))}
    //a//
    val ad = a.join(d)
    val aa = a.join(a)
    val dd = d.join(d)

    val adsort  = ad.
      map{case (x,(y,z)) => ((y,z), 1)}.
      reduceByKey((x,y) => x+y).
      filter(_._2 >= support).
      map{case(x,z) => (List(x._1, x._2), z)}.
      map{case(x,z) => ((x(0), x(1)), z)}



    val aasort =  aa.
      map{case (x,(y,z)) => ((y,z), 1)}.
      reduceByKey((x,y) => x+y).
      filter{case((x,y),z) => x != y}.
      filter(_._2 >= support).
      map{case(x,z) => (List(x._1, x._2).sorted, z)}.
      distinct.
      map{case(x,z) => ((x(0), x(1)), z)}


    val ddsort = dd.
      map{case (x,(y,z)) => ((y,z), 1)}.
      reduceByKey((x,y) => x+y).
      filter{case((x,y),z) => x != y}.
      filter(_._2 >= support).
      map{case(x,z) => (List(x._1, x._2).sorted, z)}.
      distinct.
      map{case(x,z) => ((x(0), x(1)), z)}

    val result = adsort.union(aasort).union(ddsort).sortBy(_._2, true)
    val writer = new PrintWriter("guangbo_yu_spark")
    for (i <- result.collect){
      writer.write(i + "\n")
    }
    writer.close()

  }

}
