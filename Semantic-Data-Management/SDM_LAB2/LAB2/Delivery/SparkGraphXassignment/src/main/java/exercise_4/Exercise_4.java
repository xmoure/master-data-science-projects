package exercise_4;

import com.clearspring.analytics.util.Lists;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SQLContext;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.MetadataBuilder;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import org.graphframes.GraphFrame;
import static org.apache.spark.sql.functions.*;
import java.util.ArrayList;
import java.util.List;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Exercise_4 {
	private static final double DAMPING_FACTOR = 0.85;
	private static final int MAX_NUM_ITERATIONS = 10;
	public static void wikipedia(JavaSparkContext ctx, SQLContext sqlCtx) throws Exception {
		try {
			Dataset<Row> vertices = readAndLoadVertices(ctx, sqlCtx);
			Dataset<Row> edges = readAndLoadEdges(ctx, sqlCtx);
			GraphFrame gf = GraphFrame.apply(vertices, edges);

			System.out.println(gf);

			gf.edges().show();
			gf.vertices().show();

			GraphFrame pageRank = gf.pageRank()
					.resetProbability(1 - DAMPING_FACTOR)
					.maxIter(MAX_NUM_ITERATIONS)
					.run();
			pageRank.vertices().select("id", "title", "pagerank")
					.orderBy(desc("pagerank"))
					.limit(10)
					.show();
		}catch(FileNotFoundException e){
			System.err.format("FileNotFoundException: "+ e);
		}catch (Exception ex){
			System.err.format("Error: "+ ex);
		}
	}


	private static Dataset<Row> readAndLoadVertices(JavaSparkContext ctx, SQLContext sqlCtx) throws FileNotFoundException {

		File verticesFile = new File("src/main/resources/wiki-vertices.txt");
		List<Row> vertices_list = new ArrayList<Row>();
		Scanner scannerVertices = new Scanner(verticesFile);
		while (scannerVertices.hasNextLine()) {
			String line = scannerVertices.nextLine();
			String[] data = line.split("\t", 2);
			String id = data[0];
			String title = data[1];
			vertices_list.add(RowFactory.create(id,title));
		}
		scannerVertices.close();
		JavaRDD<Row> vertices_rdd = ctx.parallelize(vertices_list);

		StructType vertices_schema = new StructType(new StructField[]{
				new StructField("id", DataTypes.StringType, true, new MetadataBuilder().build()),
				new StructField("title", DataTypes.StringType, true, new MetadataBuilder().build()),
		});

		Dataset<Row> vertices = sqlCtx.createDataFrame(vertices_rdd, vertices_schema);
		return vertices;
	}

	private static Dataset<Row> readAndLoadEdges(JavaSparkContext ctx, SQLContext sqlCtx) throws FileNotFoundException{

		File edgesFile = new File("src/main/resources/wiki-edges.txt");
		List<Row> edges_list = new ArrayList<Row>();
		Scanner scannerEdges = new Scanner(edgesFile);

		while (scannerEdges.hasNextLine()) {
			String line = scannerEdges.nextLine();
			String[] data = line.split("\t", 2);
			String id = data[0];
			String idDest = data[1];
			edges_list.add(RowFactory.create(id,idDest));
		}
		scannerEdges.close();
		JavaRDD<Row> edges_rdd = ctx.parallelize(edges_list);

		StructType edges_schema = new StructType(new StructField[]{
				new StructField("src", DataTypes.StringType, true, new MetadataBuilder().build()),
				new StructField("dst", DataTypes.StringType, true, new MetadataBuilder().build()),
		});

		Dataset<Row> edges =  sqlCtx.createDataFrame(edges_rdd, edges_schema);
		return edges;
	}


}
