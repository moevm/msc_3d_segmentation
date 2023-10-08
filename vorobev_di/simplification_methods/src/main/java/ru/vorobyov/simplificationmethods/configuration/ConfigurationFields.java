package ru.vorobyov.simplificationmethods.configuration;

public enum ConfigurationFields {
    MONGO_PATH("mongo.path"),
    MONGO_DATABASE("mongo.database"),
    MONGO_COLLECTION("mongo.collection");

    private final String fieldName;

    ConfigurationFields(String value) {
        this.fieldName = value;
    }

    String getFieldName() {
        return fieldName;
    }
}
