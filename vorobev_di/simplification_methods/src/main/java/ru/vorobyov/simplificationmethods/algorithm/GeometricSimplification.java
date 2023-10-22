package ru.vorobyov.simplificationmethods.algorithm;

import org.bson.Document;
import ru.vorobyov.simplificationmethods.service.mongo.MongoModels;
import ru.vorobyov.simplificationmethods.service.mongo.MongoService;

import java.util.ArrayList;
import java.util.List;

public class GeometricSimplification implements Algorithm{
    private final int divisionsNum;
    private final MongoService mongoService;

    public GeometricSimplification(int divisionsNum) {
        this.divisionsNum = divisionsNum;
        mongoService = new MongoService();
    }

    @Override
    public void process(){
        List<float[]> vertices = mongoService.getAllPoints(MongoModels.INPUT);

        List<float[]> boundingBox = createBoundingBox(vertices);
        List<float[][]> divisionBounds = calculateDivisionBounds(boundingBox);
        List<Document> strongPoints = calculateStrongPoints(vertices, divisionBounds);

        mongoService.saveAllPoints(MongoModels.OUTPUT, strongPoints);
    }

    private List<float[]> createBoundingBox(List<float[]> vertices){
        float[] firstVertex = vertices.get(0);
        float maxX;
        float maxY;
        float maxZ;
        float minX = maxX = firstVertex[0];
        float minY = maxY = firstVertex[1];
        float minZ = maxZ = firstVertex[2];

        for (float[] vertex : vertices) {
            float x = vertex[0];
            float y = vertex[1];
            float z = vertex[2];

            minX = Math.min(minX, x);
            minY = Math.min(minY, y);
            minZ = Math.min(minZ, z);

            maxX = Math.max(maxX, x);
            maxY = Math.max(maxY, y);
            maxZ = Math.max(maxZ, z);
        }

        return List.of(
                new float[] {minX, minY, minZ},
                new float[] {maxX, minY, minZ},
                new float[] {minX, maxY, minZ},
                new float[] {maxX, maxY, minZ},

                new float[] {minX, minY, maxZ},
                new float[] {maxX, minY, maxZ},
                new float[] {minX, maxY, maxZ},
                new float[] {maxX, maxY, maxZ}
        );
    }

    public List<float[][]> calculateDivisionBounds(List<float[]> boundingBox) {
        float[] minPoint = boundingBox.get(0);
        float[] maxPoint = boundingBox.get(1);

        float minX = minPoint[0];
        float minY = minPoint[1];
        float minZ = minPoint[2];
        float maxX = maxPoint[0];
        float maxY = maxPoint[1];
        float maxZ = maxPoint[2];

        float xRange = maxX - minX;
        float yRange = maxY - minY;
        float zRange = maxZ - minZ;

        float divisionSizeX = xRange / divisionsNum;
        float divisionSizeY = yRange / divisionsNum;
        float divisionSizeZ = zRange / divisionsNum;

        List<float[][]> divisionBounds = new ArrayList<>();

        for (int i = 0; i < divisionsNum; i++) {
            float divisionMinX = minX + i * divisionSizeX;
            float divisionMaxX = divisionMinX + divisionSizeX;

            for (int j = 0; j < divisionsNum; j++) {
                float divisionMinY = minY + j * divisionSizeY;
                float divisionMaxY = divisionMinY + divisionSizeY;

                for (int k = 0; k < divisionsNum; k++) {
                    float divisionMinZ = minZ + k * divisionSizeZ;
                    float divisionMaxZ = divisionMinZ + divisionSizeZ;

                    float[][] divisionBoundsPair = {
                            {divisionMinX, divisionMinY, divisionMinZ},
                            {divisionMaxX, divisionMaxY, divisionMaxZ}
                    };

                    divisionBounds.add(divisionBoundsPair);
                }
            }
        }

        return divisionBounds;
    }

    private List<Document> calculateStrongPoints(List<float[]> points, List<float[][]> divisionBounds) {
        List<Document> result = new ArrayList<>();

        for (float[][] bound : divisionBounds){
            float shortestDistance = Float.MAX_VALUE;
            float[] strongPoint = null;

            float[] center = {
                    (bound[0][0] + bound[1][0]) / 2,
                    (bound[0][1] + bound[1][1]) / 2,
                    (bound[0][2] + bound[1][2]) / 2
            };

            for (float[] vertex : points){
                float distance = calculateDistance(vertex, center);
                if (distance < shortestDistance) {
                    shortestDistance = distance;
                    strongPoint = vertex;
                }
            }
            if (strongPoint != null){
                Document pointDocument = pointToDocument(strongPoint);
                result.add(pointDocument);
            }
        }

        return result;
    }

    private Document pointToDocument(float[] point){
        return new Document()
                .append("x", point[0])
                .append("y", point[1])
                .append("z", point[2]);
    }

    private float calculateDistance(float[] point1, float[] point2) {
        float dx = point1[0] - point2[0];
        float dy = point1[1] - point2[1];
        float dz = point1[2] - point2[2];
        return (float) Math.sqrt(dx * dx + dy * dy + dz * dz);
    }
}
