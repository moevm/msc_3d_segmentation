package ru.vorobyov.simplificationmethods.configuration;

public enum ConfigurationFields {
    MONGO_PATH("mongo.path"),
    MONGO_DATABASE("mongo.database"),
    MONGO_COLLECTION("mongo.collection"),
    SCRIPT_PYTHON_INPUT("script.python.input.path"),
    SCRIPT_PYTHON_OUTPUT("script.python.output.path"),
    SCRIPT_PYTHON_METHOD("script.python.method");

    private final String fieldName;

    ConfigurationFields(String value) {
        this.fieldName = value;
    }

    String getFieldName() {
        return fieldName;
    }
}
