package ru.vorobyov.simplificationmethods.service;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import ru.vorobyov.simplificationmethods.configuration.ApplicationConfiguration;
import ru.vorobyov.simplificationmethods.configuration.ConfigurationFields;

import java.util.ArrayList;
import java.util.List;

public class MongoService {
    private final static String MONGO_PATH =
            ApplicationConfiguration.getProperty(ConfigurationFields.MONGO_PATH);
    private final static String MONGO_DATABASE =
            ApplicationConfiguration.getProperty(ConfigurationFields.MONGO_DATABASE);

    public List<float[]> getAllPoints(MongoModels model){
        String collectionName = getCollectionName(model);
        List<float[]> resultList = new ArrayList<>();

        try(MongoClient mongoClient = MongoClients.create(MONGO_PATH)){
            MongoDatabase database = mongoClient.getDatabase(MONGO_DATABASE);
            MongoCollection<Document> mongoCollection = database.getCollection(collectionName);

            mongoCollection.find().forEach(document -> {
                float x = document.getDouble("x").floatValue();
                float y = document.getDouble("y").floatValue();
                float z = document.getDouble("z").floatValue();
                float[] point = {x, y, z};
                resultList.add(point);
            });
        }

        return resultList;
    }

    public void saveAllPoints(MongoModels model, List<Document> points){
        dropCollection(model);
        String collectionName = getCollectionName(model);

        try(MongoClient mongoClient = MongoClients.create(MONGO_PATH)){
            MongoDatabase database = mongoClient.getDatabase(MONGO_DATABASE);
            MongoCollection<Document> mongoCollection = database.getCollection(collectionName);

            mongoCollection.insertMany(points);
        }
    }

    public void dropCollection(MongoModels model){
        String collectionName = getCollectionName(model);

        try(MongoClient mongoClient = MongoClients.create(MONGO_PATH)){
            MongoDatabase database = mongoClient.getDatabase(MONGO_DATABASE);
            MongoCollection<Document> mongoCollection = database.getCollection(collectionName);

            mongoCollection.drop();
        }
    }

    private String getCollectionName(MongoModels collection){
        return ApplicationConfiguration.getModelProperty(ConfigurationFields.MONGO_COLLECTION, collection);
    }
}
