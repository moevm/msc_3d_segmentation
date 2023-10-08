package ru.vorobyov.simplificationmethods.service;

public enum MongoModels {
    INPUT(".input"),
    OUTPUT_GEOMETRIC_METHOD(".output.geometric");

    private final String fieldName;
    private static final String CATEGORY = ".model";

    MongoModels(String value) {
        this.fieldName = CATEGORY + value;
    }

    public String getFieldName() {
        return fieldName;
    }
}
