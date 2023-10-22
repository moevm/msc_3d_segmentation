package ru.vorobyov.simplificationmethods.service.mongo;

public enum MongoModels {
    INPUT(".input"),
    OUTPUT(".output");

    private final String fieldName;
    private static final String CATEGORY = ".model";

    MongoModels(String value) {
        this.fieldName = CATEGORY + value;
    }

    public String getFieldName() {
        return fieldName;
    }
}
